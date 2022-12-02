import os
from pynubank import Nubank

from balance_service.interfaces.nubank import (
    NuBankServiceBasicInterface,
)


class NuBankInteractor(NuBankServiceBasicInterface):
    def __init__(self):
        self.service = Nubank()

    def authenticate(self,
                     token: str,
                     certificate_path: str):
        return self.service.authenticate_with_refresh_token(
            token,
            certificate_path)

    def has_certificate(self, certificate_path):
        is_file = os.path.isfile(certificate_path)
        if is_file:
            return True
        return False

    def get_balance(self):
        return self.service.get_account_balance()

    def get_transactions(self) -> list:
        return self.service.get_account_statements()