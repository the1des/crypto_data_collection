from kraken_wsclient_py import kraken_wsclient_py as client
import datetime as dt
import calendar
from client.database import Database

def handle_message(msg):
    global db
    global time
    global ohlc
    res = list(msg)
    if len(res) == 4 and res[2] == 'ohlc-1':
        pair = res[3]
        next_ohlc = list(res[1])
        next_time = float(next_ohlc[1])
        if pair not in time:
            time[pair] = next_time
        if time[pair] != next_time:
            #Debug Kraken when sends a time in future
            next_minute = calendar.timegm((dt.datetime.utcnow()
                + dt.timedelta(minutes=1)).timetuple())
            if next_time > next_minute:
                print("Kraken " + pair + " Websocket is fucked up! " + str(next_time))
                return
            #Check for no activity ohlc and store them also
            next_timestamp = dt.datetime.utcfromtimestamp(next_time) - dt.timedelta(minutes=1)
            timestamp = dt.datetime.utcfromtimestamp(time[pair]) - dt.timedelta(minutes=1)
            ohlc[pair].append(timestamp)
            while (timestamp != next_timestamp):
                db.store_kraken(pair, ohlc[pair])
                timestamp = timestamp + dt.timedelta(minutes=1)
                ohlc[pair][2] = ohlc[pair][5]
                ohlc[pair][3] = ohlc[pair][5]
                ohlc[pair][4] = ohlc[pair][5]
                ohlc[pair][6] = 0
                ohlc[pair][7] = 0
                ohlc[pair][8] = 0
                ohlc[pair][9] = timestamp
            time[pair] = next_time
        ohlc[pair] = next_ohlc

db = Database()
time = dict()
ohlc = dict()
my_client = client.WssClient()
my_client.start()
my_client.subscribe_public(
    subscription = {
        'name': 'ohlc', 'interval': 1
    },
    pair = ['XBT/USD', 'XBT/EUR'],
    callback = handle_message
)
