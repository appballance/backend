from fastapi import FastAPI
from balancelib.routes import people_routes

app = FastAPI(app_name="balance")


app.include_router(people_routes.router)
