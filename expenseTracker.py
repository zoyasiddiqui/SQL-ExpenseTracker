import sqlite3
from datetime import date

def create_connection(file):
    """Create a database connection to file"""

    connection = None
    try:
        connection = sqlite3.connect(file)
    except Exception as e:
        print(e)
    return connection

def create_table(connection):
    """Create a table called name"""

    try:
        cur = connection.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS Expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        );
        """
        cur.execute(sql)
    except Exception as e:
        print(e)

def add_expense(connection, category, amount, description):
    """Add a new expense to the expense table"""

    try:
        sql = ''' INSERT INTO Expenses(category, amount, date, description)
                VALUES(?,?,?,?) '''
        cur = connection.cursor()
        cur.execute(sql, (category, amount, date.today(), description))
        connection.commit()
        return cur.lastrowid
    except Exception as e:
        print(e)
        return None

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

def print_category_summary(connection):
    """Prints a summary of expenses grouped by category with total spent, average spending, and transaction count."""
    try:
        sql = '''
        SELECT
            category,
            SUM(amount) AS Total_Spent,
            AVG(amount) AS Average_Spending,
            COUNT(id) AS Number_of_Transactions
        FROM
            Expenses
        GROUP BY
            category
        ORDER BY
            Total_Spent DESC;
        '''
        cur = connection.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        print("Category Summary:")
        for row in rows:
            print(f"Category: {row[0]}, Total Spent: ${row[1]:.2f}, Average Spending: ${row[2]:.2f}, Transactions: {row[3]}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    database = "ExpenseTracker.db"
    cat_list = []

    #create the database and get the list of categories
    conn = create_connection(database)
    if conn != None:
        create_table(conn)
        cat_list = update_categories(conn)

    #input handling
    options = """Would you like to...
    See table : A
    Add new entry : B
    Delete entry : C
    See your stats : D
    Exit : E"""

    while True:
        print(options)
        choice = input("Enter your choice: ")

        if not choice:
            print("Not valid input. Try again.")
            pass
        
        elif choice == "A":
            print_results(conn)

        elif choice == "B":
            print("Enter an expense.")
            category = input("Category: ")
            amount = float(input("Amount: "))
            description = input("Description: ")

            if not category or not amount or not description or type(amount) is not float:
                print("Error processing entry. Invalid input.")
                pass
            else:
                add_expense(conn, category, amount, description)
                cat_list = update_categories(conn) # updating list of all categories

        elif choice == "C":
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

        elif choice == "D":
            print_category_summary(conn)
        
        elif choice == "E":
            print("Happy tracking!")
            break
    
        
