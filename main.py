from fastapi import FastAPI

from services import ibge_svc

app = FastAPI()


@app.get("/")
async def status():
    """
    This endpoint is used for health metrics
    """
    return {"status": "ok"}


@app.get("/city/external-fetching")
async def fetch_cities():
    """
    This route is used for fetching all existing cities in Brazil through IBGE's API
    """
    resp = ibge_svc.get_cities()
    return resp


@app.get("/city")
async def list_cities():
    """
    This route is used to list available cities
    """
    return {}
