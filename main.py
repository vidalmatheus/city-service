from fastapi import FastAPI
from routes import city_routes, status_routes

app = FastAPI()

app.include_router(status_routes.router)
app.include_router(city_routes.router, prefix="/city")
