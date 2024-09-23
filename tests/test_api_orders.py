import pytest
from src.models.models import Order, Product, OrderItem


@pytest.mark.asyncio
async def test_post_order(client, setup_test_database, db_session):
    new_product = Product(
        title="title", description="description", price=1, amount_in_stock=10
    )
    db_session.add(new_product)
    await db_session.commit()
    order_data = {"products": [{"product_id": new_product.id, "amount": 5}]}
    response = await client.post("/orders", json=order_data)
    assert response.status_code == 201
    assert response.json()["result"]
    assert response.json()["id"] is not None


@pytest.mark.asyncio
async def test_post_order_error(client, setup_test_database, db_session):
    new_product = Product(
        title="title", description="description", price=1, amount_in_stock=10
    )
    db_session.add(new_product)
    await db_session.commit()
    order_data = {"products": [{"product_id": new_product.id, "amount": 50}]}
    response = await client.post("/orders", json=order_data)
    assert response.status_code != 200
    assert "error" in response.json()


@pytest.mark.asyncio
async def test_get_all_orders(client, setup_test_database):
    response = await client.get("/orders")
    assert response.status_code == 200
    assert "orders" in response.json()


@pytest.mark.asyncio
async def test_get_order(client, setup_test_database, db_session):
    new_product = Product(
        title="title", description="description", price=1, amount_in_stock=10
    )
    new_order = Order()
    db_session.add(new_order)
    db_session.add(new_product)
    await db_session.commit()
    new_order_item = OrderItem(
        order_id=new_order.id, product_id=new_product.id, amount=5
    )
    db_session.add(new_order_item)
    await db_session.commit()
    response = await client.get(f"/orders/{new_order.id}")
    assert response.status_code == 200
    assert len(response.json()["products"]) == 1


@pytest.mark.asyncio
async def test_get_order_error(client, setup_test_database, db_session):
    response = await client.get("/orders/100100")
    assert response.status_code != 200
    assert "error" in response.json()


@pytest.mark.asyncio
async def test_patch_order_status(client, setup_test_database, db_session):
    new_product = Product(
        title="title", description="description", price=1, amount_in_stock=10
    )
    new_order = Order()
    db_session.add(new_order)
    db_session.add(new_product)
    await db_session.commit()
    new_order_item = OrderItem(
        order_id=new_order.id, product_id=new_product.id, amount=5
    )
    db_session.add(new_order_item)
    await db_session.commit()
    order_data = {"status": "in_progress"}

    response = await client.patch(f"/orders/{new_order.id}/status", json=order_data)

    assert response.status_code == 200
    assert response.json()["result"]
