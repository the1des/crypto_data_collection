from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
from unicorn_fy.unicorn_fy import UnicornFy
import time
from client.database import Database

db = Database()
binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
binance_websocket_api_manager.create_stream(['kline_1m'], ['btcusdt', 'btceur'])
while True:
    if binance_websocket_api_manager.is_manager_stopping():
        print("Binance Websocket Terminated!")
        exit(0)
    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()
    if oldest_stream_data_from_stream_buffer is False:
        time.sleep(0.01)
    else:
        oldest_stream_data_from_stream_buffer = UnicornFy.binance_com_websocket(oldest_stream_data_from_stream_buffer)
        if oldest_stream_data_from_stream_buffer is not None:
            try:
                if oldest_stream_data_from_stream_buffer['event_time'] >= \
                        oldest_stream_data_from_stream_buffer['kline']['kline_close_time']:
                    pair = oldest_stream_data_from_stream_buffer['symbol']
                    ohlc = oldest_stream_data_from_stream_buffer['kline']
                    db.store_binance(pair, ohlc)
            except KeyError:
                pass
