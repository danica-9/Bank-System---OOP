import sqlite3
import hashlib
from customer import Customer

class Bank:
    def __init__(self):
        self.__pending_requests = []
        self.__users = {}
        self.__pending_loans = []
        self.__approved_loans = []

    def request_account(self, name, birthdate, age, occupation, monthly_income, username, password, pin,
                        initial_deposit):
        if initial_deposit < 1000:
            return "The account should have at least P1000."
        user = Customer(name, birthdate, age, occupation, monthly_income, initial_deposit)
        self.__pending_requests.append(user)

        try:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            pin_hash = hashlib.sha256(pin.encode()).hexdigest()
            cur.execute(
                "INSERT INTO userdata (username, password, pin, name, birthdate, age, occupation, monthly_income, balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (username, password_hash, pin_hash, name, birthdate, age, occupation, monthly_income, initial_deposit))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return f"Failed to create account for {name}. Error: {str(e)}"

        return f"Account request for {name} is submitted to teller."

    def get_pending_requests(self):
        return self.__pending_requests

    def approve_request(self, user):
        approved_user = self.__bank.approve_request(user)
        try:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("UPDATE userdata SET status = 'active' WHERE username = ?", (user.username,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return f"Failed to update status for {user.name}. Error: {str(e)}"
        return f"Account for {approved_user.name} is approved.\nDetails: {approved_user.show_attributes()}"

    def get_user(self, name):
        return self.__users.get(name)

    def get_approved_users(self):
        return self.__users

    def request_loan(self, user, amount):
        loan_request = {"user": user, "amount": amount, "approved_by_manager": False}
        self.__pending_loans.append(loan_request)
        return f"Loan request for P{amount} by {user.name} has been submitted to the manager."

    def get_pending_loans(self):
        return self.__pending_loans

    def approve_loan_by_manager(self, loan_request):
        loan_request["approved_by_manager"] = True
        self.__pending_loans.remove(loan_request)
        self.__approved_loans.append(loan_request)
        return loan_request

    def get_approved_loans(self):
        return self.__approved_loans

    def finalize_loan_by_teller(self, loan_request):
        user = loan_request["user"]
        amount = loan_request["amount"]
        user.deposit(amount)
        self.__approved_loans.remove(loan_request)
        try:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("UPDATE userdata SET balance = ? WHERE username = ?", (user._balance, user.name))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return f"Failed to update balance for {user.name}. Error: {str(e)}"
        return f"Loan of P{amount} has been added to {user.name}'s balance. Current balance is P{user._balance}."

    def change_password(self, username, new_password):
        try:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            cur.execute("UPDATE userdata SET password = ? WHERE username = ?", (new_password_hash, username))
            conn.commit()
            conn.close()
            return "Password changed successfully."
        except sqlite3.Error as e:
            return f"Failed to change password. Error: {str(e)}"

    def deactivate_account(self, user_id):
        try:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("UPDATE userdata SET status = 'inactive' WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return f"Account with ID {user_id} has been deactivated."
        except sqlite3.Error as e:
            return f"Failed to deactivate account with ID {user_id}. Error: {str(e)}"

    def activate_account(self, user_id):
        try:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("UPDATE userdata SET status = 'active' WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return f"Account with ID {user_id} has been activated."
        except sqlite3.Error as e:
            return f"Failed to activate account with ID {user_id}. Error: {str(e)}"