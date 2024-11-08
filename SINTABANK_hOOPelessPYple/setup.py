import sqlite3
import hashlib

def create_database():
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS userdata")
    cur.execute("DROP TABLE IF EXISTS tellers")
    cur.execute("DROP TABLE IF EXISTS managers")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        birthdate DATE NOT NULL,
        age INTEGER NOT NULL,
        occupation VARCHAR(255) NOT NULL,
        monthly_income REAL NOT NULL,
        balance REAL NOT NULL,
        loan_amount REAL NOT NULL DEFAULT 0,
        pin VARCHAR(6) NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'inactive',  -- Added status column
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tellers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS managers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    users = [
        ("kingpogi", hashlib.sha256("123456".encode()).hexdigest(), "King Joseph Castillo", "2000-06-16", 24,
         "Programmer", 50000.0, 1500.0, 0.0, hashlib.sha256("123456".encode()).hexdigest(), "active"),
        ("inubebe", hashlib.sha256("091124".encode()).hexdigest(), "Danica Lopez", "2001-09-11", 19, "Designer", 45000.0,
         2000.0, 0.0, hashlib.sha256("567890".encode()).hexdigest(), "active"),
        ("cochibebe", hashlib.sha256("cochicute".encode()).hexdigest(), "Sotnem Ekoc", "1995-05-15", 25, "Manager",
         55000.0, 2500.0, 0.0, hashlib.sha256("901243".encode()).hexdigest(), "inactive"),
        ("chrizwow", hashlib.sha256("mitch26".encode()).hexdigest(), "Jhon Chriz Seda", "2005-03-20", 19, "Analyst",
         60000.0, 3000.0, 0.0, hashlib.sha256("345621".encode()).hexdigest(), "inactive")
    ]

    tellers = [
        ("tellmewhy", hashlib.sha256("iwantit".encode()).hexdigest(), "Teller John"),
        ("tell2211", hashlib.sha256("110226".encode()).hexdigest(), "Teller Kath")
    ]

    managers = [
        ("143mng", hashlib.sha256("anoba".encode()).hexdigest(), "Manager Austin"),
        ("0909mng", hashlib.sha256("wow33".encode()).hexdigest(), "Manager Bebe")
    ]

    cur.executemany("INSERT INTO userdata (username, password, name, birthdate, age, occupation, monthly_income, balance, loan_amount, pin, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", users)
    cur.executemany("INSERT INTO tellers (username, password, name) VALUES (?, ?, ?)", tellers)
    cur.executemany("INSERT INTO managers (username, password, name) VALUES (?, ?, ?)", managers)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()