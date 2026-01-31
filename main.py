from pymongo import ReturnDocument
from fastapi import FastAPI, HTTPException, Query
from bson import ObjectId
from typing import List


from database import product_collection
from schemas import ProductCreate, ProductResponse, ProductUpdate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Ecommerce Inventory API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "stock": product["stock"],
        "category": product["category"],
        "description": product.get("description", ""),
        "discount": product.get("discount", 0),
        "color": product.get("color", "N/A"),
    }


@app.get("/")
def home():
    return {"status": "API is running"}



@app.post("/products", response_model=ProductResponse)
def add_product(product: ProductCreate):
    new_product = product_collection.insert_one(product.dict())
    created = product_collection.find_one({"_id": new_product.inserted_id})
    return product_helper(created)



@app.get("/products", response_model=List[ProductResponse])
def list_products():
    products = []
    for product in product_collection.find():
        products.append(product_helper(product))
    return products



@app.get("/products/search", response_model=List[ProductResponse])
def search_product(name: str):
    products = []
    query = {"name": {"$regex": name, "$options": "i"}}
    for product in product_collection.find(query):
        products.append(product_helper(product))
    return products



@app.put("/products/{id}", response_model=ProductResponse)
def update_product(id: str, data: ProductUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    updated = product_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,  
    )

    if updated:
        return product_helper(updated)

    raise HTTPException(status_code=404, detail="Product not found")



@app.delete("/products/{id}")
def delete_product(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = product_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "Product removed successfully"}
    raise HTTPException(status_code=404, detail="Product not found")
