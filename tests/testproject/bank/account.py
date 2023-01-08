from testproject.bank import loan as loan_module  #"as" import to test that in the mutation tester


class Account:

    def __init__(self, account_number, name):
        self.name = name
        self.account_number = account_number
        self.balance = 0
        self._loans = set()

    def deposit(self, amount):
        self.balance += amount

    def withdrawal(self, amount):
        self.balance -= amount

    def get_spendable_amount(self):
        spendable = self.balance
        for loan in self._loans:
            spendable += loan.amount

        return spendable

    def get_loan(self, amount):
        loan = loan_module.Loan(self, amount)
        self._loans.add(loan)
        return loan

