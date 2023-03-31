from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database.settings import Base


class User(Base):
    __tablename__ = "TB_USER"

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String(255))
    fullname = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)

    bank = relationship("Bank")

    def to_json(self):
        return vars(self)

