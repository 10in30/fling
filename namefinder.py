from dotenv import load_dotenv
import openai
import json
from os import environ
from pprint import pprint
import requests
import httpx

load_dotenv()

openai.api_key = environ["OPENAI_API_KEY"]

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

