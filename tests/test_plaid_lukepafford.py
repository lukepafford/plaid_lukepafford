from plaid_lukepafford import __version__
from plaid_lukepafford.transactions import all_transactions_since
from unittest.mock import patch


def test_version():
    assert __version__ == "0.1.0"


# This test doesn't actually ensure the loop works properly because
# I would really have to call get_chase_transactions
# I'm not sure what should be done in situations like this, other than
# literally running the real call every time in an integration test
# @patch("plaid_lukepafford.transactions.get_chase_transactions")
# def test_all_transactions_since(get_chase_transactions):
#    results = dict(
#        transactions=[{"date": "2020-01-01"}, {"date": "2020-01-05"}],
#        total_transactions=2,
#    )
#    get_chase_transactions.return_value = results
#
#    transactions = all_transactions_since("2020-01-06", count=1)
#    assert len(transactions["transactions"]) == 2
