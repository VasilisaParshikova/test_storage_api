from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, func
import enum

from sqlalchemy.orm import relationship

import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("ENV") == "test":
    from src.models.database import Base
else:
    from models.database import Base


class StatusEnum(enum.Enum):
    created = "created"
    in_progress = "in progress"
    sent = "sent"
    delivered = "delivered"


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    amount_in_stock = Column(Integer, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.created, nullable=False)
    items = relationship("OrderItem", backref="order", lazy="selectin")

    def to_json(self):
        order_data = {
            "id": self.id,
            "date": str(self.date),
            "status": self.status.name,
            "products": [item.to_order_json() for item in self.items]}
        return order_data


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    amount = Column(Integer, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_order_json(self):
        return {"product_id": self.product_id, "amount": self.amount}
