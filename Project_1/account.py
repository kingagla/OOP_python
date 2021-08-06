import datetime
import time
from dateutil.tz import tzoffset


class TransactionTypeError(Exception):
    pass


class BankAccount:
    transaction_number = 0
    interest_rate = 0.005
    _acc_numbers = []

    def __init__(self, account_number, first_name, last_name, timezone=None, initial_deposit=None):
        if account_number in self._acc_numbers:
            raise ValueError("Account number must be UNIQUE! Please provide other number!")
        self._account_number = account_number
        self._acc_numbers.append(account_number)
        self._balance = 0
        self._set_owner((first_name, last_name))
        if isinstance(timezone, tzoffset):
            self.timezone = timezone
        else:
            self.timezone = datetime.timezone(datetime.timedelta(seconds=time.altzone * -1))
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
        self.transaction_number += 1
        return f'{transaction_type}-{self.account_number}-\
{datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")}-{self.transaction_number}'

    def transaction(self, transaction_type, amount):
        if not (isinstance(amount, (float, int)) and amount > 0):
            raise ValueError('Transaction amount must be positive value')
        if transaction_type == 'deposit':
            self._balance += amount
            transaction_type = 'D'
        elif transaction_type == 'withdrawal':
            if self.balance < amount:
                transaction_type = 'X'
            else:
                self._balance -= amount
                transaction_type = 'W'
        else:
            raise TransactionTypeError("Transaction type must be one of: ('deposit', 'withdrawal')")
        confirmation = self._generate_confirmation_number(transaction_type)
        self.history.append(confirmation)
        return confirmation

    def interest_deposit(self):
        self._balance *= (1 + self.interest_rate)
        confirmation = self._generate_confirmation_number('I')
        self.history.append(confirmation)
        return confirmation

    @staticmethod
    def transaction_info(transaction_id, timezone):
        class TransactionInfo:
            transaction_type, account_number, _date_utc, transaction_number = transaction_id.split('-')
            account_number = int(account_number)
            transaction_number = int(transaction_number)
            _date_utc = datetime.datetime.strptime(_date_utc, "%Y%m%d%H%M%S")
            transaction_datetime = _date_utc + timezone.utcoffset(_date_utc)
            transaction_datetime = transaction_datetime.strftime('%Y-%m-%d %H:%M:%S')

        transaction_info = TransactionInfo()
        return transaction_info

