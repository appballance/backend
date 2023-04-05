import uuid
from fastapi import APIRouter

router = APIRouter()

encrypted_code = str(uuid.uuid4())


@router.post('/banco-original/uri')
def redirect_uri(request):
    print('request.body ::', request.body)
    return request.body
