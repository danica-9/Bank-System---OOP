import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from PIL import Image, ImageTk


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class BankInterface:
    background = "#06283D"
    framebg = "#EDEDED"
    framefg = "#06283D"

    def __init__(self, root):
        self.root = root
        self.root.title("SINTA Bank")
        self.root.geometry("1166x718")
        self.root.configure(bg='light gray')
        self.root.resizable(False, False)
        self.load_images()
        self.create_main_menu()
        self.__pending_loans = []
        self.__approved_loans = []

    def load_images(self):
        try:
            background_image = Image.open('background.png')
            background_image = background_image.resize((1166, 718), Image.LANCZOS)
            self.background_img = ImageTk.PhotoImage(background_image)
        except FileNotFoundError:
            messagebox.showerror("File Not Found", "Image file not found.")
            self.background_img = None

    def create_main_menu(self):
        self.clear_frame()

        if self.background_img:
            background_label = tk.Label(self.root, image=self.background_img)
            background_label.place(relwidth=1, relheight=1)

        tk.Button(self.root, text="User Login", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised", command=lambda: self.login_screen("user")).place(relx=0.5, rely=0.5,
                                                                                    anchor=tk.CENTER)
        tk.Button(self.root, text="Teller Login", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised", command=lambda: self.login_screen("teller")).place(relx=0.5, rely=0.6,
                                                                                      anchor=tk.CENTER)
        tk.Button(self.root, text="Manager Login", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised", command=lambda: self.login_screen("manager")).place(relx=0.5, rely=0.7,
                                                                                       anchor=tk.CENTER)
        tk.Button(self.root, text="Request Account", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  bd=3, relief="raised",
                  command=self.request_account).place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        tk.Button(self.root, text="Exit", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised", command=self.root.quit).place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def login_screen(self, user_type):
        self.clear_frame()
        login_frame = tk.Frame(self.root, bg="light gray")
        login_frame.pack(pady=100)

        tk.Label(login_frame, text="Username: ", bg="light gray", font=("Arial", 15, "bold")).grid(row=0, column=0,
                                                                                                   padx=20, pady=5)
        username_entry = tk.Entry(login_frame, width=20, font=("Arial", 15))
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(login_frame, text="Password: ", bg="light gray", font=("Arial", 15, "bold")).grid(row=1, column=0,
                                                                                                   padx=20, pady=5)
        password_entry = tk.Entry(login_frame, width=20, font=("Arial", 15), show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(login_frame, text="Login", width=10, fg="#FFFFFF", bg="#074592", relief="raised",
                  font=("Arial", 15, "bold"),
                  command=lambda: self.login(user_type, username_entry.get(), password_entry.get())).grid(row=2,
                                                                                                          column=0,
                                                                                                          columnspan=2,
                                                                                                          pady=20)

        tk.Button(login_frame, text="Back", width=10, fg="#FFFFFF", bg="#074592", relief="raised",
                  font=("Arial", 15, "bold"),
                  command=self.create_main_menu).grid(row=3, column=0, columnspan=2, pady=20)

    def login(self, user_type, username, password):
        hashed_password = hash_password(password)

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            if user_type == "user":
                cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
            elif user_type == "teller":
                cur.execute("SELECT * FROM tellers WHERE username = ? AND password = ?", (username, hashed_password))
            elif user_type == "manager":
                cur.execute("SELECT * FROM managers WHERE username = ? AND password = ?", (username, hashed_password))
            else:
                messagebox.showerror("Error", "Unknown user type.")
                return

            result = cur.fetchone()
            conn.close()

            if result:
                if user_type == "user":
                    (id, username, password_hash, name, birthdate, age, occupation, monthly_income, balance,
                     loan_amount, pin, status, created_at) = result

                    if status == "inactive":
                        messagebox.showerror("Error",
                                             "Account is deactivated. Request activation permission to Bank Manager.")
                        return None, None, None

                    if status == "pending":
                        messagebox.showerror("Error", "Account is still under for pending.")
                        return None, None, None

                    if status == "For approval":
                        messagebox.showerror("Error", "Account is still under for approval.")
                        return None, None, None

            if result:
                messagebox.showinfo("Success", "Login successful!")
                self.load_user_interface(user_type, result)
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}")

        finally:
            conn.close()

    def load_user_interface(self, user_type, user_data):
        if user_type == "user":
            self.load_user_menu(user_data)
        elif user_type == "teller":
            self.load_teller_menu()
        elif user_type == "manager":
            self.load_manager_menu()

    def load_user_menu(self, user_data):
        self.clear_frame()
        tk.Label(self.root, text=f"Welcome, {user_data[3]}", font=("Arial", 20, "bold"), bg="light gray").pack(pady=20)

        tk.Button(self.root, text="See Balance", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.show_balance(user_data)).pack(pady=10)
        tk.Button(self.root, text="Deposit", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.deposit(user_data)).pack(pady=10)
        tk.Button(self.root, text="Withdraw", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.withdraw(user_data)).pack(pady=10)
        tk.Button(self.root, text="Request Loan", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.request_loan(user_data)).pack(pady=10)
        tk.Button(self.root, text="Change Password", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.change_password_process(user_data)).pack(pady=10)
        tk.Button(self.root, text="Personal Details", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  bd=3, relief="raised",
                  command=lambda: self.show_personal_details(user_data)).pack(pady=10)
        tk.Button(self.root, text="Logout", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.create_main_menu).pack(pady=10)

    def load_teller_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Teller Menu", font=("Arial", 20, "bold"), bg="light gray").pack(pady=100)

        tk.Button(self.root, text="Process Account Requests", width=45, font=("Arial", 15, "bold"), fg="#FFFFFF",
                  bg="#074592", relief="raised",
                  command=self.teller_process_account_request).pack(pady=20)
        tk.Button(self.root, text="Process Loan Requests", width=45, font=("Arial", 15, "bold"), fg="#FFFFFF",
                  bg="#074592", relief="raised",
                  command=self.teller_process_loan_requests).pack(pady=20)
        tk.Button(self.root, text="Logout", width=45, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.create_main_menu).pack(pady=20)

    def load_manager_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Manager Menu", font=("Arial", 20, "bold"), bg="light gray").pack(pady=100)

        tk.Button(self.root, text="Approve Account Requests", width=45, font=("Arial", 15, "bold"), fg="#FFFFFF",
                  bg="#074592", bd=3, relief="raised",
                  command=self.manager_process_account_request).pack(pady=20)
        tk.Button(self.root, text="Approve Loan Requests", width=45, font=("Arial", 15, "bold"), fg="#FFFFFF",
                  bg="#074592", relief="raised",
                  command=self.approve_loan_requests).pack(pady=20)
        tk.Button(self.root, text="Manage Accounts", width=45, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.manage_accounts).pack(pady=20)
        tk.Button(self.root, text="Logout", width=45, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.create_main_menu).pack(pady=20)

    def request_account(self):
        self.clear_frame()

        tk.Label(self.root, text="Request Account", font=("Arial", 12, "bold"), bg="light gray").pack(pady=15)

        tk.Label(self.root, text="Username", bg="light gray", font=("Arial", 8, "bold")).pack(pady=5)
        username_entry = tk.Entry(self.root, width=30, font=("Arial", 10))
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Name", bg="light gray", font=("Arial", 8, "bold")).pack(pady=5)
        name_entry = tk.Entry(self.root, width=50, font=("Arial", 10))
        name_entry.pack(pady=5)

        tk.Label(self.root, text="Birthdate", bg="light gray", font=("Arial", 8, "bold")).pack(pady=5)
        birthdate_entry = tk.Entry(self.root, width=35, font=("Arial", 10))
        birthdate_entry.pack(pady=5)

        tk.Label(self.root, text="Age", bg="light gray", font=("Arial", 8, "bold")).pack(pady=5)
        age_entry = tk.Entry(self.root, width=35, font=("Arial", 10))
        age_entry.pack(pady=5)

        tk.Label(self.root, text="Occupation", bg="light gray", font=("Arial", 8, "bold")).pack(pady=5)
        occupation_entry = tk.Entry(self.root, width=25, font=("Arial", 10))
        occupation_entry.pack(pady=5)

        tk.Label(self.root, text="Monthly Income", bg="light gray", font=("Arial", 8, "bold")).pack(pady=5)
        income_entry = tk.Entry(self.root, width=40, font=("Arial", 10))
        income_entry.pack(pady=5)

        tk.Label(self.root, text="Password", bg="light gray", font=("Arial", 8, "bold")).pack(pady=5)
        password_entry = tk.Entry(self.root, width=45, font=("Arial", 10))
        password_entry.pack(pady=5)

        tk.Label(self.root, text="Pin", bg="light gray", font=("Arial", 8, "bold")).pack(pady=5)
        pin_entry = tk.Entry(self.root, width=25, font=("Arial", 10))
        pin_entry.pack(pady=5)

        tk.Label(self.root, text="Initial Deposit (Must be over 1,000!)", bg="light gray",
                 font=("Arial", 8, "bold")).pack(pady=5)
        initital_deposit_entry = tk.Entry(self.root, width=30, font=("Arial", 10))
        initital_deposit_entry.pack(pady=5)

        tk.Button(self.root, text="Submit Request", width=20, font=("Arial", 10, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.submit_account_request(username_entry.get(), name_entry.get(),
                                                              birthdate_entry.get(), age_entry.get(),
                                                              occupation_entry.get(), income_entry.get(),
                                                              password_entry.get(), pin_entry.get(),
                                                              int(initital_deposit_entry.get()))).pack(pady=10)

        tk.Button(self.root, text="Back", width=20, font=("Arial", 10, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.create_main_menu).pack(pady=5)

    def submit_account_request(self, username, name, birthdate, age, occupation, monthly_income, password, pin,
                               initial_deposit):
        if initial_deposit < 1000:
            return messagebox.showerror("Error",
                                        "Initital deposit must be more than 1k!")  # pop-up message of initial deposite must be more than 1000

        else:
            if not (
                    username and name and birthdate and age and occupation and monthly_income and password and pin and initial_deposit):
                messagebox.showerror("Error", "All fields are required.")
                return

            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()

            try:
                status_change = 'pending'
                cur.execute(
                    "INSERT INTO userdata (username, name, birthdate, age, occupation, monthly_income, password, pin, balance, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (username, name, birthdate, age, occupation, monthly_income, password, pin, initial_deposit,
                     status_change))
                conn.commit()
                messagebox.showinfo("Success", "Account request submitted successfully!")
                self.create_main_menu()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error accessing database: {e}")
            finally:
                conn.close()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # User Section
    def show_balance(self, user_data):
        balance = user_data[8]
        messagebox.showinfo("Balance", f"Your balance is: P{balance}")

    def deposit(self, user_data):
        self.transaction_screen(user_data, "Deposit")

    def withdraw(self, user_data):
        self.transaction_screen(user_data, "Withdraw")

    def transaction_screen(self, user_data, transaction_type):
        self.clear_frame()
        tk.Label(self.root, text=f"{transaction_type} Money", font=("Arial", 20, "bold"), bg="light gray").pack(pady=20)

        tk.Label(self.root, text="Amount", bg="light gray", font=("Arial", 15, "bold")).pack(pady=5)
        amount_entry = tk.Entry(self.root, width=30, font=("Arial", 15))
        amount_entry.pack(pady=5)

        tk.Button(self.root, text=transaction_type, width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.execute_transaction(user_data, transaction_type, amount_entry.get())).pack(
            pady=10)

        tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.load_user_menu(user_data)).pack(pady=10)

    def execute_transaction(self, user_data, transaction_type, amount):
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
            return

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("SELECT balance FROM userdata WHERE username = ?", (user_data[1],))
            balance = cur.fetchone()[0]

            if transaction_type == "Deposit":
                new_balance = balance + amount
            elif transaction_type == "Withdraw":
                if amount > balance:
                    raise ValueError("Insufficient funds.")
                new_balance = balance - amount

            cur.execute("UPDATE userdata SET balance = ? WHERE username = ?", (new_balance, user_data[1]))
            conn.commit()

            messagebox.showinfo(transaction_type, f"{transaction_type} successful! New balance: P{new_balance}")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}")
        except ValueError as e:
            messagebox.showerror("Transaction Error", f"Error: {e}")
        finally:
            conn.close()

    def change_password_process(self, user_data):
        self.clear_frame()
        tk.Label(self.root, text="Change Password", font=("Arial", 20, "bold"), bg="light gray").pack(pady=20)
        user = user_data[1]

        tk.Label(self.root, text="Enter new password", bg="light gray", font=("Arial", 15, "bold")).pack(pady=5)
        new_password_entry = tk.Entry(self.root, width=30, font=("Arial", 15))
        new_password_entry.pack(pady=5)
        tk.Button(self.root, text="Update Password", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.change_password(new_password_entry.get(), user_data[1])).pack(pady=10)
        tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.load_user_menu(user_data)).pack(pady=10)

    def request_loan(self, user_data):
        self.clear_frame()
        tk.Label(self.root, text="Request Loan", font=("Arial", 20, "bold"), bg="light gray").pack(pady=20)

        tk.Label(self.root, text="Amount", bg="light gray", font=("Arial", 15, "bold")).pack(pady=5)
        amount_entry = tk.Entry(self.root, width=30, font=("Arial", 15))
        amount_entry.pack(pady=5)

        tk.Button(self.root, text="Submit Loan Request", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF",
                  bg="#074592", relief="raised",
                  command=lambda: self.submit_loan_request(amount_entry.get(), user_data)).pack(pady=10)

        tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=lambda: self.load_user_menu(user_data)).pack(pady=10)

    def submit_loan_request(self, loan_amount_req, user_data):
        return self.user_request_loan(loan_amount_req, user_data)

    def user_request_loan(self, amount, user_data):
        loan_request = {"user": user_data[1], "amount": amount, "approved_by_manager": False}
        self.__pending_loans.append(loan_request)
        messagebox.showinfo("Success",
                            f"Loan request for P{amount} by {user_data[3]} has been submitted to the manager.")

    def show_personal_details(self, user_data):
        self.clear_frame()
        header = tk.Label(self.root, text="Personal Details", font=("Arial", 20, "bold"), bg="light gray")
        header.pack(pady=20)

        details_frame = tk.Frame(self.root, bg="light gray")
        details_frame.pack(anchor="center")

        details = [
            ("Username", user_data[1]),
            ("Name", user_data[3]),
            ("Age", user_data[5]),
            ("Occupation", user_data[6]),
            ("Monthly Income", user_data[7])
        ]

        for label, value in details:
            detail_label = tk.Label(details_frame, text=f"{label}: {value}", bg="light gray", font=("Arial", 15))
            detail_label.pack(anchor="w", padx=20, pady=5)

        back_button = tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF",
                                bg="#074592", relief="raised",
                                command=lambda: self.load_user_menu(user_data))
        back_button.pack(pady=20)

    def change_password(self, new_password, username):
        hashed_password = hash_password(new_password)
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()
        try:
            cur.execute("UPDATE userdata SET password = ? WHERE username = ?", (hashed_password, username))
            conn.commit()
            messagebox.showinfo("Success", "Account password has been updated.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}")
        finally:
            conn.close()

    # Teller Section
    def teller_process_account_request(self):
        self.clear_frame()
        tk.Label(self.root, text="Process Account Requests", font=("Arial", 20, "bold"), bg="light gray").pack(pady=20)

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM userdata WHERE status = 'pending'")
            requests = cur.fetchall()

            if not requests:
                tk.Label(self.root, text="No pending account requests.", bg="light gray", font=("Arial", 15)).pack(
                    pady=10)
            else:
                for request in requests:
                    details = f"""
                    Username: {request[1]}
                    Name: {request[2]}
                    Age: {request[3]}
                    Occupation: {request[4]}
                    Monthly Income: {request[5]}
                    """

                    tk.Label(self.root, text=details, bg="light gray", font=("Arial", 15)).pack(pady=10)
                    tk.Button(self.root, text="Forward", width=10, font=("Arial", 15, "bold"), fg="#FFFFFF",
                              bg="#074592", relief="raised",
                              command=lambda r=request: self.teller_approve_account_request(r)).pack(pady=5)
                    tk.Button(self.root, text="Reject", width=10, font=("Arial", 15, "bold"), fg="#FFFFFF",
                              bg="#074592", relief="raised",
                              command=lambda r=request: self.teller_reject_account_request(r)).pack(pady=5)

        finally:
            conn.close()

        tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.load_teller_menu).pack(pady=10)

    def teller_approve_account_request(self, request):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("UPDATE userdata SET status = 'For approval' WHERE id = ?", (request[0],))
            conn.commit()
            messagebox.showinfo("Success", "Account request has been forwarded.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}")
        finally:
            conn.close()

    def teller_reject_account_request(self, request):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("UPDATE userdata SET status = 'rejected' WHERE id = ?", (request[0],))
            conn.commit()
            messagebox.showinfo("Success", "Account request rejected.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}")
        finally:
            conn.close()

    def get_pending_loans(self):
        return self.__pending_loans

    def get_approved_loans(self):
        return self.__approved_loans

    def teller_process_loan_requests(self):
        approved_loans = self.get_approved_loans()
        if approved_loans:
            for loan_request in approved_loans:
                user = loan_request["user"]
                amount = loan_request["amount"]
                messagebox.showinfo("Loading...", f"Finalizing loan for username: {user}")
                return self.finalize_loan_by_teller(user, amount), self.__approved_loans.remove(loan_request)

    def finalize_loan_by_teller(self, user, amount):
        try:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("UPDATE userdata SET balance = balance + ?, loan_amount = loan_amount + ? WHERE username = ?",
                        (amount, amount, user))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            return messagebox.showinfo("Error", f"Failed to update balance for {user}. Error: {str(e)}")
        return messagebox.showinfo("Success", f"Loan of P{amount} has been added to {user}'s balance.")

    # Manager Section
    def manage_accounts(self):
        self.clear_frame()
        tk.Label(self.root, text="Manage Accounts", font=("Arial", 20, "bold"), bg="light gray").pack(pady=20)

        tk.Button(self.root, text="Activate Accounts", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.account_activate_process).pack(pady=10)
        tk.Button(self.root, text="Deactivate Accounts", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF",
                  bg="#074592",
                  relief="raised",
                  command=self.account_deactivate_process).pack(pady=10)
        tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.load_manager_menu).pack(pady=10)

    def account_activate_process(self):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        self.clear_frame()
        try:
            cur.execute("SELECT * FROM userdata WHERE status = 'inactive'")
            inactive_accounts = cur.fetchall()

            if not inactive_accounts:
                tk.Label(self.root, text="No inactive accounts.", bg="light gray", font=("Arial", 15)).pack(
                    pady=10)
            else:
                for inactive_account in inactive_accounts:
                    details = f"""
                            Username: {inactive_account[1]}
                            Name: {inactive_account[2]}
                            Age: {inactive_account[3]}
                            Occupation: {inactive_account[4]}
                            Monthly Income: {inactive_account[5]}
                            """

                    tk.Label(self.root, text=details, bg="light gray", font=("Arial", 15)).pack(pady=10)
                    tk.Button(self.root, text="Activate", width=10, font=("Arial", 15, "bold"), fg="#FFFFFF",
                              bg="#074592", relief="raised",
                              command=lambda ic=inactive_account: self.activate_account(ic)).pack(pady=5)

        finally:
            conn.close()

        tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.manage_accounts).pack(pady=10)

    def activate_account(self, account):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("UPDATE userdata SET status = 'active' WHERE id = ?", (account[0],))
            conn.commit()
            messagebox.showinfo("Success", "Account request has been activated.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}")
        finally:
            conn.close()

    def account_deactivate_process(self):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        self.clear_frame()
        try:
            cur.execute("SELECT * FROM userdata WHERE status = 'active'")
            active_accounts = cur.fetchall()

            if not active_accounts:
                tk.Label(self.root, text="No inactive accounts.", bg="light gray", font=("Arial", 15)).pack(
                    pady=10)
            else:
                for active_account in active_accounts:
                    details = f"""
                            Username: {active_account[1]}
                            Name: {active_account[2]}
                            Age: {active_account[3]}
                            Occupation: {active_account[4]}
                            Monthly Income: {active_account[5]}
                            """

                    tk.Label(self.root, text=details, bg="light gray", font=("Arial", 15)).pack(pady=10)
                    tk.Button(self.root, text="Activate", width=10, font=("Arial", 15, "bold"), fg="#FFFFFF",
                              bg="#074592", relief="raised",
                              command=lambda ac=active_account: self.deactivate_account(ac)).pack(pady=5)

        finally:
            conn.close()
        tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.manage_accounts).pack(pady=10)

    def deactivate_account(self, account):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("UPDATE userdata SET status = 'inactive' WHERE id = ?", (account[0],))
            conn.commit()
            messagebox.showinfo("Success", "Account request has been deactivated.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}")
        finally:
            conn.close()

    def manager_process_account_request(self):
        self.clear_frame()
        tk.Label(self.root, text="Approve Account Requests", font=("Arial", 20, "bold"), bg="light gray").pack(pady=20)

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("SELECT * FROM userdata WHERE status = 'For approval'")
            requests = cur.fetchall()

            if not requests:
                tk.Label(self.root, text="No account requests for approval.", bg="light gray", font=("Arial", 15)).pack(
                    pady=10)
            else:
                for request in requests:
                    details = f"""
                    Username: {request[1]}
                    Name: {request[2]}
                    Age: {request[3]}
                    Occupation: {request[4]}
                    Monthly Income: {request[5]}
                    """

                    tk.Label(self.root, text=details, bg="light gray", font=("Arial", 15)).pack(pady=10)
                    tk.Button(self.root, text="Approve", width=10, font=("Arial", 15, "bold"), fg="#FFFFFF",
                              bg="#074592", relief="raised",
                              command=lambda r=request: self.manager_approve_account_request(r)).pack(pady=5)
                    tk.Button(self.root, text="Reject", width=10, font=("Arial", 15, "bold"), fg="#FFFFFF",
                              bg="#074592", relief="raised",
                              command=lambda r=request: self.manager_reject_account_request(r)).pack(pady=5)

        finally:
            conn.close()

        tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                  relief="raised",
                  command=self.load_manager_menu).pack(pady=10)

    def manager_approve_account_request(self, request):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("UPDATE userdata SET status = 'active' WHERE id = ?", (request[0],))
            conn.commit()
            messagebox.showinfo("Success", "Account has been approved.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}")
        finally:
            conn.close()

    def manager_reject_account_request(self, request):
        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        try:
            cur.execute("UPDATE userdata SET status = 'rejected' WHERE id = ?", (request[0],))
            conn.commit()
            messagebox.showinfo("Success", "Account for approval has been rejected.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error accessing database: {e}")
        finally:
            conn.close()

    def approve_loan_by_manager(self, loan_request):
        loan_request["approved_by_manager"] = True
        self.__pending_loans.remove(loan_request)
        self.__approved_loans.append(loan_request)
        return loan_request

    def approve_loan_requests(self):
        loan_requests = self.get_pending_loans()
        if loan_requests:
            for loan_request in loan_requests:
                user = loan_request["user"]
                amount = loan_request["amount"]
                self.clear_frame()
                tk.Label(self.root, text=f"Approve loan for {user} for P{amount}?", font=("Arial", 15, "bold"),
                         bg="light gray").pack(pady=20)
                approve_button = tk.Button(self.root, text="Approve", width=20, font=("Arial", 15, "bold"),
                                           fg="#FFFFFF", bg="#074592", relief="raised",
                                           command=lambda lr=loan_request: self.approve_loan(lr))
                approve_button.pack(pady=10)
                reject_button = tk.Button(self.root, text="Reject", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF",
                                          bg="#074592", relief="raised",
                                          command=lambda lr=loan_request: self.reject_loan(lr))
                reject_button.pack(pady=10)

                tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                          relief="raised",
                          command=self.load_manager_menu).pack(pady=10)
        else:
            self.clear_frame()
            tk.Label(self.root, text="No pending request", font=("Arial", 15, "bold"))
            tk.Button(self.root, text="Back", width=20, font=("Arial", 15, "bold"), fg="#FFFFFF", bg="#074592",
                      relief="raised",
                      command=self.load_manager_menu).pack(pady=10)

    def approve_loan(self, loan_request):
        self.approve_loan_by_manager(loan_request)
        messagebox.showinfo("Loan Approved",
                            f"Loan of P{loan_request['amount']} for {loan_request['user']} is approved and sent to teller for finalization.")

    def reject_loan(self, loan_request):
        self.__pending_loans.remove(loan_request)
        messagebox.showinfo("Loan Rejected", f"Loan request for {loan_request['user']} has been denied.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BankInterface(root)
    root.mainloop()
