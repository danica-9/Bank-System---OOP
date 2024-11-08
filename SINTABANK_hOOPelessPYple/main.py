from bank import Bank
from teller import Teller
from manager import Manager
from customer import Customer
import sqlite3
import hashlib

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def user_login(role):
    try:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if role == "user":
            cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password_hash))
        elif role == "teller":
            cur.execute("SELECT * FROM tellers WHERE username = ? AND password = ?", (username, password_hash))
        elif role == "manager":
            cur.execute("SELECT * FROM managers WHERE username = ? AND password = ?", (username, password_hash))

        row = cur.fetchone()
        conn.close()

        if row:
            if role == "user":
                (id, username, password_hash, name, birthdate, age, occupation, monthly_income, balance,
                 loan_amount, pin, status, created_at) = row

                if status == "inactive":
                    print("Login failed.")
                    return None, None, None, None

                user = Customer(name, birthdate, age, occupation, monthly_income, balance)
                print(f"Login successful!")
                return user, username, name, pin
            else:
                return True, username, row[3], None
        else:
            print("Login failed. Please check your username and password.")
            return None, None, None, None

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None, None, None, None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None, None, None, None

def main():
    print("****************************************")
    print("*                                      *")
    print("*        Welcome to Sinta Bank         *")
    print("*                                      *")
    print("****************************************")

    bank = Bank()
    teller = Teller(bank)
    manager = Manager(bank)

    while True:
        print("\nWhat would you like to do?")
        print("1. User")
        print("2. Teller")
        print("3. Manager")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            print("1. Login")
            print("2. Request Account")
            action = input("Choose an option: ").lower()

            if action == "1":
                while True:
                    user, username, name, pin = user_login("user")
                    if user:
                        print(f"Welcome, {name}!")
                        while True:
                            try:
                                option = int(input(
                                    "1) See Balance\n2) Personal Details\n3) ATM\n4) Logout\nEnter your choice (1-4): "))
                                if option == 1:
                                    print(user.show_details())
                                elif option == 2:
                                    print(user.show_attributes())
                                elif option == 3:
                                    while True:
                                        atm_option = int(input(
                                            "1) Deposit\n2) Withdraw\n3) Request Loan\n4) Change Password\n5) Exit\nEnter your choice (1-5): "))
                                        if atm_option == 1:
                                            input_pin = input("Enter your pin: ").strip()
                                            input_pin_hashed = hash_pin(input_pin)
                                            if input_pin_hashed == pin.strip():
                                                amount = float(input("Enter amount to deposit (minimum P1000): "))
                                                if amount >= 1000:
                                                    print(user.deposit(amount))
                                                    try:
                                                        conn = sqlite3.connect("userdata.db")
                                                        cur = conn.cursor()
                                                        cur.execute("UPDATE userdata SET balance = ? WHERE username = ?",
                                                                    (user._balance, username))
                                                        conn.commit()
                                                        conn.close()
                                                    except sqlite3.Error as e:
                                                        print(f"Failed to update balance for {name}. Error: {str(e)}")
                                                else:
                                                    print("Minimum deposit amount is P1000.")
                                            else:
                                                print("Invalid pin.")
                                        elif atm_option == 2:
                                            input_pin = input("Enter your pin: ").strip()
                                            input_pin_hashed = hash_pin(input_pin)
                                            if input_pin_hashed == pin.strip():
                                                amount = float(input("Enter amount to withdraw (minimum P500): "))
                                                if amount >= 500:
                                                    print(user.withdraw(amount))
                                                    try:
                                                        conn = sqlite3.connect("userdata.db")
                                                        cur = conn.cursor()
                                                        cur.execute(
                                                            "UPDATE userdata SET balance = ? WHERE username = ?",
                                                            (user._balance, username))
                                                        conn.commit()
                                                        conn.close()
                                                    except sqlite3.Error as e:
                                                        print(f"Failed to update balance for {name}. Error: {str(e)}")
                                                else:
                                                    print("Minimum withdrawal amount is P500.")
                                            else:
                                                print("Invalid pin.")
                                        elif atm_option == 3:
                                            amount = float(input("Enter loan amount: "))
                                            if amount >= 4 * user.monthly_income:
                                                print(
                                                    "We do not allow a loan request that is four times above your monthly income!")
                                            else:
                                                print(bank.request_loan(user, amount))
                                                try:
                                                    conn = sqlite3.connect("userdata.db")
                                                    cur = conn.cursor()
                                                    cur.execute(
                                                        "UPDATE userdata SET balance = balance + ?, loan_amount = loan_amount + ? WHERE username = ?",
                                                        (amount, amount, username))
                                                    conn.commit()
                                                    conn.close()
                                                except sqlite3.Error as e:
                                                    print(f"Failed to update loan amount for {user.name}. Error: {str(e)}")
                                        elif atm_option == 4:
                                            new_password = input("Enter new password: ")
                                            print(bank.change_password(username, new_password))
                                        elif atm_option == 5:
                                            break
                                        else:
                                            print("Invalid option, please choose again.")
                                elif option == 4:
                                    print("Logged out successfully.")
                                    break
                                else:
                                    print("Invalid option, please choose again.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        break
                    else:
                        retry = input("Do you want to try again? (yes/no): ").lower()
                        if retry != "yes":
                            break
            elif action == "2":
                name = input("Enter your full name: ")
                birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
                age = int(input("Enter your age: "))
                occupation = input("Enter your occupation: ")
                monthly_income = float(input("Enter your monthly income: "))
                username = input("Enter a username: ")
                password = input("Enter a password: ")
                pin = input("Enter a 6-digit pin: ")
                initial_deposit = float(input("Enter initial deposit (minimum P1000): "))
                print(bank.request_account(name, birthdate, age, occupation, monthly_income, username, password, pin,
                                           initial_deposit))
            else:
                print("Invalid action, please choose again.")

        elif choice == "2":
            print("1. Login")
            action = input("Choose an option: ").lower()

            if action == "1":
                while True:
                    teller_account, username, name, _ = user_login("teller")
                    if teller_account:
                        print(f"Welcome, {name}!")
                        while True:
                            try:
                                option = int(input("1) Process account requests\n2) Process loan requests\n3) Logout\nEnter your choice (1-3): "))
                                if option == 1:
                                    requests = teller.process_requests()
                                    if requests:
                                        for user in requests:
                                            print(
                                                f"Name: {user.name}, Age: {user.age}, Occupation: {user.occupation}, Monthly Income: P{user.monthly_income}")
                                            forward = input(
                                                f"Forward request for {user.name} to manager? (yes/no): ").lower()
                                            if forward == "yes":
                                                print(teller.forward_request(user))
                                    else:
                                        print("No pending account requests.")
                                elif option == 2:
                                    teller.process_loan_requests()
                                elif option == 3:
                                    print("Logged out successfully.")
                                    break
                                else:
                                    print("Invalid option, please choose again.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        break
                    else:
                        retry = input("Do you want to try again? (yes/no): ").lower()
                        if retry != "yes":
                            break
            else:
                print("Invalid action, please choose again.")

        elif choice == "3":
            print("1. Login")
            action = input("Choose an option: ").lower()

            if action == "1":
                while True:
                    manager_account, username, name, _ = user_login("manager")
                    if manager_account:
                        print(f"Welcome, {name}!")
                        while True:
                            try:
                                option = int(input("1) Approve account requests\n2) Approve loan requests\n3) Manage Accounts\n4) Logout\nEnter your choice (1-4): "))
                                if option == 1:
                                    requests = manager.process_requests()
                                    if requests:
                                        for user in requests:
                                            print(user.show_attributes())
                                            user_id = input("Enter the user ID to activate: ")
                                            manager.activate_account(user_id)
                                    else:
                                        print("No pending requests.")
                                elif option == 2:
                                    manager.process_loans()
                                elif option == 3:
                                    manager.manage_accounts()
                                elif option == 4:
                                    print("Logged out successfully.")
                                    break
                                else:
                                    print("Invalid option, please choose again.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                        break
                    else:
                        retry = input("Do you want to try again? (yes/no): ").lower()
                        if retry != "yes":
                            break
            else:
                print("Invalid action, please choose again.")

        elif choice == "4":
            print("Thank you for using Sinta Bank. Goodbye!")
            break

        else:
            print("Invalid choice, please choose again.")

if __name__ == "__main__":
    main()
