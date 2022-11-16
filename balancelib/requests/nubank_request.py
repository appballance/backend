from pydantic import BaseModel


class RequestSendCodeCertificate(BaseModel):
    cpf: str
    password: str
    device_id: str


class RequestAccount(BaseModel):
    cpf: str
    password: str
