from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from balancelib.interactors.response_api_interactor import ResponseError
from balancelib.routes import nubank
from balancelib.routes import user_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(app_name="balance")


@app.exception_handler(ResponseError)
async def unicorn_exception_handler(request: Request, exc: ResponseError):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.error(),
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(nubank.router)
