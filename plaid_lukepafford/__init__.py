import os
import platform
from pathlib import Path

__version__ = "0.1.0"

try:
    CLIENT_ID = os.environ["PLAID_CLIENT_ID"]
    SECRET = os.environ["PLAID_SECRET"]
    PUBLIC_KEY = os.environ["PLAID_PUBLIC_KEY"]
    ENV = os.environ["PLAID_ENV"]
    CHASE_TOKEN = os.environ["CHASE_ACCESS_TOKEN"]
except KeyError:
    msg = "The following environment variables must be defined: "
    msg += "CLIENT_ID, SECRET, PUBLIC_KEY, ENV, CHASE_TOKEN"
    raise EnvironmentError(msg)

is_windows = any(platform.win32_ver())
if is_windows:
    PLAID_CACHE = (
        Path(os.getenv("APPDATA")) / "lukepafford" / "plaid" / "transactions.json"
    )
else:
    PLAID_CACHE = (
        Path.home() / ".local" / "share" / "lukepafford" / "plaid" / "transactions.json"
    )
