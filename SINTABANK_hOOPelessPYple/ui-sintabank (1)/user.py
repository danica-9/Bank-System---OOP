from abc import ABC, abstractmethod

class User(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def birthdate(self):
        pass

    @property
    @abstractmethod
    def age(self):
        pass

    @property
    @abstractmethod
    def occupation(self):
        pass

    @property
    @abstractmethod
    def monthly_income(self):
        pass

    @property
    @abstractmethod
    def username(self):
        pass

    @property
    @abstractmethod
    def password(self):
        pass

    @property
    @abstractmethod
    def show_details(self):
        pass

    @property
    @abstractmethod
    def show_attributes(self):
        pass

    @property
    @abstractmethod
    def request_loan(self, amount):
        pass