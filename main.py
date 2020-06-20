import typer
from plaid_lukepafford.transactions import ChaseTransactions

app = typer.Typer()


@app.command()
def fetch_latest_transactions():
    transactions = ChaseTransactions()
    transactions.merge_transactions()


@app.command()
def money_spent_on_food(top_entries: int = 10):
    transactions = ChaseTransactions()
    df = transactions.to_dataframe()
    categories = df.groupby("category")["amount"].sum()
    categories = categories[categories.index.str.contains("food|drink", case=False)]
    categories.sort_values(inplace=True)
    categories = categories.to_frame()
    categories["cumulative total"] = categories.cumsum()
    print(categories)


if __name__ == "__main__":
    app()
