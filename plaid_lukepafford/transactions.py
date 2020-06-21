import datetime
import json
import pandas as pd
from plaid import Client
from plaid_lukepafford import CLIENT_ID, SECRET, PUBLIC_KEY, ENV, CHASE_TOKEN
from functools import partial
from plaid_lukepafford import PLAID_CACHE
from pathlib import Path


class ChaseTransactions:
    def __init__(self, cache: Path = PLAID_CACHE, **kwargs) -> None:
        """
        cache: File to read/write transaction data from
        kwargs:
            CLIENT_ID
            SECRET
            PUBLIC_KEY
            ENV
            CHASE_TOKEN
        """
        self._CLIENT_ID = kwargs.get("CLIENT_ID", CLIENT_ID)
        self._SECRET = kwargs.get("SECRET", SECRET)
        self._PUBLIC_KEY = kwargs.get("PUBLIC_KEY", PUBLIC_KEY)
        self._ENV = kwargs.get("ENV", ENV)
        self._CHASE_TOKEN = kwargs.get("CHASE_TOKEN", CHASE_TOKEN)

        self._client = Client(
            self._CLIENT_ID, self._SECRET, self._PUBLIC_KEY, self._ENV
        )
        self._end_date = datetime.date.today().isoformat()
        self._get_chase_transactions = partial(
            self._client.Transactions.get, self._CHASE_TOKEN
        )

        self.cache = cache
        self._read()

    @staticmethod
    def latest_date(transactions: list) -> str:
        """
        Returns the date of the latest transaction in list of transactions
        """
        return sorted(transactions, key=lambda x: x["date"])[-1]["date"]

    def _read(self) -> None:
        # Read existing cache if it exists
        try:
            with open(self.cache, "r") as f:
                self.transactions = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # Very early year before any records are tracked
            self.start_date = "2000-01-01"

            # initialize an empty transaction dictionary
            self.transactions = {"transactions": []}
        else:
            # Retrieve the latest date data has been received
            self.start_date = ChaseTransactions.latest_date(
                self.transactions["transactions"]
            )

    def _all_transactions_since(self, count: int = 500) -> dict:
        """
        Fetches all transactions since the latest start date in the
        existing cache
        """
        transactions = list()

        while True:
            results = self._get_chase_transactions(
                self.start_date, self._end_date, count=count, offset=len(transactions)
            )
            transactions += results["transactions"]
            if len(transactions) >= results["total_transactions"]:
                break
        results["transactions"] = transactions
        return results

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(self.transactions["transactions"])
        df.category = df.category.str.join(", ")
        df.date = pd.to_datetime(df.date)
        return df

    def merge_transactions(self) -> None:
        """
        Performs network IO to fetch latest transactions
        and append them to current cache
        """

        # Discard possibly stale results of todays data if
        # this call runs more than once a day
        if self.start_date == self._end_date:
            self.transactions["transactions"] = [
                t
                for t in self.transactions["transactions"]
                if t["date"] != self._end_date
            ]

        transactions = self._all_transactions_since()
        transactions["transactions"] += self.transactions["transactions"]

        self.transactions = transactions
        self.start_date = ChaseTransactions.latest_date(
            self.transactions["transactions"]
        )
        self._write()

    def _write(self) -> None:
        self.cache.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache, "w") as f:
            json.dump(self.transactions, f)
