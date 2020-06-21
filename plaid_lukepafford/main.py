import typer
import matplotlib.pyplot as plt
import pandas as pd
from plaid_lukepafford.transactions import ChaseTransactions

app = typer.Typer()


@app.command()
def fetch_latest_transactions():
    transactions = ChaseTransactions()
    transactions.merge_transactions()


@app.command()
def money_spent_on_food():
    transactions = ChaseTransactions()
    df = transactions.to_dataframe()
    food_by_month = (
        df[df.category.str.contains("food|drink", case=False)]
        .groupby(pd.Grouper(key="date", freq="1M"))["amount"]
        .sum()
    )

    fig, axes = plt.subplots(2)
    food_by_month.plot.line(ax=axes[0])
    axes[0].set_title("Money spent on food per month")
    axes[0].set_ylabel("Dollars")

    food_totals = food_by_month.sort_index().cumsum()
    food_totals.plot.line(ax=axes[1])
    axes[1].set_title("Running total of food expenses")
    axes[1].set_ylabel("Dollars")
    axes[1].annotate(
        food_totals[-1], (food_totals.index[-1], food_totals[-1]), textcoords="data"
    )
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    app()
