import sqlite3
from teller import Teller

class Manager(Teller):
    def __init__(self, bank):
        super().__init__(bank)
        self.__bank = bank

    def process_requests(self):
        return self.__bank.get_pending_requests()

    def approve_request(self, user):
        approved_user = self._bank.approve_request(user)
        return f"Account for {approved_user.name} is approved.\nDetails: {approved_user.show_attributes()}"

    def process_loans(self):
        loan_requests = self._bank.get_pending_loans()
        if loan_requests:
            for loan_request in loan_requests:
                user = loan_request["user"]
                amount = loan_request["amount"]
                print(f"Loan Request Details:")
                print(f"User Information:\n{user.show_attributes()}")
                print(f"Requested Loan Amount: P{amount}")
                approve = input(f"Approve loan for {user.name} for P{amount}? (yes/no): ").lower()
                if approve == "yes":
                    approved_loan = self._bank.approve_loan_by_manager(loan_request)
                    print(f"Loan of P{approved_loan['amount']} for {approved_loan['user'].name} is approved and sent to teller for finalization.")
                else:
                    print(f"Loan request for {user.name} has been denied.")
        else:
            print("No pending loan requests.")

    def activate_account(self, user_id):
        try:
            conn = sqlite3.connect("userdata.db")
            cur = conn.cursor()
            cur.execute("UPDATE userdata SET status = 'active' WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return f"Account with ID {user_id} is activated."
        except sqlite3.Error as e:
            return f"Failed to activate account with ID {user_id}. Error: {str(e)}"

    def manage_accounts(self):
        while True:
            print("\nAccount Management:")
            print("1. Deactivate an account")
            print("2. Activate an account")
            print("3. Exit")

            choice = input("Enter your option (1-3): ")

            if choice == "1":
                user_id = input("Enter the user ID to deactivate: ")
                result = self.__bank.deactivate_account(user_id)
                print(result)
            elif choice == "2":
                user_id = input("Enter the user ID to activate: ")
                result = self.__bank.activate_account(user_id)
                print(result)
            elif choice == "3":
                break
            else:
                print("Invalid option, please choose again.")