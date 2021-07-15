from fastapi import FastAPI
from routes import people

balance = FastAPI(app_name="balance")


balance.include_router(people.router)
