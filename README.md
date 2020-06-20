# plaid_lukepafford

Uses Plaid to instantiate a Chase connection and save transaction data
locally.

Graphs and summaries will be built that I find interesting.

# Install

```
# Install package
pip install plaid_lukepafford

# Fetch transactions from Plaid API. (This will fail if you don't provide correct environment variables)
chase-plaid fetch-latest-transactions

# Display a table summarizing results
chase-plaid money-spent-on-food
```
