from testproject.bank import loan
from testproject.main import open_account



def test_loan_is_valid():

    new_account = open_account("Bas", 2500)
    new_loan = new_account.get_loan(100)

    assert new_loan.is_valid()


def test_invalid_loan():

    new_account = open_account("Bas", 2500)
    new_loan = new_account.get_loan(10000)

    assert not new_loan.is_valid()

