from fastapi import FastAPI, HTTPException, Query
from bson import ObjectId
from typing import List

# অন্য ফাইল থেকে ইমপোর্ট করা
from database import product_collection
from schemas import ProductCreate, ProductResponse, ProductUpdate

app = FastAPI(title="Ecommerce Inventory API")


# MongoDB ডেটাকে Python ডিকশনারিতে সাজানোর জন্য হেল্পার
def product_helper(product) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "stock": product["stock"],
        "category": product["category"],
        "description": product.get("description", ""),
    }


@app.get("/")
def home():
    return {"status": "API is running"}


# ১. প্রোডাক্ট অ্যাড করা (Add Product)
@app.post("/products", response_model=ProductResponse)
def add_product(product: ProductCreate):
    new_product = product_collection.insert_one(product.dict())
    created = product_collection.find_one({"_id": new_product.inserted_id})
    return product_helper(created)


# ২. সব প্রোডাক্টের লিস্ট (List Products)
@app.get("/products", response_model=List[ProductResponse])
def list_products():
    products = []
    for product in product_collection.find():
        products.append(product_helper(product))
    return products


# ৩. নাম দিয়ে সার্চ করা (Search Product)
@app.get("/products/search", response_model=List[ProductResponse])
def search_product(name: str):
    products = []
    query = {"name": {"$regex": name, "$options": "i"}}
    for product in product_collection.find(query):
        products.append(product_helper(product))
    return products


# ৪. স্টক বা তথ্য আপডেট করা (Update Product/Stock)
@app.put("/products/{id}", response_model=ProductResponse)
def update_product(id: str, data: ProductUpdate):
    update_data = {k: v for k, v in data.dict().items() if v is not None}
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    updated = product_collection.find_one_and_update(
        {"_id": ObjectId(id)}, {"$set": update_data}, return_document=True
    )
    if updated:
        return product_helper(updated)
    raise HTTPException(status_code=404, detail="Product not found")


# ৫. প্রোডাক্ট রিমুভ করা (Remove Product)
@app.delete("/products/{id}")
def delete_product(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")

    result = product_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "Product removed successfully"}
    raise HTTPException(status_code=404, detail="Product not found")
