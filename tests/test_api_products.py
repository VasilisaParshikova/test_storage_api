import pytest
from src.models.models import Product


@pytest.mark.asyncio
async def test_post_product(client, setup_test_database):
    product_data = {
        "title": "test product 1",
        "description": "test description for product 1",
        "price": 5,
        "amount_in_stock": 100,
    }
    response = await client.post("/products", json=product_data)

    assert response.status_code == 201
    assert response.json()["result"]
    assert response.json()["id"] is not None


@pytest.mark.asyncio
async def test_get_all_products(client, setup_test_database):
    response = await client.get("/products")
    assert response.status_code == 200
    assert "products" in response.json()


@pytest.mark.asyncio
async def test_get_product(client, setup_test_database, db_session):
    new_product = Product(
        title="title", description="description", price=1, amount_in_stock=10
    )
    db_session.add(new_product)
    await db_session.commit()
    response = await client.get(f"/products/{new_product.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_product_error(client, setup_test_database, db_session):
    response = await client.get("/products/100100")
    assert response.status_code != 200
    assert "error" in response.json()


@pytest.mark.asyncio
async def test_put_product(client, setup_test_database, db_session):
    new_product = Product(
        title="title", description="description", price=1, amount_in_stock=10
    )
    db_session.add(new_product)
    await db_session.commit()
    product_data = {"description": "new_description", "price": 15}

    response = await client.put(f"/products/{new_product.id}", json=product_data)

    assert response.status_code == 200
    assert response.json()["result"]


@pytest.mark.asyncio
async def test_delete_product(client, setup_test_database, db_session):
    new_product = Product(
        title="title", description="description", price=1, amount_in_stock=10
    )
    db_session.add(new_product)
    await db_session.commit()

    response = await client.delete(f"/products/{new_product.id}")

    assert response.status_code == 200
    assert response.json()["result"]
