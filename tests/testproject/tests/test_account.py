from testproject import main
from testproject.bank import bank
from testproject.main import open_account, pay_lottery


def _setup():
    main.BANK = bank.Bank()
    #TODO: this should actually test (to be added) functionality on the account object, and not involve the bank


def test_winning_the_lottery():
    _setup()

    new_account = open_account("Bas", 2500)
    pay_lottery(new_account.account_number)

    assert new_account.balance == 2500 + 1000 * 1000

