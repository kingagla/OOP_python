import time
import datetime


class BankAccount:
    bank_tz = datetime.timezone.utc
    interest_rate = 0.005
    acc_numbers = []

    def __init__(self, account_number, first_name, last_name, initial_deposit=None):
        if account_number in self.acc_numbers:
            raise ValueError("Account number must be UNIQUE! Please provide other number!")
        self._account_number = account_number
        self.acc_numbers.append(account_number)
        self._balance = 0
        self._set_owner(first_name, last_name)
        self.acc_tz = datetime.timezone(datetime.timedelta(seconds=time.altzone * -1))
        self.history = []
        if initial_deposit:
            self.transaction('deposit', initial_deposit)

    def _get_owner(self):
        return self._owner

    def _set_owner(self, owner):
        try:
            first_name, last_name = owner
            self._owner = first_name + " " + last_name
            return self._owner
        except ValueError:
            raise ValueError("Account owner should be given as tuple (first_name, last_name)")

    owner = property(_get_owner, _set_owner)

    @property
    def account_number(self):
        return self._account_number

    @property
    def balance(self):
        return self._balance

    def _generate_confirmation_number(self, transaction_type):
        return f'{transaction_type}-{self.account_number}-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'

    def transaction(self, type_, amount):
        if not (isinstance(amount, (float, int)) and amount > 0):
            raise ValueError('Transaction amount must be positive value')
        if type_ == 'deposit':
            self.balance += amount
            transaction_type = 'D'
        elif type_ == 'withdrawals':
            if self.balance < amount:
                transaction_type = 'X'
            else:
                self.balance -= amount
                transaction_type = 'W'
        return self._generate_confirmation_number(transaction_type)

    def interest_deposit(self):
        self.balance *= (1+self.interest_rate)
        return self._generate_confirmation_number('I')