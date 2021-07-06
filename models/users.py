from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database.users import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    fullname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    identity = relationship("Identity", back_populates="user")

    def __str__(self) -> str:
        return f'{self.id} - {self.fullname}'


class Identity(Base):
    __tablename__ = "identity"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="identity")

    def __str__(self) -> str:
        return f'{self.id} - {self.user_id}'
