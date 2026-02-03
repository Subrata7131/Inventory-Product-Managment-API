import os

# import certifi
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()


MONGO_uri = os.getenv("MONGO_uri")
DB_NAME = os.getenv("DATABASE_NAME", "InventoryDB")


client = MongoClient(MONGO_uri, server_api=ServerApi("1"))#,tlsCAFile=certifi.where())

db = client[DB_NAME]
product_collection = db["products"]


def test_db():
    try:
        client.admin.command("ping")
        print("✅ Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")


def add_products_from_user():
    print("\n--- 🛒 Ecommerce Inventory Data Entry ---")

    while True:
        try:
            name = input("Product Name (and plese 'exit' ): ")
            if name.lower() == "exit":
                break

            price = float(input("Enter Price: "))

            discount_input = input("Enter Discount (% , optional): ")
            if discount_input:
                try:
                    discount = float(discount_input)
                except ValueError:
                    discount = 0.0
            else:
                discount = 0.0

            stock = int(input("Enter Stock Quantity: "))
            category = input("Enter Category: ")
            description = input("Enter Description: ")

            new_product = {
                "name": name,
                "price": price,
                "discount": discount,
                "stock": stock,
                "category": category,
                "description": description,
            }

            result = product_collection.insert_one(new_product)
            print(f"✅ Sucessful add! (ID: {result.inserted_id})\n")

        except ValueError:
            print("❌ wrong input please write correct input\n")


if __name__ == "__main__":
    test_db()
    add_products_from_user()




