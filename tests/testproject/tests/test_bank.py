from testproject import main
from testproject.bank import bank
from testproject.main import open_account


class TestBank():

    def _setup(self):
        main.BANK = bank.Bank()


    def test_opening_account(self):
        self._setup()

        new_account = open_account("Bas", 2500)

        assert new_account.name == "Bas"
        assert new_account.balance == 2500


    def test_closing_account(self):
        self._setup()

        new_account = open_account("Bas", 2500)

        assert main.BANK.report_amount_of_open_accounts() == 1

        main.BANK.close_account(new_account.account_number)

        assert main.BANK.report_amount_of_open_accounts() == 0

