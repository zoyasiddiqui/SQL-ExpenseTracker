import sqlite3
from datetime import date

def create_connection(file):
    """create a database connection to file"""

    connection = None
    try:
        connection = sqlite3.connect(file)
    except Exception as e:
        print(e)
    return connection

def create_table(connection):
    """create a table"""

    try:
        cur = connection.cursor()
        # NOT NULL ensures that a column cannot have a null value
        cur.execute("""
        CREATE TABLE IF NOT EXISTS Expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        );
        """)
    except Exception as e:
        print(e)

def add_expense(connection, category, amount, description):
    """add a new expense to the expense table"""

    sql = ''' INSERT INTO Expenses(category, amount, date, description)
              VALUES(?,?,?,?) '''
    cur = connection.cursor()
    cur.execute(sql, (category, amount, date.now(), description))
    connection.commit()
    return cur.lastrowid

if __name__ == "__main__":
    database = "ExpenseTracker.db"

    #create the database
    conn = create_connection(database)
    if conn != None:
        create_table(conn)

    while True:
        pass
        # if input is not valid: pass
        # if input, stripped and put into all lowercase, is done, then exit
        
