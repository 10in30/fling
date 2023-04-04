from fastapi import FastAPI
from .namefinder import get_company_name_for

app = FastAPI(title="fling")


@app.get("/namer", tags=["names"])
async def generate_names(phrase: str = "Clothing for Autistic Children") -> dict:
    names = get_company_name_for(phrase)
    return {
        "names": names
    }
