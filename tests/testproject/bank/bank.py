import testproject.bank.account  #FQN to cover that in tests of the mutation tester


class Bank():

    def __init__(self):
        self._accounts = {}
        self._next_account_number = 100001

    def get_account_by_number(self, account_number):
        self._validate_account_number(account_number)
        return self._accounts[account_number]

    def new_account(self, name):
        new_account_number = self._next_account_number
        self._next_account_number += 1

        new_account = testproject.bank.account.Account(new_account_number, name)
        self._accounts[new_account_number] = new_account
        return new_account

    def report_amount_of_open_accounts(self):
        return len(self._accounts)

    def transfer(self, account1, account2, amount):
        account1.withdraw(amount)
        account2.deposit(amount)

    def close_account(self, account_number):
        self._validate_account_number(account_number)
        del self._accounts[account_number]

    def _validate_account_number(self, account_number):
        if account_number not in self._accounts:
            raise Exception(f"Account with number {account_number} does not exist")

