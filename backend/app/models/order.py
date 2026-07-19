"""订单模型"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..database.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default="pending", nullable=False, index=True)
    configuration_json = Column(Text, nullable=True, default="{}")
    # 收货地址
    recipient_name = Column(String(100), nullable=True, default="")
    recipient_phone = Column(String(30), nullable=True, default="")
    address_line1 = Column(String(200), nullable=True, default="")
    address_line2 = Column(String(200), nullable=True, default="")
    city = Column(String(100), nullable=True, default="")
    state = Column(String(100), nullable=True, default="")
    zip_code = Column(String(20), nullable=True, default="")
    notes = Column(Text, nullable=True, default="")
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # 关系
    user = relationship("User", backref="orders")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status='{self.status}')>"
