from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from .database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    orders = relationship('Orders', back_populates='buyer', cascade='all, delete')
    stores = relationship('Stores', back_populates='seller', cascade='all, delete')
    cart = relationship('Cart', back_populates='users', cascade='all, delete', uselist=False)


# This is for the users who are 'buyers'
class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    status = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    buyer = relationship('Users', back_populates='orders')
    order_items = relationship('OrderItems', back_populates='order', cascade='all, delete')


class OrderItems(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Numeric(10, 2), nullable=False)

    order = relationship('Orders', back_populates='order_items')
    product = relationship('Products', back_populates='order_items')


class CartItems(Base):
    __tablename__ = 'cart_items'
    __table_args__ = (
        UniqueConstraint('cart_id', 'product_id')
    )

    id = Column(Integer, primary_key=True, index=True)

    cart_id = Column(Integer, ForeignKey('cart.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    quantity = Column(Integer, nullable=False)

    cart = relationship('Cart', back_populates='cart_items')
    product = relationship('Products')


class Cart(Base):
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, unique=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    users = relationship('Users', back_populates='cart')
    cart_items = relationship('CartItems', back_populates='cart', cascade='all, delete')


# This is for the users who are 'sellers'
class Stores(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(ForeignKey('users.id'))

    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    seller = relationship('Users', back_populates='stores')
    products = relationship('Products', back_populates='store', cascade='all, delete')


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(ForeignKey('stores.id'))

    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    image = Column(String, nullable=False)
    details = Column(JSONB, nullable=False)

    order_items = relationship('OrderItems', back_populates='product')
    store = relationship('Stores', back_populates='products')