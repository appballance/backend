from fastapi import FastAPI
from routes.user import user

balance = FastAPI(app_name="balance")


balance.route(user)
