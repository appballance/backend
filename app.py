from fastapi import FastAPI
from balancelib.routes import user_routes

app = FastAPI(app_name="balance")


app.include_router(user_routes.router)
