from testproject.bank import bank


BANK = bank.Bank()


def open_account(name, amount):
    account = BANK.new_account(name)
    account.deposit(amount)
    return account


def pay_lottery(account_number):
    account = BANK.get_account_by_number(account_number)
    account.deposit(1000 * 1000)

