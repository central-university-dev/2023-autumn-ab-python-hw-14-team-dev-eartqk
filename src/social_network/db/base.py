from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class DefaultIdBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        attrs = ', '.join(f'{field}: {getattr(self, field)}' for field in self.__repr_fields__)
        return f'{self.__class__.__name__}({attrs})'


class CreateTimestampMixin(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())  # pylint: disable=E1102


class UpdateTimestampMixin(Base):
    __abstract__ = True

    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=func.now())  # pylint: disable=E1102
