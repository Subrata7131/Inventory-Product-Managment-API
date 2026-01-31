from bson import ObjectId
from pymongo import ReturnDocument
from rich.console import Console
from rich.table import Table

from database import product_collection, test_db
from schemas import ProductCreate

console = Console()


def add_product():
    console.print("\n[bold green]➕ Add Product[/bold green]")
    name = input("Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    category = input("Category: ")
    description = input("Description: ")

    product = ProductCreate(
        name=name,
        price=price,
        stock=stock,
        category=category,
        description=description,
    )

    result = product_collection.insert_one(product.dict())
    console.print(f"✅ Product added | ID: {result.inserted_id}")


def update_product():
    console.print("\n[bold yellow]✏️ Update Product[/bold yellow]")
    pid = input("Enter Product ID: ")

    if not ObjectId.is_valid(pid):
        console.print("❌ Invalid ID")
        return

    print("Leave blank if not change")

    name = input("New Name: ")
    price = input("New Price: ")
    stock = input("New Stock: ")
    discount = input("New Discount (%): ")
    category = input("New Category: ")

    update_data = {}

    if name:
        update_data["name"] = name
    if price:
        update_data["price"] = float(price)
    if stock:
        update_data["stock"] = int(stock)
    if discount:
        update_data["discount"] = int(discount)
    if category:
        update_data["category"] = category

    if not update_data:
        console.print("⚠️ Nothing to update")
        return

    updated = product_collection.find_one_and_update(
        {"_id": ObjectId(pid)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )

    if updated:
        console.print("✅ Product updated")
    else:
        console.print("❌ Product not found")


def list_products():
    table = Table(title="📦 Product List")

    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Price")
    table.add_column("Discount")
    table.add_column("Final Price")
    table.add_column("Stock")
    table.add_column("Category")

    for p in product_collection.find():
        discount = p.get("discount", 0)  # 1️⃣ discount
        discount_text = f"{discount}%" if discount > 0 else "—"  # 2️⃣ text

        final_price = p["price"] - (p["price"] * discount // 100)  # 3️⃣ final price

        table.add_row(
            str(p["_id"]),
            p["name"],
            f"{p['price']:.2f}",  
            discount_text,
            f"{final_price:.2f}",
            str(p["stock"]),
            p["category"],
        )

    console.print(table)


def search_product():
    name = input("Search name: ")

    table = Table(title="🔍 Search Result")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Price")

    for p in product_collection.find({"name": {"$regex": name, "$options": "i"}}):
        table.add_row(str(p["_id"]), p["name"], str(p["price"]))

    console.print(table)


def delete_product():
    console.print("\n[bold red]🗑️ Delete Product[/bold red]")
    pid = input("Enter Product ID: ")

    if not ObjectId.is_valid(pid):
        console.print("❌ Invalid ID")
        return

    result = product_collection.delete_one({"_id": ObjectId(pid)})
    if result.deleted_count == 1:
        console.print("✅ Product deleted")
    else:
        console.print("❌ Product not found")


def menu():
    console.print("\n[bold cyan]====================================[/bold cyan]")
    console.print("[bold cyan] 🛒 E-Commerce Inventory CLI[/bold cyan]")
    console.print("[bold cyan]====================================[/bold cyan]")
    print("1️⃣  Add Product")
    print("2️⃣  Update Product")
    print("3️⃣  List Products")
    print("4️⃣  Search Product")
    print("5️⃣  Delete Product")
    print("0️⃣  Exit")
    print("------------------------------------")


def main():
    test_db()

    while True:
        menu()
        choice = input("👉 Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            list_products()
        elif choice == "4":
            search_product()
        elif choice == "5":
            delete_product()
        elif choice == "0":
            console.print("👋 Bye Bye")
            break
        else:
            console.print("❌ Invalid choice")


if __name__ == "__main__":
    main()

