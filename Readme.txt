🚀 Backend - Expense Tracker API

A FastAPI-based backend for managing expense data with MySQL database.

⚙️ Tech Stack
FastAPI (Backend Framework)
MySQL (Database)
Uvicorn (Server)
Pydantic (Validation)
📌 Features
Add new expense
View all expenses
Update expense
Delete expense
Search expense by title
Filter by category
Sort expenses
Spending analytics API
📁 Project Structure
backend/
│── main.py
│── database.py
│── models.py
│── .env
⚙️ Setup Instructions
1️⃣ Install dependencies
pip install fastapi uvicorn pymysql python-dotenv
2️⃣ Setup .env
db_host=your_host
db_port=3306
db_user=your_user
db_password=your_password
db_name=your_db
3️⃣ Run server
uvicorn main:app --reload
🔌 API Endpoints
POST /add_expense
GET /view_expense
PUT /update_expense/{id}
DELETE /delete_expense/{id}
GET /search_expense/{title}
GET /filter_expense/{category}
GET /sort_expense/{order}
GET /spending_analysis
📍 Backend runs at:
http://127.0.0.1:8000

AUTHOR
HARSHINI