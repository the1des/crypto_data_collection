from decouple import config
import datetime as dt
import logging
import psycopg2

class Database:
    def __init__(self):
        self.connect()

    def connect(self):
        self.db = psycopg2.connect(
            host = config('DB_HOST'),
            user = config('DB_USERNAME'),
            password = config('DB_PASSWORD'),
            dbname = config('DB_DATABASE')
        )
        self.cursor = self.db.cursor()

    def check(self):
        if not self.db or self.db.closed != 0:
            self.connect()

    def exists(self, table, timestamp):
        sql = "SELECT EXISTS(SELECT 1 FROM " + table + " WHERE time = %s)"
        try:
            self.check()
            self.cursor.execute(sql, (timestamp.strftime('%Y-%m-%d %H:%M:%S'),))
            return self.cursor.fetchone()[0]
        except (Exception, psycopg2.Error) as e:
            print("Postgres Exception: " + str(e))

    def store_binance(self, pair, ohlc):
        table = config('DB_BINANCE_' + pair + '_TABLE')
        timestamp = dt.datetime.utcfromtimestamp(ohlc['kline_start_time']/1000)
        if (self.exists(table, timestamp)):
            return;
        if (not self.exists(table, timestamp - dt.timedelta(minutes=1))):
            print("Missing OHLC data occurred for Binance " + pair
            + " " + (timestamp - dt.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'))

        sql = "INSERT INTO " + table + " (time, open, high, low, close," \
        " volume, quote_asset_volume, number_of_trades," \
        " taker_buy_base_asset_volume, taker_buy_quote_asset_volume)" \
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (timestamp.strftime('%Y-%m-%d %H:%M:%S'), ohlc['open_price'],
                ohlc['high_price'], ohlc['low_price'], ohlc['close_price'],
                ohlc['base_volume'], ohlc['quote'], ohlc['number_of_trades'],
                ohlc['taker_by_base_asset_volume'],
                ohlc['taker_by_quote_asset_volume'])
        try:
            self.check()
            self.cursor.execute(sql, val)
            self.db.commit()
        except (Exception, psycopg2.Error) as e:
            ohlc_logger = logging.getLogger(pair)
            filename = 'binance_'+pair+'.csv'
            filename = filename.lower()
            ohlc_handler = logging.FileHandler(filename)
            ohlc_handler.setLevel(logging.CRITICAL)
            ohlc_logger.addHandler(ohlc_handler)
            ohlc_logger.critical('%s - %s - %s - %s - %s - %s - %s - %s - %s - %s - %s', pair,
                    timestamp.strftime('%Y-%m-%d %H:%M:%S'), ohlc['open_price'],
                    ohlc['high_price'], ohlc['low_price'], ohlc['close_price'],
                    ohlc['base_volume'], ohlc['quote'], ohlc['number_of_trades'],
                    ohlc['taker_by_base_asset_volume'],
                    ohlc['taker_by_quote_asset_volume'])
            print("Postgres Exception: " + str(e))

    def store_kraken(self, pair, ohlc):
        table = config('DB_KRAKEN_' + pair + '_TABLE')
        timestamp = ohlc[9]
        if (self.exists(table, timestamp)):
            return;
        if (not self.exists(table, timestamp - dt.timedelta(minutes=1))):
            print("Missing OHLC data occurred for Kraken " + pair
            + " " + (timestamp - dt.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S'))

        sql = "INSERT INTO " + table + " (time, open, high, low, close, vwap, volume, count)" \
        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (timestamp.strftime('%Y-%m-%d %H:%M:%S'), ohlc[2], ohlc[3],
                ohlc[4], ohlc[5], ohlc[6], ohlc[7], ohlc[8])
        try:
            self.check()
            self.cursor.execute(sql, val)
            self.db.commit()
        except (Exception, psycopg2.Error) as e:
            ohlc_logger = logging.getLogger(pair)
            filename = 'kraken_'+pair+'.csv'
            filename = filename.replace('XBT/', 'btc').lower()
            ohlc_handler = logging.FileHandler(filename)
            ohlc_handler.setLevel(logging.CRITICAL)
            ohlc_logger.addHandler(ohlc_handler)
            ohlc_logger.critical('%s - %s - %s - %s - %s - %s - %s - %s - %s', pair,
                    timestamp.strftime('%Y-%m-%d %H:%M:%S'), ohlc[2],
                    ohlc[3], ohlc[4], ohlc[5], ohlc[6],
                    ohlc[7], ohlc[8])
            print("Postgres Exception: " + str(e))
