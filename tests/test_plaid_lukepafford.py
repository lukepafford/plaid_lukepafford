from plaid_lukepafford import __version__
from plaid_lukepafford.transactions import ChaseTransactions
import pytest
import json
import pandas as pd


def test_version():
    assert __version__ == "0.1.0"


@pytest.fixture
def empty_cache(tmp_path):
    return ChaseTransactions(tmp_path / "empty.json")


@pytest.fixture
def fake_cache(tmp_path):
    transactions = dict(
        transactions=[
            {"date": "2020-01-01", "category": "test"},
            {"date": "2020-01-05", "category": "test2"},
        ],
        total_transactions=2,
    )

    path = tmp_path / "test.json"
    path.write_text(json.dumps(transactions))
    return ChaseTransactions(path)


def test_no_cache(empty_cache):
    assert hasattr(empty_cache, "start_date")
    # Arbitrary early date that will include all Data that Plaid
    # has saved
    assert empty_cache.start_date == "2000-01-01"

    # There should be no transactions
    assert not empty_cache.transactions["transactions"]


def test_cache(fake_cache):
    assert (
        ChaseTransactions.latest_date(fake_cache.transactions["transactions"])
        == "2020-01-05"
    )


def test_dataframe_is_parsed_from_dict(fake_cache):
    df = fake_cache.to_dataframe()
    assert isinstance(df, pd.core.frame.DataFrame)


def test_cache_write(empty_cache):
    empty_cache.transactions["transactions"].append(
        {"date": "2020-01-10", "category": "test"}
    )
    empty_cache.total_transactions = 1
    empty_cache._write()
    empty_cache._read()
    assert len(empty_cache.transactions["transactions"]) == 1


def test_transactions_since(fake_cache):
    pass


def test_merge_latest_transactions(fake_cache):
    pass
