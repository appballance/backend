from pydantic import BaseModel


class RequestSendCodeCertificate(BaseModel):
    cpf: str
    password: str
    code: str
    device_id: str


class RequestAccount(BaseModel):
    cpf: str
    password: str


class RequestBank(BaseModel):
    code_id: str
    code: str
