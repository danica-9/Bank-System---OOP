from user import User
from bank import Bank

class Teller(User):
    def __init__(self, bank):
        self._bank = bank

    @property
    def name(self):
        return None

    @property
    def birthdate(self):
        return None

    @property
    def age(self):
        return None

    @property
    def occupation(self):
        return "Teller"

    @property
    def monthly_income(self):
        return None

    @property
    def username(self):
        return None

    @property
    def password(self):
        return None

    def show_details(self):
        return None

    def show_attributes(self):
        return None

    def request_loan(self, amount):
        return None

    def process_requests(self):
        return self._bank.get_pending_requests()

    def forward_request(self, user):
        return f"Request for {user.name} is forwarded to the manager."

    def process_loan_requests(self):
        approved_loans = self._bank.get_approved_loans()
        if approved_loans:
            for loan_request in approved_loans:
                user = loan_request["user"]
                amount = loan_request["amount"]
                print(f"Finalizing loan for {user.name}:")
                result = self._bank.finalize_loan_by_teller(loan_request)
                print(result)
        else:
            print("No approved loan requests.")