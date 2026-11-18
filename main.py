from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config.database import engine, session_local
from models import database_model
from models.product import Product

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use this to initialize table in the database
database_model.Base.metadata.create_all(bind=engine)

# products = [
#     Product(id=1, name="Iphone X", desc="A smart phone", price=10.0, quantity=5),
#     Product(id=2, name="Iphone 11", desc="Another smart phone", price=20.0, quantity=3),
#     Product(
#         id=3, name="Iphone 12", desc="Yet another smart phone", price=30.0, quantity=8
#     ),
#     Product(
#         id=4, name="Iphone 13", desc="The latest smart phone", price=40.0, quantity=2
#     ),
# ]


# # To initialize the database with the products,
# # uncomment the following code and run the application once.
# # After that, comment it back to avoid duplicate entries in the database.
# def init_db():
#     db = session_local()

#     for product in products:
#         db.add(database_model.Product(**product.model_dump()))

#     db.commit()
#     db.close()


# init_db()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def greet():
    return "Welcome to FastAPI!"


@app.get("/products")
def get_products(db: Session = Depends(get_db)):  # noqa: B008
    db_products = db.query(database_model.Product).all()
    return db_products


@app.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):  # noqa: B008
    db_product = (
        db.query(database_model.Product).filter(database_model.Product.id == id).first()
    )
    if db_product:
        return db_product
    return {"error": "Product not found"}


@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):  # noqa: B008
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product


@app.put("/products/{id}")
def update_product(id: int, updated_product: Product, db: Session = Depends(get_db)):  # noqa: B008
    db_product = (
        db.query(database_model.Product).filter(database_model.Product.id == id).first()
    )
    if db_product:
        db_product.name = updated_product.name
        db_product.desc = updated_product.desc
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return "Product updated successfully"
    else:
        return {"error": "Product not found"}


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):  # noqa: B008
    db_product = (
        db.query(database_model.Product).filter(database_model.Product.id == id).first()
    )
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    return {"error": "Product not found"}
