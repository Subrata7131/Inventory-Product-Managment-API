import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# .env ফাইল থেকে ভেরিয়েবল লোড করা
load_dotenv()

# MONGO_uri এবং DATABASE_NAME লোড করা
MONGO_uri = os.getenv("MONGO_uri")
DB_NAME = os.getenv("DATABASE_NAME", "InventoryDB")

# কানেকশন তৈরি করা
client = MongoClient(MONGO_uri, server_api=ServerApi("1"))

# ডাটাবেস এবং কালেকশন অবজেক্ট তৈরি
db = client[DB_NAME]
product_collection = db["products"]


# ১. কানেকশন টেস্ট করার ফাংশন (এটি মিসিং ছিল)
def test_db():
    try:
        client.admin.command("ping")
        print("✅ Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")


# ২. ইউজার ইনপুট দিয়ে প্রোডাক্ট যোগ করার ফাংশন
def add_products_from_user():
    print("\n--- 🛒 Ecommerce Inventory Data Entry ---")

    while True:
        try:
            name = input("Product Name (and plese 'exit' ): ")
            if name.lower() == "exit":
                break

            price = float(input("Enter Price: "))
            stock = int(input("Enter Stock Quantity: "))
            category = input("Enter Category: ")
            description = input("Enter Description: ")

            new_product = {
                "name": name,
                "price": price,
                "stock": stock,
                "category": category,
                "description": description,
            }

            # ডাটাবেসে ইনসার্ট করা
            result = product_collection.insert_one(new_product)
            print(f"✅ Sucessful add! (ID: {result.inserted_id})\n")

        except ValueError:
            print("❌ wrong input please write correct input\n")


# প্রোগ্রামটি রান করার অংশ
if __name__ == "__main__":
    test_db()  # এখন আর এরর আসবে না
    add_products_from_user()
