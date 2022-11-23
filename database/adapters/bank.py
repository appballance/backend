from database.settings import ConnectionDatabase
from database.models.bank import Bank as BankModel

from balance_service.repositories.bank import BankRepositorie

from balance_domain.entities.bank import BankEntity


class BankAlchemyAdapter(
    BankRepositorie,
    ConnectionDatabase,
):
    def __init__(self):
        super().__init__()

    def create(self, bank: BankEntity):
        bank = BankModel(
            number=bank.number,
            token=bank.token,
            user_id=bank.user_id)
        self.session.add(bank)
        self.session.commit()
        self.session.refresh(bank)
        return bank

    def get_by_id(self, bank_id: str):
        banks = self.session.query(BankModel).filter(BankModel.id == bank_id).first()
        return banks

    def get_by_user_id(self, user_id: str):
        banks = self.session.query(BankModel).filter(BankModel.user_id == user_id).all()
        return banks

    def user_has_bank(self,
                      user_id: int,
                      bank_number: str):
        banks = self.session.query(BankModel).filter(
            BankModel.number == bank_number,
            BankModel.user_id == user_id,
        ).first()

        if banks is None:
            return False
        return True
