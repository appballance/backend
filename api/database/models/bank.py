from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from database.settings import Base


class Bank(Base):
    __tablename__ = "TB_BANK"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5))
    certificate_url = Column(String(255))
    token = Column(String(800))
    is_active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("TB_USER.id"))

    def to_json(self):
        return vars(self)
