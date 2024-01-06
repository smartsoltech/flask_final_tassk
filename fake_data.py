from faker import Faker
from sqlalchemy.orm import Session
from main import User, Product, Order
from main import engine
import random
from datetime import datetime


# Создание экземпляра Faker
fake = Faker()

# Создание сессии базы данных
session = Session(bind=engine)

# Генерация фейковых пользователей
for _ in range(50):
    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password=fake.password()
    )
    session.add(user)

# Генерация фейковых товаров
for _ in range(1200):
    product = Product(
        name=fake.word(),
        description=fake.text(),
        price=random.randint(10, 1000)
    )
    session.add(product)
    

# Генерация фейковых заказов
users = session.query(User).all()
products = session.query(Product).all()
for _ in range(50):
    order_date = datetime.strptime(fake.date(), '%Y-%m-%d').date()
    order = Order(
        user_id=random.choice(users).id,
        product_id=random.choice(products).id,
        order_date=order_date,
        status=random.choice(["обработан", "доставляется", "доставлен"])
    )
    session.add(order)

# Сохранение изменений в базе данных
session.commit()

# Закрытие сессии
session.close()
