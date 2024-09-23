from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("ENV") == "test":
    from src.models.models import Product, Order
    from src.models.database import session
else:
    from models.models import Product, Order
    from models.database import session



class OrderService:

    @staticmethod
    async def get_order_by_id(id: int) -> Order:
        order = await session.execute(
            select(Order).where(Order.id == id).options(selectinload(Order.items))
        )
        order = order.scalars().first()
        return order

    @staticmethod
    async def get_all_orders() -> List[Order]:
        orders = await session.execute(select(Order).options(selectinload(Order.items)))
        orders = orders.scalars().all()
        return orders


class ProductService:

    @staticmethod
    async def get_product_by_id(id: int) -> Product:
        product = await session.execute(select(Product).where(Product.id == id))
        product = product.scalars().first()
        return product

    @staticmethod
    async def get_all_products() -> List[Product]:
        products = await session.execute(select(Product))
        products = products.scalars().all()
        return products
