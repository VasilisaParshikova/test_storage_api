from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse

import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get("ENV") == "test":
    from src.api import products_api, orders_api
    from src.models.database import engine, session, Base
else:
    from api import products_api, orders_api
    from models.database import engine, session, Base

app = FastAPI()

app.include_router(products_api.router, prefix="/products", tags=["Products"])
app.include_router(orders_api.router, prefix="/orders", tags=["Orders"])


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await session.close()
    await engine.dispose()


@app.get("/")
async def root():
    return {"message": "Welcome to warehouse API"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
