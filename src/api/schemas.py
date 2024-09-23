from datetime import datetime

from pydantic import BaseModel
from typing import Union


class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    amount_in_stock: int


class ProductPut(BaseModel):
    title: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    amount_in_stock: Union[int, None] = None


class ProductSch(ProductBase):
    id: int


class ProductInList(BaseModel):
    products: list[ProductSch]


class OrderItem(BaseModel):
    product_id: int
    amount: int


class OrderStatus(BaseModel):
    status: str


class OrderPost(BaseModel):
    products: list[OrderItem]


class OrderSch(OrderStatus, OrderPost):
    id: int
    date: datetime


class OrderInList(BaseModel):
    orders: list[OrderSch]


class Answer(BaseModel):
    result: bool


class PostAnswer(Answer):
    id: int


# class TweetBase(BaseModel):
#     content: str
#
#
# class TweetPost(BaseModel):
#     tweet_data: str
#     tweet_media_ids: Union[list[int], None] = None
#
#
# class User(BaseModel):
#     id: int
#     name: str
#
#     class Config:
#         orm_mode = True
#
#
# class Like(BaseModel):
#     user_id: int
#     name: str
#
#

#
#
# class TweetInlist(TweetBase):
#     id: int
#     attachments: list[str] = []
#     author: User
#     likes: list[Like] = []
#
#     class Config:
#         orm_mode = True
#
#
# class TweetAnswer(Answer):
#     tweets: list[TweetInlist]
#
#
# class UserPage(User):
#     followers: list[User]
#     following: list[User]
#
#
# class UserAnswer(Answer):
#     user: UserPage
#
#
# class MediaAnswer(Answer):
#     media_id: int
