import typer
from plaid_lukepafford.transactions import ChaseTransactions

app = typer.Typer()


@app.command()
def fetch_latest_transactions():
    transactions = ChaseTransactions()
    transactions.merge_transactions()


if __name__ == "__main__":
    app()
