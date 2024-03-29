from database.settings import ConnectionDatabase
from database.models.user import User as UserModel

from balance_service.repositories.user import UserRepositorie

from balance_domain.entities.user import UserEntity


class UserAlchemyAdapter(UserRepositorie, ConnectionDatabase):
    def __init__(self):
        super().__init__()

    def create(self, user: UserEntity):
        user = UserModel(
            surname=user.surname,
            fullname=user.fullname,
            email=user.email,
            password=user.password,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self.session.close()
        return user

    def get_by_id(self, user_id: int):
        user = self.session.query(UserModel).filter(
            UserModel.id == user_id).first()
        self.session.close()
        return user

    def get_by_email(self, user_email: str):
        user = self.session.query(UserModel).filter(
            UserModel.email == user_email).first()
        self.session.close()
        return user
