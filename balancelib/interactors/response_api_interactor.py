
class ResponseError(Exception):
    def __init__(self,
                 message: str,
                 status_code: int):
        self.message = message
        self.status_code = status_code

    def error(self):
        return {
            "success": False,
            "message": self.message,
            "status_code": self.status_code,
        }


def ResponseSuccess(body):
    body.update({"success": True})
    return body
