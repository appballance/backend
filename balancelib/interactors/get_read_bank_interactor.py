from balance_domain.entities.bank import BankEntity
from balance_service.interfaces.nubank import NuBankServiceInterface

from balancelib.interactors.nubank_interactor import NuBankInteractor
from balancelib.interactors.pagination_interactor import PaginationInteractor, PaginationRequest
from balancelib.interactors.response_api_interactor import (
    ResponseSuccess,
    ResponseError
)

from database.adapters.bank import BankAlchemyAdapter


class BasicTransactionResponse:
    def __init__(self,
                 amount: float,
                 address: str,
                 date: str,
                 type_payment: str,
                 type_transaction: str):
        self.amount = amount
        self.address = self.formatted_address(address)
        self.date = date
        self.type_payment = self.formatted_method_payment(type_payment)
        self.type_transaction = self.formatted_type_transaction(type_transaction)

    @staticmethod
    def formatted_method_payment(type_payment: str) -> str:
        types_payments = ['Pix']
        type_payment_cut = type_payment[0:3]

        for type_payment in types_payments:
            if type_payment == type_payment_cut:
                return type_payment_cut

        return type_payment

    @staticmethod
    def formatted_type_transaction(type_transaction: str) -> str:
        place_cut = type_transaction.find(' ')

        if place_cut == -1:
            return type_transaction

        type_transaction_formatted = type_transaction[(place_cut + 1):len(type_transaction)]

        if type_transaction_formatted == 'enviada':
            return 'expense'
        if type_transaction_formatted == 'recebida':
            return 'income'

        return ''

    @staticmethod
    def formatted_address(address: str) -> str:
        place_cut = address.find('\n')

        if place_cut == -1:
            return address

        return address[0:place_cut]

    def to_json(self) -> dict:
        return vars(self)


class BasicBankResponseModel:
    def __init__(self,
                 entity_id: int,
                 balance: int,
                 code: str,
                 transactions: list):
        self.entity_id = entity_id
        self.balance = balance
        self.code = code
        self.transactions = transactions

    def to_json(self) -> dict:
        return vars(self)


class GetReadBankResponseModel:
    def __init__(self, bank: BasicBankResponseModel):
        self.bank = bank

    def __call__(self):
        response = {}
        response.update(self.bank.to_json())
        return ResponseSuccess(response)


class GetReadBankRequestModel:
    def __init__(self,
                 entity_id: int,
                 user_id: str,
                 page: int,
                 per_page: int):
        self.entity_id = entity_id
        self.user_id = user_id
        self.page = page
        self.per_page = per_page


class GetReadBankInteractor:
    def __init__(self,
                 request: GetReadBankRequestModel,
                 adapter: BankAlchemyAdapter, ):
        self.request = request
        self.adapter = adapter

    def get_bank(self):
        bank = self.adapter.get_by_id(self.request.entity_id)

        if bank is None:
            raise ResponseError(status_code=400,
                                message="This bank don't exists")

        if bank.user_id != self.request.user_id:
            raise ResponseError(status_code=400,
                                message="This bank don't exists")

        return bank

    @staticmethod
    def get_nubank_instance(bank_token: str,
                            certificate_path: str):
        return NuBankServiceInterface(
            token=bank_token,
            certificate_path=certificate_path,
            bank_service=NuBankInteractor()
        )

    def enriched_bank_nubank(self, bank: BankEntity):
        nubank_instance = self.get_nubank_instance(
            bank_token=bank.token,
            certificate_path=bank.certificate_url
        )

        transactions = nubank_instance.get_transactions(quantity=None)

        new_transactions = [
            BasicTransactionResponse(
                amount=transaction['amount'],
                address=transaction['detail'],
                date=transaction['postDate'],
                type_payment=transaction['__typename'],
                type_transaction=transaction['title']
            ) for transaction in transactions
        ]

        request = PaginationRequest(
            rows=new_transactions,
            page=self.request.page,
            per_page=self.request.per_page,
        )
        interactor = PaginationInteractor(request)
        transactions_paginated = interactor.run()

        new_bank = BasicBankResponseModel(
            entity_id=bank.id,
            balance=nubank_instance.get_balance(),
            code=bank.code,
            transactions=transactions_paginated,
        )
        return new_bank

    def run(self):
        bank = self.get_bank()
        bank_enriched = self.enriched_bank_nubank(bank)
        response = GetReadBankResponseModel(bank_enriched)
        return response
