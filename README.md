
# 🛒 Ecommerce Inventory Management API

A simple **Ecommerce Inventory Management System** built using **FastAPI** and **MongoDB**.  
This project allows you to **add, view, search, update, and delete products** using REST APIs, with MongoDB as the backend database.

---

## 📌 Features

- ✅ MongoDB connection with environment variables
- ✅ Add new products
- ✅ List all products
- ✅ Search products by name (case-insensitive)
- ✅ Update product details or stock
- ✅ Delete products
- ✅ Data validation using Pydantic schemas
- ✅ Clean project structure

---

## 🧱 Project Structure

```

project/
│
├── main.py              # FastAPI application & API routes
├── database.py          # MongoDB connection & CLI product insert
├── schemas.py           # Pydantic models (schemas)
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
└── README.md            # Project documentation

````

---

## ⚙️ Technologies Used

- **Python 3.10+**
- **FastAPI**
- **MongoDB**
- **PyMongo**
- **Pydantic**
- **python-dotenv**
- **Uvicorn**

---

## 🔐 Environment Variables (`.env`)

Create a `.env` file in your project root:

```env
MONGO_uri=mongodb+srv://<username>:<password>@cluster.mongodb.net/
DATABASE_NAME=InventoryDB
````

---

## 🗄️ Database Configuration

MongoDB connection is handled in `database.py`.

* Loads environment variables
* Creates MongoDB client
* Selects database & `products` collection
* Includes a connection test (`ping`)

📄 Source: `database.py` 

---

## 🧩 Database Functions (database.py)

### 🔹 Test Database Connection

```python
def test_db():
    client.admin.command("ping")
```

Checks whether MongoDB is connected successfully.

---

### 🔹 Add Products from Terminal (CLI)

```python
def add_products_from_user():
```

Allows manual product entry using terminal input:

* Product Name
* Price
* Stock
* Category
* Description
  Type `exit` to stop.

---

## 🧠 Data Models (schemas.py)

All schemas are defined using **Pydantic**.

📄 Source: `schemas.py` 

### 🔹 ProductBase

Used as a base model:

```python
name: str
price: float
stock: int
category: str
description: Optional[str]
```

---

### 🔹 ProductCreate

Used when creating a new product.

---

### 🔹 ProductUpdate

Used for partial updates (PUT):

```python
Optional fields only
```

---

### 🔹 ProductResponse

Used for API responses:

```python
id: str
```

---

## 🚀 FastAPI Application (main.py)

📄 Source: `main.py` 

### 🔹 API Title

```python
FastAPI(title="Ecommerce Inventory API")
```

---

## 🌐 API Endpoints

### 🏠 Home

```http
GET /
```

Response:

```json
{
  "status": "API is running"
}
```

---

### ➕ Add Product

```http
POST /products
```

Request Body:

```json
{
  "name": "Keyboard",
  "price": 1500,
  "stock": 10,
  "category": "Electronics",
  "description": "Mechanical keyboard"
}
```

---

### 📄 List All Products

```http
GET /products
```

Returns a list of all products.

---

### 🔍 Search Product by Name

```http
GET /products/search?name=key
```

* Case-insensitive search using regex

---

### ✏️ Update Product

```http
PUT /products/{id}
```

Example Body:

```json
{
  "price": 1800,
  "stock": 20
}
```

---

### ❌ Delete Product

```http
DELETE /products/{id}
```

Deletes a product by MongoDB ObjectId.

---

## ▶️ How to Run the Project

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Run FastAPI Server

```bash
uvicorn main:app --reload
```

### 3️⃣ Open API Docs

```
http://127.0.0.1:8000/docs
```

(Swagger UI)

---

## 🧪 Optional: Run CLI Product Entry

```bash
python database.py
```

---

## 📌 Future Improvements

* 🔐 Authentication (JWT)
* 📊 Pagination
* 🧾 Order management
* 🖼️ Product images
* 🛍️ User roles (Admin/User)

---

## 👨‍💻 Author

**Subrata Pal**
B.Tech ECE | Python & Backend Enthusiast
📍 West Bengal, India

---

## ⭐ If you like this project

Give it a ⭐ 

---

