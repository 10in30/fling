from fastapi import FastAPI
from .namefinder import get_all_domains, get_company_name_for

app = FastAPI(title="fling")


@app.get("/namer", tags=["names"])
async def generate_names(phrase: str = "Clothing for Autistic Children") -> dict:
    names = get_all_domains(phrase)
    return {'names': names}
