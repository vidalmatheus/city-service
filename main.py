from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes import city_routes, status_routes

app = FastAPI()

app.include_router(status_routes.router, prefix="/status")
app.include_router(city_routes.router, prefix="/city")


# Redirect to /docs
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse("/docs")
