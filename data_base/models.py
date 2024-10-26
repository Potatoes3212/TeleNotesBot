from sqlalchemy import BigInteger, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from data_base.database import Base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


# Модель для таблицы пользователей
class User(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    # Связи с заметками и напоминаниями
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="user", cascade="all, delete-orphan")


# Модель для таблицы заметок
class Note(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=True)
    file_id: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="notes")
