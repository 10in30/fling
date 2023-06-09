import hashlib
import io
from typing import Annotated, Union
from fastapi import FastAPI, Header
import requests
from .namefinder import get_all_domains
from starlette.responses import RedirectResponse
from fling_core.github import (
    github_client_id,
    github_client_secret,
    validate_token,
    get_username_from_token,
)
from fling_core import settings
import json
import botocore
from . import BUCKET, s3_client, r53, SSH_KEY, SSH_USERNAME
from cachetools import TTLCache, cached
from paramiko import SSHClient, RSAKey, AutoAddPolicy
from scp import SCPClient


app = FastAPI(title="fling")


@app.get("/")
async def index():
    return {"hello": "world"}


def push_key(key_string: str, username: str):
    with SSHClient() as ssh:
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        # TODO(JMC) Store Host key for server somewhere (TXT record?)
        keyio = io.StringIO(SSH_KEY)
        k = RSAKey.from_private_key(keyio)
        ssh.load_system_host_keys()
        ssh.connect("fling.team", username=SSH_USERNAME, pkey=k)
        with SCPClient(ssh.get_transport()) as scp:
            fl = io.BytesIO()
            fl.write(key_string.encode())
            fl.seek(0)
            scp.putfo(fl, f"~/{username}.keys")
            ssh.exec_command(
                f"echo >> /mnt/stateful_partition/sish/pubkeys/{username}.keys && \
                    cat {username}.keys >> /mnt/stateful_partition/sish/pubkeys/{username}.keys"
            )


@app.put("/expose_app", tags=["loophost"])
async def expose_app(
    app_name: str,
    ssh_public_key: str = None,
    gh_token: Annotated[Union[str, None], Header()] = None,
):
    username = get_username_from_token(gh_token)
    if not username:
        raise
    # TODO(JMC) Ensure this is a paid account
    ensure_username_team_records(username)
    keys = ssh_public_key
    if not keys:
        keys = requests.get(f"https://github.com/{username}.keys").text
    push_key(keys, username)
    # TODO(Set up the TXT records to pin the ssh keys)


@app.put("/txt_record", tags=["loophost"])
async def add_txt_record(
    validation_domain_name: str,
    validation: str,
    ttl: int,
    gh_token: Annotated[Union[str, None], Header()] = None,
):
    username = get_username_from_token(gh_token)
    if not username:
        raise
    ensure_username_a_record(username, "loophost.dev")
    # TODO: Make sure the username matches the requested domain name
    change_id = change_txt_record("CREATE", validation_domain_name, validation, ttl)
    return {"result": change_id}


@app.delete("/txt_record", tags=["loophost"])
async def del_txt_record(
    validation_domain_name: str,
    validation: str,
    ttl: int,
    gh_token: Annotated[Union[str, None], Header()] = None,
):
    username = get_username_from_token(gh_token)
    if not username:
        raise
    change_id = change_txt_record("DELETE", validation_domain_name, validation, ttl)
    return {"result": change_id}


def _find_zone_id_for_domain(domain: str) -> str:
    """Find the zone id responsible a given FQDN.

    That is, the id for the zone whose name is the longest parent of the
    domain.
    """
    paginator = r53.get_paginator("list_hosted_zones")
    zones = []
    target_labels = domain.rstrip(".").split(".")
    for page in paginator.paginate():
        for zone in page["HostedZones"]:
            if zone["Config"]["PrivateZone"]:
                continue

            candidate_labels = zone["Name"].rstrip(".").split(".")
            if candidate_labels == target_labels[-len(candidate_labels):]:
                zones.append((zone["Name"], zone["Id"]))

    if not zones:
        raise Exception("Unable to find a Route53 hosted zone for {0}".format(domain))

    # Order the zones that are suffixes for our desired to domain by
    # length, this puts them in an order like:
    # ["foo.bar.baz.com", "bar.baz.com", "baz.com", "com"]
    # And then we choose the first one, which will be the most specific.
    zones.sort(key=lambda z: len(z[0]), reverse=True)
    return zones[0][1]


def ensure_username_a_record(username: str, loophost_domain: str):
    print(f"Adding A records for {username} on {loophost_domain}")
    zone_id = _find_zone_id_for_domain(loophost_domain)  # TODO(generalize me)
    add_localhost_entry(f"{username}.{loophost_domain}", zone_id)
    add_localhost_entry(f"*.{username}.{loophost_domain}", zone_id)


def ensure_username_team_records(username: str):
    zone_id = _find_zone_id_for_domain("fling.team")  # TODO(generalize me)
    add_tunnel_entry(f"{username}.fling.team", zone_id)
    add_tunnel_entry(f"*.{username}.fling.team", zone_id)


def add_tunnel_entry(domain, zone_id):
    return add_a_record(domain, "34.102.104.118", zone_id)


def add_localhost_entry(loophost_domain, zone_id):
    return add_a_record(loophost_domain, "127.0.0.1", zone_id)


def add_a_record(domain, a_record, zone_id):
    return r53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": "flingdev adding loophost " + domain,
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": domain,
                        "Type": "A",
                        "TTL": 60,
                        "ResourceRecords": [{"Value": a_record}],
                    },
                }
            ],
        },
    )


def change_txt_record(
    action: str, validation_domain_name: str, validation: str, ttl: str
) -> str:

    zone_id = _find_zone_id_for_domain(validation_domain_name)
    rrecords = [{"Value": '"{0}"'.format(validation)}]
    response = r53.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": "certbot-dns-route53 certificate validation " + action,
            "Changes": [
                {
                    "Action": action,
                    "ResourceRecordSet": {
                        "Name": validation_domain_name,
                        "Type": "TXT",
                        "TTL": ttl,
                        "ResourceRecords": rrecords,
                        "MultiValueAnswer": True,
                        "SetIdentifier": validation,
                    },
                }
            ],
        },
    )
    return response["ChangeInfo"]["Id"]


@app.get("/namer", tags=["names"])
async def generate_names(
    phrase: str, gh_token: Annotated[Union[str, None], Header()] = None
) -> dict:
    names = get_all_domains(phrase)
    return {"names": names}


@app.get("/github-login")
async def github_login(state: str):
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={github_client_id}&state={state}&scope=repo",
        status_code=307,
    )


def get_token_from_code(code):
    params = {
        "client_id": github_client_id,
        "client_secret": github_client_secret,
        "code": code,
    }

    headers = {"Accept": "application/json"}
    response = requests.post(
        url="https://github.com/login/oauth/access_token",
        params=params,
        headers=headers,
    )
    response_json = response.json()
    print(response_json)
    access_token: str = response_json.get("access_token")
    return access_token


@app.get("/callback")
async def github_code(code: str, state: str):
    # TODO(JMC): Accept parameter for local port number
    access_token = get_token_from_code(code)
    validation = validate_token(access_token)
    if validation.status_code != 200:
        raise "Token is invalid"
    username: str = validation.json()["user"]["login"]
    return RedirectResponse(
        f"http://localhost:5817/callback?token={access_token}&username={username}&state={state}",
        status_code=307,
    )


@app.get("/callback/web-prod")
async def token_to_web(code: str, state: str):
    access_token = get_token_from_code(code)
    return RedirectResponse(
        f"{settings.web_server}/callback?oauth_token={access_token}&state={state}",
        status_code=307,
    )


@app.get("/repolist", tags=["data"])
async def get_repo_list(gh_token: Annotated[Union[str, None], Header()] = None):
    username = get_username_from_token(gh_token)
    if not username:
        return {"error": "No Github Token or Token not valid"}
    repos = get_repos_by_username(username, gh_token)
    return repos


@cached(cache=TTLCache(maxsize=100, ttl=60))
def get_repos_by_username(username, gh_token):
    headers = {"Accept": "application/json", "Authorization": f"Bearer {gh_token}"}
    return paginated_gh_api("https://api.github.com/user/repos?per_page=200", headers)


def paginated_gh_api(first_url, headers):
    session = requests.Session()
    repo_list = []
    url = first_url
    while url:
        repos_response = session.get(url=url, headers=headers)
        repo_list.extend(repos_response.json())
        url = repos_response.links.get("next", {}).get("url", None)
    return repo_list


@app.get("/index", tags=["data"])
async def read_index(gh_token: Annotated[Union[str, None], Header()] = None) -> dict:
    username = get_username_from_token(gh_token)
    return project_index_for_user(username)


index_cache = TTLCache(maxsize=100, ttl=30)


@cached(cache=index_cache)
def project_index_for_user(username):
    index = safe_read_data(f"gh{username}")
    print(f"Reading index for {username}, got {json.dumps(index)}")
    return index.get("projects", {})


@app.put("/index", tags=["data"])
async def add_to_index(
    fling_id, gh_token: Annotated[Union[str, None], Header()] = None
) -> dict:
    username = get_username_from_token(gh_token)
    repos = get_repos_by_username(username, gh_token)
    allowed_fling_ids = [f"github.com/{x['full_name']}" for x in repos]
    if fling_id not in allowed_fling_ids:
        raise Exception("This project is not in your repo list, not allowed?")

    index = safe_read_data(f"gh{username}")
    projects = index.get("projects", {})
    projects[fling_id] = {"visibility": "private"}
    index["projects"] = projects
    print(f"Writing {json.dumps(index)} to index file for {username}")
    s3_client.put_object(
        Body=json.dumps(index), Bucket=BUCKET, Key=f"gh{username}.json"
    )
    index_cache.clear()
    return index


@app.post("/{fling_id}/add", tags=["data"])
async def add_data(
    fling_id: str,
    key: str,
    val: str,
    gh_token: Annotated[Union[str, None], Header()] = None,
) -> dict:
    username = get_username_from_token(gh_token)
    index = project_index_for_user(username)
    # TODO(JMC): Optimize this, store the hashes maybe?
    hashes = [hashlib.md5(x.encode("utf-8")).hexdigest() for x in index.keys()]
    if fling_id not in hashes:
        raise Exception("You don't have permissions on this fling")
    cache = safe_read_data(fling_id)
    cache[key] = val
    s3_client.put_object(Body=json.dumps(cache), Bucket=BUCKET, Key=f"{fling_id}.json")
    return cache


@app.get("/{fling_id}", tags=["data"])
async def read_data(
    fling_id: str, gh_token: Annotated[Union[str, None], Header()] = None
) -> dict:
    username = get_username_from_token(gh_token)
    index = project_index_for_user(username)
    # TODO(JMC): Optimize this, store the hashes maybe?
    hashes = [hashlib.md5(x.encode("utf-8")).hexdigest() for x in index.keys()]
    if fling_id not in hashes:
        raise Exception("You don't have permissions on this fling")
    cache = safe_read_data(fling_id)
    return cache


def safe_read_data(fling_id: str):
    s3_obj = {}
    try:
        s3_obj = s3_client.get_object(Bucket=BUCKET, Key=f"{fling_id}.json")
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            pass
        else:
            raise e
    raw_cache = s3_obj.get("Body", io.BytesIO("{}".encode("utf-8")))
    cache = json.loads(raw_cache.read() or {})
    return cache
