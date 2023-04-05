import io
from pprint import pprint
from fastapi import FastAPI
from .namefinder import get_all_domains
import json
import botocore
from . import BUCKET, s3_client

app = FastAPI(title="fling")


@app.get("/namer", tags=["names"])
async def generate_names(
        phrase: str = "Clothing for Autistic Children") -> dict:
    names = get_all_domains(phrase)
    return {'names': names}


@app.post("/<fling_id>/add", tags=["data"])
async def add_data(
    fling_id: str,
    key: str, val: str
) -> dict:
    s3_obj = {}
    try:
        s3_obj = s3_client.get_object(
            Bucket=BUCKET,
            Key=f"{fling_id}.json")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            pass
        else:
            raise e
    raw_cache = s3_obj.get("Body", io.BytesIO("{}".encode("utf-8")))
    cache = json.loads(raw_cache.read())
    pprint(cache)
    cache[key] = val
    s3_client.put_object(Body=json.dumps(cache),
                         Bucket=BUCKET,
                         Key=f"{fling_id}.json")
    return cache
