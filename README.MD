Конечно, вот весь текст, отформатированный в одном блоке Markdown:

markdown
Copy code
# FastAPI CRUD Application

This is a FastAPI application with CRUD operations for three tables: Users, Products, and Orders. The application uses SQLAlchemy as the ORM and SQLite as the database.

## Prerequisites

- Python 3.8 or higher
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic

## Setup

Clone the repository:
```
git clone https://github.com/your_username/fastapi-crud-app.git
```
```
cd fastapi-crud-app
```

**Create a virtual environment and activate it:**

```
python3 -m venv venv
source venv/bin/activate
```

**Install the required packages:**
```
pip install -r requirements.txt
```

**Run the application:**
```
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## Database Models

The application has three SQLAlchemy models: User, Product, and Order.

### User
- id: Integer, primary key, unique, and auto-incrementing
- first_name: String, indexed
- last_name: String, indexed
- email: String, unique and indexed
- password: String

### Product
- id: Integer, primary key, unique, and auto-incrementing
- name: String, indexed
- description: String, indexed
- price: Integer

### Order
- id: Integer, primary key, unique, and auto-incrementing
- user_id: Integer, foreign key referencing User
- product_id: Integer, foreign key referencing Product
- order_date: Date
- status: String

## API Endpoints

### Users

- **Create a user**
  - Endpoint: `/users/create/`
  - Method: POST
  - Request body: UserCreate
  - Response: User

- **Get all users**
  - Endpoint: `/users/`
  - Method: GET
  - Response: List of User

- **Get a user by ID**
  - Endpoint: `/users/{user_id}`
  - Method: GET
  - Response: User

- **Update a user**
  - Endpoint: `/users/{user_id}`
  - Method: PUT
  - Request body: UserBase
  - Response: User

- **Delete a user**
  - Endpoint: `/users/{user_id}`
  - Method: DELETE
  - Response: `{'detail': 'User deleted'}`

### Products

- **Create a product**
  - Endpoint: `/products/create/`
  - Method: POST
  - Request body: ProductCreate
  - Response: Product

- **Get all products**
  - Endpoint: `/products/`
  - Method: GET
  - Response: List of Product

- **Get a product by ID**
  - Endpoint: `/products/{product_id}`
  - Method: GET
  - Response: Product

- **Update a product**
  - Endpoint: `/products/{product_id}`
  - Method: PUT
  - Request body: ProductBase
  - Response: Product

- **Delete a product**
  - Endpoint: `/products/{product_id}`
  - Method: DELETE
  - Response: `{'detail': 'Product deleted'}`

### Orders

- **Create an order**
  - Endpoint: `/orders/create/`
  - Method: POST
  - Request body: OrderCreate
  - Response: Order

- **Get all orders**
  - Endpoint: `/orders/`
  - Method: GET
  - Response: List of Order

- **Get an order by ID**
  - Endpoint: `/orders/{order_id}`
  - Method: GET
  - Response: Order
Этот блок кода содержит полное описание вашего проекта FastAPI CRUD Application в формате Markdown, готовый для вставки в файл README.md