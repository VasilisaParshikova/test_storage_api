from fastapi import APIRouter, Path, Depends
from fastapi.responses import JSONResponse

import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("ENV") == "test":
    from src.api.schemas import (
        PostAnswer,
        Answer,
        OrderInList,
        OrderSch,
        OrderStatus,
        OrderPost,
    )
    from src.models.models import Order, OrderItem
    from src.models.database import session
    from src.models.db_service import OrderService, ProductService
else:
    from api.schemas import (
        PostAnswer,
        Answer,
        OrderInList,
        OrderSch,
        OrderStatus,
        OrderPost,
    )
    from models.models import Order, OrderItem
    from models.database import session
    from models.db_service import OrderService, ProductService

from fastapi import HTTPException
from http import HTTPStatus


router = APIRouter()


async def get_order(id: int = Path(title="Id of the order")):
    order = await OrderService.get_order_by_id(id)
    if order:
        return order
    else:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order not found.")


@router.get("", response_model=OrderInList)
async def get_all_orders():
    orders = await OrderService.get_all_orders()
    orders = [order.to_json() for order in orders]
    return JSONResponse(content={"orders": orders})


@router.post("", response_model=PostAnswer)
async def post_order(order: OrderPost):
    products = order.products
    async with session.begin_nested():
        new_order = Order()
        session.add(new_order)

        for product in products:
            product_in_stock = await ProductService.get_product_by_id(
                product.product_id
            )
            if product_in_stock and product_in_stock.amount_in_stock >= product.amount:
                product_in_stock.amount_in_stock -= product.amount
                new_order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.product_id,
                    amount=product.amount,
                )
                session.add(product_in_stock)
                session.add(new_order_item)
            else:
                await session.rollback()
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="This amount of such products are not available",
                )
        await session.commit()
    return JSONResponse(
        content={"result": True, "id": new_order.id}, status_code=HTTPStatus.CREATED
    )


@router.get("/{id}", dependencies=[Depends(get_order)], response_model=OrderSch)
async def get_order(order: Order = Depends(get_order)):
    return JSONResponse(content=order.to_json())


@router.patch("/{id}/status", dependencies=[Depends(get_order)], response_model=Answer)
async def update_order_status(
    order_status: OrderStatus, id: int = Path(title="Id of the order")
):
    order = await OrderService.get_order_by_id(id)
    order.status = order_status.status
    session.add(order)
    await session.commit()
    return JSONResponse(content={"result": True})
