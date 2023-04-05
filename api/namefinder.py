from dotenv import load_dotenv
import openai
import json
from os import environ
import httpx


load_dotenv()

openai.api_key = environ["OPENAI_API_KEY"]
name_token_dev = environ["NAME_TOKEN_DEV"]
name_user = environ["NAME_USER"]


def get_company_name_for(description):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(description),
        temperature=0,
        n=1
    )
    return response["choices"][0].get("text").split(",")


def generate_prompt(description):
    return """Suggest three names for a company based on these descriptors. Name should be one word long.
Description: {}
Only respond with the three names, with a comma and space between each. For example:
Name 1, Name 2, Name 3

""".format(
        description.capitalize()
    )


def query_name_for_domains(phrase):
    print(phrase)
    params = f'{{"keyword":"{phrase}"}}'
    headers = {'Content-Type': 'application/json'}

    r = httpx.post("https://api.dev.name.com/v4/domains:search",
                   data=params, auth=(name_user, name_token_dev), headers=headers)

    return (json.loads(r.content))


def is_domain_free(domains):
    allowed_tlds = ["com", "net", "io", "co", "ai", "info", "xyz", "org"]
    free_domains = [{"domain": d.get('domainName'), "available": d.get('purchasable'), "price": f"{d.get('purchasePrice')} USD"} 
                    for d in domains.get('results', []) if d.get(
        'purchasable') is True and d.get('tld') in allowed_tlds]
    if free_domains:
        return free_domains
    else:
        return []


def get_all_domains(phrase):
    companies = get_company_name_for(phrase)
    domains = [query_name_for_domains(c) for c in companies]
    free_domains = [is_domain_free(d) for d in domains]
    return free_domains
