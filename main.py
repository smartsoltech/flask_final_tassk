from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import logging
from typing import Optional, Type, TypeVar, Generic

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка FastAPI и SQLAlchemy
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модели SQLAlchemy
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

Base.metadata.create_all(bind=engine)

# Модели Pydantic
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

# Создание FastAPI приложения
app = FastAPI()

# Dependency для получения сессии SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создаем обобщенные переменные типов для моделей и схем Pydantic
T = TypeVar("T", bound=Base)  # Для моделей SQLAlchemy
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)  # Для схем создания Pydantic
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)  # Для схем обновления Pydantic

class CRUDBase(Generic[T, CreateSchema, UpdateSchema]):
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, db: Session, *, obj_in: CreateSchema) -> T:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)  # Создаем экземпляр модели SQLAlchemy
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int) -> Optional[T]:
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, db: Session, *, db_obj: T, obj_in: UpdateSchema) -> T:
        obj_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Optional[T]:
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
            return obj

# Создаем экземпляры CRUDBase для каждой модели
crud_user = CRUDBase[User, UserCreate, UserBase](User)
crud_product = CRUDBase[Product, ProductCreate, ProductBase](Product)
crud_order = CRUDBase[Order, OrderCreate, OrderBase](Order)

# Маршруты FastAPI
@app.post("/users/", response_model=UserBase)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create(db, obj_in=user)

@app.get("/users/{user_id}", response_model=UserBase)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get(db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserBase)
def update_user_route(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    db_user = crud_user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update(db, db_obj=db_user, obj_in=user)

@app.delete("/users/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.remove(db, id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}

# Маршруты для Product
@app.post("/products/", response_model=ProductBase)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create(db, obj_in=product)

@app.get("/products/{product_id}", response_model=ProductBase)
def read_product_route(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get(db, id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductBase)
def update_product_route(product_id: int, product: ProductBase, db: Session = Depends(get_db)):
    db_product = crud_product.get(db, id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud_product.update(db, db_obj=db_product, obj_in=product)

@app.delete("/products/{product_id}")
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.remove(db, id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}

# Маршруты для Order
@app.post("/orders/", response_model=OrderBase)
def create_order_route(order: OrderCreate, db: Session = Depends(get_db)):
    return crud_order.create(db, obj_in=order)

@app.get("/orders/{order_id}", response_model=OrderBase)
def read_order_route(order_id: int, db: Session = Depends(get_db)):
    order = crud_order.get(db, id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=OrderBase)
def update_order_route(order_id: int, order: OrderBase, db: Session = Depends(get_db)):
    db_order = crud_order.get(db, id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud_order.update(db, db_obj=db_order, obj_in=order)

@app.delete("/orders/{order_id}")
def delete_order_route(order_id: int, db: Session = Depends(get_db)):
    order = crud_order.remove(db, id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
