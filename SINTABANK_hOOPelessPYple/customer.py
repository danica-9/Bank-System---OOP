from user import User

class Customer(User):
    def __init__(self, name, birthdate, age, occupation, monthly_income, balance):
        self._name = name
        self._birthdate = birthdate
        self._age = age
        self._occupation = occupation
        self._monthly_income = monthly_income
        self._balance = balance

    @property
    def name(self):
        return self._name

    @property
    def birthdate(self):
        return self._birthdate

    @property
    def age(self):
        return self._age

    @property
    def occupation(self):
        return self._occupation

    @property
    def monthly_income(self):
        return self._monthly_income

    @property
    def username(self):
        return None

    @property
    def password(self):
        return None

    def show_details(self):
        return f"Account Holder: {self.name}, Balance: {self._balance}"

    def show_attributes(self):
        return f"Name: {self.name}, Birthdate: {self.birthdate}, Age: {self.age}, Occupation: {self.occupation}, Monthly Income: {self.monthly_income}, Balance: {self._balance}"

    def request_loan(self, amount):
        return f"Loan request for P{amount} by {self.name} has been submitted."

    def deposit(self, amount):
        self._balance += amount
        return f"Deposit successful. New balance: {self._balance}"

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
            return f"Withdrawal successful. New balance: {self._balance}"
        else:
            return "Insufficient balance."