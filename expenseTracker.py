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
    cur.execute(sql, (category, amount, date.today(), description))
    connection.commit()
    return cur.lastrowid

def print_results(connection):
    """print all of the entries in the Expenses table"""

    sql = ''' SELECT * FROM Expenses '''
    cur = connection.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for r in rows:
        print(r)

def get_all_by_category(connection, category):
    """print all entries in some category"""

    sql = ''' SELECT * FROM Expenses where CATEGORY = ? '''
    cur = connection.cursor()
    cur.execute(sql, (category,))
    rows = cur.fetchall()
    for r in rows:
        print(r)

def delete_by_id(connection, id):
    """delete entry by ID"""
    
    sql = ''' DELETE FROM Expenses WHERE id = ?'''
    cur = connection.cursor()
    cur.execute(sql, (id,))
    connection.commit()

def update_categories(connection):
    """ update the categories """

    cur = connection.cursor()
    cur.execute("SELECT DISTINCT category FROM Expenses")
    temp_cats = cur.fetchall()
    categories = []
    for c in temp_cats:
        categories.append(c[0])
    
    return categories

if __name__ == "__main__":
    database = "ExpenseTracker.db"
    cat_list = []

    #create the database and get the list of categories
    conn = create_connection(database)
    if conn != None:
        create_table(conn)
        cat_list = update_categories(conn)

    #input handling
    while True:
        isDone = input("Are you done? Y/N ... ")
        if isDone == "Y":
            break

        enterOrDelete = input("Would you like to enter or delete an entry? E/D ... ")
        if enterOrDelete == "E":
            print("Enter an expense.")
            category = input("Category: ")
            amount = float(input("Amount: "))
            description = input("Description: ")
            if not category or not amount or not description or type(amount) is not float:
                print("Error processing entry. Invalid input.")
                pass
            else:
                add_expense(conn, category, amount, description)
                cat_list = update_categories(conn)

        elif enterOrDelete == "D":
            category = input("What category would you like to delete from? ")
            if not category or category not in cat_list:
                print("Invalid category.")
                pass
            else:
                get_all_by_category(conn, category)

                to_delete = int(input("Enter the ID of the entry to delete: "))
                if not to_delete or type(to_delete) is not int:
                    print("Invalid ID.")
                    pass
                else:
                    delete_by_id(conn, to_delete)

        else:
            print("Invalid input.")
            pass

    print("Your Expenses Currently: ")
    print_results(conn)
    
        
