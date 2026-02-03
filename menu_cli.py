import requests
from rich.console import Console
from rich.table import Table


console = Console()


API = "http://127.0.0.1:8000"


def add_product():
    console.print("\n[bold green]➕ Add Product (Via API)[/bold green]")
    name = input("Name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    category = input("Category: ")
    description = input("Description: ")

    product = {
        "name": name,
        "price": price,
        "stock": stock,
        "category": category,
        "description": description,
    }

    try:
        response = requests.post(f"{API}/products", json=product)
        if response.status_code == 200:
            data = response.json()
            console.print(f"✅ Product added | ID: {data['id']}")
        else:
            console.print(f" Error: {response.json().get('detail')}")
    except Exception as e:
        console.print(f" Connection Failed: {e}")


def list_products():
    try:
        response = requests.get(f"{API}/products")
        if response.status_code == 200:
            products = response.json()
            table = Table(title="📦 Product List (Fetched from API)")

            table.add_column("ID")
            table.add_column("Name")
            table.add_column("Price")
            table.add_column("Discount")
            table.add_column("Stock")
            table.add_column("Category")

            for p in products:
                discount = p.get("discount", 0)
                table.add_row(
                    p["id"],
                    p["name"],
                    f"{p['price']:.2f}",
                    f"{discount}%",
                    str(p["stock"]),
                    p["category"],
                )
            console.print(table)
        else:
            console.print("❌ Could not fetch products")
    except Exception as e:
        console.print(f"❌ Error: {e}")


def update_product():
    console.print("\n[bold yellow]✏️ Update Product[/bold yellow]")
    pid = input("Enter Product ID: ")

    print("What do you want to update?")
    print("1. Name  2. Price  3. Stock  4. Category 5. discount")
    choice = input("Enter choice (e.g., 1,2): ")

    update_data = {}
    if "1" in choice:
        update_data["name"] = input("New Name: ")
    if "2" in choice:
        update_data["price"] = float(input("New Price: "))
    if "3" in choice:
        update_data["stock"] = int(input("New Stock: "))
    if "4" in choice:
        update_data["category"] = input("New Category: ")
    if "5" in choice:
        update_data["discount"] = input("New discount: ")

    if not update_data:
        console.print("⚠️ No fields selected for update")
        return

    try:
        response = requests.put(f"{API}/products/{pid}", json=update_data)
        if response.status_code == 200:
            console.print("✅ Product updated successfully")
        else:
            console.print(f"❌ Failed: {response.json().get('detail')}")
    except Exception as e:
        console.print(f"❌ Error: {e}")


def delete_product():
    console.print("\n[bold red]🗑️ Delete Product[/bold red]")
    pid = input("Enter Product ID: ")

    try:
        response = requests.delete(f"{API}/products/{pid}")
        if response.status_code == 200:
            console.print("✅ Product deleted ")
        else:
            console.print(f" Failed: {response.json().get('detail')}")
    except Exception as e:
        console.print(f" Error: {e}")


def search_product():
    name = input("Search name: ")
    try:
        response = requests.get(f"{API}/products/search", params={"name": name})
        if response.status_code == 200:
            products = response.json()
            table = Table(title="🔍 Search Result")
            table.add_column("ID")
            table.add_column("Name")
            table.add_column("Price")
            for p in products:
                table.add_row(p["id"], p["name"], str(p["price"]))
            console.print(table)
    except Exception as e:
        console.print(f"❌ Error: {e}")


def menu():
    console.print("\n[bold orange]====================================[/bold orange]")
    console.print("[bold orange] 🛒 API-Driven Inventory CLI[/bold orange]")
    console.print("[bold orange]====================================[/bold orange]")
    print("1️⃣  Add Product")
    print("2️⃣  Update Product")
    print("3️⃣  List Products")
    print("4️⃣  Search Product")
    print("5️⃣  Delete Product")
    print("0️⃣  Exit")


def main():
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
            break
        else:
            console.print("❌ Invalid choice Please Enter Valid Number")


if __name__ == "__main__":
    main()


