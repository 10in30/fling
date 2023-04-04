from dotenv import load_dotenv
import openai
import json
from os import environ
from pprint import pprint
import requests
import httpx
import base64

load_dotenv()

openai.api_key = environ["OPENAI_API_KEY"]
name_token_dev = environ["NAME_TOKEN_DEV"]
name_user = environ["NAME_USER"]

def models():
    headers = {'Authorization': f'Bearer {openai.api_key}'}
    r = httpx.get("https://api.openai.com/v1/models", headers=headers )
    pprint(r.url)
    return json.loads(r.content)

def get_company_name_for(description):
    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(description),
            temperature=0.6,
        )
    return response["choices"][0].get("text")



def generate_prompt(description):
    return """Suggest three names for a company based on these descriptors. Name should be one word long.
Description: {}
Names:""".format(
        description.capitalize()
    )

def find_domain(phrase):
    params = f'{{"keyword":"{phrase}"}}'
    headers = {'Content-Type': 'application/json'}

    r = httpx.post("https://api.dev.name.com/v4/domains:search", data=params
                   , auth=(name_user, name_token_dev), headers=headers)

    return(json.loads(r.content))

def is_domain_free(domains):
    pprint(domains['results'])
    free_domains = [(d.get('domainName'), d.get('purchasable'), d.get('purchasePrice'), d.get('tld')) for d in domains['results'] if d.get('purchasable') is True and d.get('tld') in ["com", "net", "io", "co", "ai", "info", "xyz", "org"]]
    return free_domains

