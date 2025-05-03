from typing import Optional
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_mail: Mapped[str] = mapped_column(String(100), nullable=False)
    user_password: Mapped[str] = mapped_column(String(100), nullable=False)
    user_reset_code: Mapped[Optional[int]] = mapped_column(Integer)
    user_trainer_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("trainer.trainer_id", ondelete="CASCADE"), default=1
    )
