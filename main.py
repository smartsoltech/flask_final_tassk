from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Date, select
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import List, Optional

# CORS middleware
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# SQLAlchemy model
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    order_date = Column(Date)
    status = Column(String)

# Pydantic models
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

class UserCreate(UserBase):
    pass

class ProductBase(BaseModel):
    name: str
    description: str
    price: int

class ProductCreate(ProductBase):
    pass

class OrderBase(BaseModel):
    user_id: int
    product_id: int
    order_date: str
    status: str

class OrderCreate(OrderBase):
    pass

# Session creation
engine = create_engine('sqlite:///./db.sqlite', connect_args={'check_same_thread': False})
Base.metadata.create_all(bind=engine)

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = DBSession()

# User routes
@app.post("/users/create/")
def create_user(user: UserCreate):
    db_user = User(**user.dict())
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user

@app.get("/users/")
def read_users():
    return db_session.query(User).all()

# Product routes
@app.post("/products/create/")
def create_product(product: ProductCreate):
    db_product = Product(**product.dict())
    db_session.add(db_product)
    db_session.commit()
    db_session.refresh(db_product)
    return db_product

@app.get("/products/")
def read_products():
    return db_session.query(Product).all()

# Order routes
@app.post("/orders/create/")
def create_order(order: OrderCreate):
    db_order = Order(**order.dict())
    db_session.add(db_order)
    db_session.commit()
    db_session.refresh(db_order)
    return db_order

@app.get("/orders/")
def read_orders():
    return db_session.query(Order).all()