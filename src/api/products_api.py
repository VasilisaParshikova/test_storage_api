from fastapi import APIRouter, Path, Depends
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("ENV") == "test":
    from src.models.models import Product
    from src.api.schemas import (
        ProductBase,
        ProductInList,
        PostAnswer,
        Answer,
        ProductPut,
        ProductSch,
    )
    from src.models.database import session
    from src.models.db_service import ProductService
else:
    from models.models import Product
    from api.schemas import (
        ProductBase,
        ProductInList,
        PostAnswer,
        Answer,
        ProductPut,
        ProductSch,
    )
    from models.database import session
    from models.db_service import ProductService

from fastapi import HTTPException
from http import HTTPStatus

router = APIRouter()


async def get_product(id: int = Path(title="Id of the product")):
    product = await ProductService.get_product_by_id(id)
    if product:
        return product
    else:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Product not found."
        )


@router.get("", response_model=ProductInList)
async def get_all_products():
    products = await ProductService.get_all_products()
    products = [product.to_json() for product in products]
    return JSONResponse(content={"products": products})


@router.post("", response_model=PostAnswer)
async def post_products(product: ProductBase):
    new_product = Product(
        title=product.title,
        description=product.description,
        price=product.price,
        amount_in_stock=product.amount_in_stock,
    )
    session.add(new_product)
    await session.commit()

    return JSONResponse(
        content={"result": True, "id": new_product.id}, status_code=HTTPStatus.CREATED
    )


@router.get("/{id}", dependencies=[Depends(get_product)], response_model=ProductSch)
async def get_product(product: Product = Depends(get_product)):
    return JSONResponse(content=product.to_json())


@router.put("/{id}", dependencies=[Depends(get_product)], response_model=Answer)
async def update_product(
    product: ProductPut, id: int = Path(title="Id of the product")
):
    upd_product = await ProductService.get_product_by_id(id)
    if product.title:
        upd_product.title = product.title
    if product.description:
        upd_product.description = product.description
    if product.price:
        upd_product.price = product.price
    if product.amount_in_stock:
        upd_product.amount_in_stock = product.amount_in_stock

    session.add(upd_product)
    await session.commit()

    return JSONResponse(content={"result": True})


@router.delete("/{id}", dependencies=[Depends(get_product)], response_model=Answer)
async def delete_product(id: int = Path(title="Id of the product")):
    product = await ProductService.get_product_by_id(id)
    await session.delete(product)
    await session.commit()
    return JSONResponse(content={"result": True})
