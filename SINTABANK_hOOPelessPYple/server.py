import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 10000))
server.listen()

def handle_connection(c):
    try:
        c.send("Username: ".encode())
        username = c.recv(1024).decode().strip()
        print(f"Received username: {username}")

        c.send("Password: ".encode())
        password = c.recv(1024).decode().strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(f"Received hashed password: {hashed_password}")

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM userdata WHERE username = ?", (username,))
        row = cur.fetchone()

        if row:
            stored_hashed_password = row[2]  # Assuming password hash is in the third column
            if hashed_password == stored_hashed_password:
                response = f"Login Successful! You are logged in as a user."
                print(response)
                c.send(response.encode())
            else:
                response = "Login Failed! Incorrect password."
                print(response)
                c.send(response.encode())
        else:
            response = "Login Failed! User not found."
            print(response)
            c.send(response.encode())

    except Exception as e:
        print(f"Exception occurred: {e}")

    finally:
        conn.close()
        c.close()
