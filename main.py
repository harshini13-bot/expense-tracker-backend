from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os

conn_obj=mysql.connector.connect(
    host=os.getenv("db_host"),
    database=os.getenv("db_name"),
    user=os.getenv("db_user"),
    password=os.getenv("db_password"),
    port=os.getenv("db_port")
)
cursor_obj=conn_obj.cursor(dictionary=True)

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)

create_table_query = """
CREATE TABLE IF NOT EXISTS expenses(

    expense_id INT PRIMARY KEY AUTO_INCREMENT,

    title VARCHAR(100),

    amount INT,

    category VARCHAR(100),

    expense_date DATE

)
"""

cursor_obj.execute(create_table_query)
conn_obj.commit()

#  Add Expense 
@app.post("/add_expense")
def add_expense(new_data: dict):

    title = new_data["t"]
    amount = new_data["a"]
    category = new_data["c"]
    expense_date = new_data["d"]

    query = """
    INSERT INTO expenses(title, amount, category, expense_date)
    VALUES(%s,%s,%s,%s)
    """

    values = (title, amount, category, expense_date)

    cursor_obj.execute(query, values)
    conn_obj.commit()

    return {"msg": "Expense Added Successfully"}


#  View Expenses 
@app.get("/view_expense")
def view_expense():

    query = "SELECT * FROM expenses"
    cursor_obj.execute(query)

    data = cursor_obj.fetchall()

    return data


#  Delete Expense 
@app.delete("/delete_expense/{expense_id}")
def delete_expense(expense_id: int):

    query = "DELETE FROM expenses WHERE expense_id=%s"

    cursor_obj.execute(query, (expense_id,))
    conn_obj.commit()

    return {"msg": "Expense Deleted Successfully"}


# Update Expense 
@app.put("/update_expense/{expense_id}")
def update_expense(expense_id: int, new_data: dict):

    title = new_data["t"]
    amount = new_data["a"]
    category = new_data["c"]
    expense_date = new_data["d"]

    query = """
    UPDATE expenses
    SET title=%s, amount=%s, category=%s, expense_date=%s
    WHERE expense_id=%s
    """

    values = (
        title,
        amount,
        category,
        expense_date,
        expense_id
    )

    cursor_obj.execute(query, values)
    conn_obj.commit()

    return {"msg": "Expense Updated Successfully"}

# SEARCH EXPENSE
@app.get("/search_expense/{title}")

def search_expense(title: str):
    query = "SELECT * FROM expenses WHERE title LIKE %s"
    cursor_obj.execute(query, (f"%{title}%",))
    data = cursor_obj.fetchall()
    return data

#SORT EXPENSE
@app.get("/sort_expense/{order}")

def sort_expense(order: str):

    if order.lower() == "asc":
        query = "SELECT * FROM expenses ORDER BY amount ASC"

    elif order.lower() == "desc":
        query = "SELECT * FROM expenses ORDER BY amount DESC"

    else:
        return {"msg": "Choose asc or desc"}

    cursor_obj.execute(query)
    data = cursor_obj.fetchall()

    return data

# FILTER EXPENSE
@app.get("/filter_expense/{category}")

def filter_expense(category: str):

    query = "SELECT * FROM expenses WHERE category=%s"

    cursor_obj.execute(query, (category,))

    data = cursor_obj.fetchall()

    return data

# SPENDING ANALYSIS
@app.get("/spending_analysis")

def spending_analysis():

    query = """
    SELECT category, SUM(amount) as total
    FROM expenses
    GROUP BY category
    """
    cursor_obj.execute(query)

    data = cursor_obj.fetchall()

    return data