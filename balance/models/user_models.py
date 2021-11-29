from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from balance.database.settings import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    fullname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    identity = relationship("Identity", back_populates="user")

    def __init__(self,
                 entity_id: str = None,
                 surname: str = None,
                 fullname: str = None,
                 email: str = None,
                 hashed_password: str = None,
                 is_active: bool = None):
        self.entity_id = entity_id
        self.surnam = surname
        self.fullname = fullname
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active

    def to_json(self):
        return vars(self)


class Identity(Base):
    __tablename__ = "identity"

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="identity")
