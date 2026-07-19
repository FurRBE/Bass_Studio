"""贝斯配置选项模型"""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from ..database.base import Base


class BassOption(Base):
    __tablename__ = "bass_options"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String(50), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True, default="")
    price = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<BassOption(id={self.id}, category='{self.category}', name='{self.name}')>"
