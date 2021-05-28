from decouple import config
import datetime as dt
from client.database import Database

MINUTES = 5 # minutes before now to check related rows in database tables
db = Database()
utcnow = dt.datetime.utcnow()
timestamp = utcnow - dt.timedelta(seconds=utcnow.second) - dt.timedelta(minutes=MINUTES)
tables = dict()
tables['Binance BTCUSDT'] = config('DB_BINANCE_BTCUSDT_TABLE')
tables['Binance BTCEUR'] = config('DB_BINANCE_BTCEUR_TABLE')
tables['Kraken XBT/USD'] = config('DB_KRAKEN_XBT/USD_TABLE')
tables['Kraken XBT/EUR'] = config('DB_KRAKEN_XBT/EUR_TABLE')
for market, table in tables.items():
    if (not db.exists(table, timestamp)):
        print(market + " websocket is probably dead! Missing OHLC data occurred for " + timestamp.strftime('%Y-%m-%d %H:%M:%S'))
