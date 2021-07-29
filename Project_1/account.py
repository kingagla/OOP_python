import time
import datetime


class BankAccount:
    bank_tz = datetime.timezone.utc
    interest_rate = 0.005
    acc_numbers = []

    def __init__(self, account_number, first_name, last_name):
        if account_number in self.acc_numbers:
            raise ValueError("Account number must be UNIQUE! Please provide other number!")
        self._account_number = account_number
        self.acc_numbers.append(account_number)
        self._set_owner(first_name, last_name)
        self.acc_tz = datetime.timezone(datetime.timedelta(seconds=time.altzone * -1))

    def _get_owner(self):
        return self._owner

    def _set_owner(self, first_name, last_name):
        if isinstance(first_name, str) and isinstance(last_name, str):
            self._owner = first_name + " " + last_name
        else:
            raise ValueError("first_name and last_name should be string!")
        return self._owner

    owner = property(_get_owner, _set_owner)

    @property
    def account_number(self):
        return self._account_number

