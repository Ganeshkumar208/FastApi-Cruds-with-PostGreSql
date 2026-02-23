from fastapi import Depends, FastAPI
from models import Products
from database import session
import database_models
from database import engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers = ["*"]
)
database_models.Base.metadata.create_all(bind=engine)

@app.get("/greetUser")
def greetUser():
    return "Hello Ganesh & Gayatri"
 
products = [
    Products(id=1, name='iPhone 15 Pro', description='6.1-inch Super Retina XDR display, A17 Pro chip, Titanium design', price=999, quantity=25),
    Products(id=2, name='Samsung Galaxy S24', description='Dynamic AMOLED 2X display, 200MP camera, Snapdragon 8 Gen 3', price=899, quantity=30),
    Products(id=3, name='MacBook Pro 14"', description='M3 Pro chip, 14-inch Liquid Retina XDR display, 18GB RAM', price=1999, quantity=15),
    Products(id=4, name='iPad Air', description='10.9-inch Liquid Retina display, M1 chip, 128GB storage', price=599, quantity=40),
    Products(id=5, name='AirPods Pro', description='Active Noise Cancellation, Transparency mode, MagSafe Charging', price=249, quantity=60),
    Products(id=6, name='PlayStation 5', description='DualSense wireless controller, 825GB SSD, 4K gaming', price=499, quantity=10),
    Products(id=7, name='Xbox Series X', description='12 teraflops of processing power, 1TB SSD, 4K gaming', price=499, quantity=8),
    Products(id=8, name='Nintendo Switch', description='OLED model, 7-inch screen, 64GB storage, Joy-Con controllers', price=349, quantity=22),
    Products(id=9, name='GoPro Hero 12', description='5.3K video, 27MP photos, HyperSmooth 6.0 stabilization', price=399, quantity=18),
    Products(id=10, name='Kindle Paperwhite', description='6.8-inch display, waterproof, 8GB storage, adjustable warm light', price=139, quantity=45)
]

def get_db():
    db=session()
    try:
        yield db
    finally:    
        db.close()

def init_db():
    db = session()
    count = db.query(database_models.Products).count()
    if count == 0:
        for product in products:
            db.add(database_models.Products(**product.model_dump()))
        db.commit()

init_db()

@app.get('/products')
def getAllProducts(db:Session = Depends(get_db)):
    db_products = db.query(database_models.Products).all()
    return db_products

@app.get('/products/{id}')
def getProductById(id:int,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        return db_product
    return "Product Not Found"

@app.post('/products/add')
def addProduct(product:Products,db:Session = Depends(get_db)):
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return product

@app.delete('/products/delete/{id}')
def deleteProduct(id:int,db:Session = Depends(get_db)):
    db_products = db.query(database_models.Products).filter(database_models.Products.id == id).first()    
    if db_products:
        db.delete(db_products)
        db.commit()
        return "Product Deleted"
    return "Product Not Found"

@app.put('/products/{id}')
def updateProduct(id:int,product:Products,db:Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "No Product"