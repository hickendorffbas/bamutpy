
class Loan():

    def __init__(self, account, amount):
        self.account = account
        self.amount = amount

    def is_valid(self):
        basis = self.account.balance / 5
        basis = basis + 10
        return basis > self.amount

