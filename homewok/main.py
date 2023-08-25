# Нужные библиотеки:
# pip install fastapi
# pip install uvicorn
# pip install sqlalchemy
# pip install databases
# pip install pydantic


from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from databases import Database
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
metadata = declarative_base()

app = FastAPI()

class UserDB(metadata):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

class ProductDB(metadata):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: int

class OrderDB(metadata):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order_date = Column(String)
    status = Column(String)

class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    order_date: str
    status: str




async def create_user(user: User):
    query = UserDB.insert().values(first_name=user.first_name, last_name=user.last_name, email=user.email, password=user.password)
    return await database.execute(query)

async def read_users():
    query = UserDB.select()
    return await database.fetch_all(query)

async def read_user(user_id: int):
    query = UserDB.select().where(UserDB.c.id == user_id)
    return await database.fetch_one(query)

async def update_user(user_id: int, user: User):
    query = UserDB.update().where(UserDB.c.id == user_id).values(first_name=user.first_name, last_name=user.last_name, email=user.email, password=user.password)
    return await database.execute(query)

async def delete_user(user_id: int):
    query = UserDB.delete().where(UserDB.c.id == user_id)
    return await database.execute(query)

async def create_product(product: Product):
    query = ProductDB.insert().values(name=product.name, description=product.description, price=product.price)
    return await database.execute(query)

async def read_products():
    query = ProductDB.select()
    return await database.fetch_all(query)

async def read_product(product_id: int):
    query = ProductDB.select().where(ProductDB.c.id == product_id)
    return await database.fetch_one(query)

async def update_product(product_id: int, product: Product):
    query = ProductDB.update().where(ProductDB.c.id == product_id).values(name=product.name, description=product.description, price=product.price)
    return await database.execute(query)

async def delete_product(product_id: int):
    query = ProductDB.delete().where(ProductDB.c.id == product_id)
    return await database.execute(query)

async def create_order(order: Order):
    query = OrderDB.insert().values(user_id=order.user_id, product_id=order.product_id, order_date=order.order_date, status=order.status)
    return await database.execute(query)

async def read_orders():
    query = OrderDB.select()
    return await database.fetch_all(query)

async def read_order(order_id: int):
    query = OrderDB.select().where(OrderDB.c.id == order_id)
    return await database.fetch_one(query)

async def update_order(order_id: int, order: Order):
    query = OrderDB.update().where(OrderDB.c.id == order_id).values(user_id=order.user_id, product_id=order.product_id, order_date=order.order_date, status=order.status)
    return await database.execute(query)

async def delete_order(order_id: int):
    query = OrderDB.delete().where(OrderDB.c.id == order_id)
    return await database.execute(query)




@app.post("/users/", response_model=User)
async def create_user_route(user: User):
    user_id = await create_user(user)
    return {**user.dict(), "id": user_id}

@app.get("/users/", response_model=list[User])
async def read_users_route():
    return await read_users()

@app.get("/users/{user_id}/", response_model=User)
async def read_user_route(user_id: int):
    user = await read_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}/", response_model=User)
async def update_user_route(user_id: int, user: User):
    existing_user = await read_user(user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await update_user(user_id, user)
    return {**user.dict(), "id": user_id}

@app.delete("/users/{user_id}/", response_model=User)
async def delete_user_route(user_id: int):
    existing_user = await read_user(user_id)
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await delete_user(user_id)
    return existing_user

@app.post("/products/", response_model=Product)
async def create_product_route(product: Product):
    product_id = await create_product(product)
    return {**product.dict(), "id": product_id}

@app.get("/products/", response_model=list[Product])
async def read_products_route():
    return await read_products()

@app.get("/products/{product_id}/", response_model=Product)
async def read_product_route(product_id: int):
    product = await read_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}/", response_model=Product)
async def update_product_route(product_id: int, product: Product):
    existing_product = await read_product(product_id)
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await update_product(product_id, product)
    return {**product.dict(), "id": product_id}

@app.delete("/products/{product_id}/", response_model=Product)
async def delete_product_route(product_id: int):
    existing_product = await read_product(product_id)
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await delete_product(product_id)
    return existing_product

@app.post("/orders/", response_model=Order)
async def create_order_route(order: Order):
    order_id = await create_order(order)
    return {**order.dict(), "id": order_id}

@app.get("/orders/", response_model=list[Order])
async def read_orders_route():
    return await read_orders()

@app.get("/orders/{order_id}/", response_model=Order)
async def read_order_route(order_id: int):
    order = await read_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}/", response_model=Order)
async def update_order_route(order_id: int, order: Order):
    existing_order = await read_order(order_id)
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    await update_order(order_id, order)
    return {**order.dict(), "id": order_id}

@app.delete("/orders/{order_id}/", response_model=Order)
async def delete_order_route(order_id: int):
    existing_order = await read_order(order_id)
    if existing_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    await delete_order(order_id)
    return existing_order

