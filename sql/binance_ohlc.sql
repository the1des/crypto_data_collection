CREATE TABLE binance_btceur (
    time timestamp without time zone PRIMARY KEY,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume numeric,
    quote_asset_volume numeric,
    number_of_trades integer,
    taker_buy_base_asset_volume numeric,
    taker_buy_quote_asset_volume numeric
);
CREATE TABLE binance_btcusdt (
    time timestamp without time zone PRIMARY KEY,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    volume numeric,
    quote_asset_volume numeric,
    number_of_trades integer,
    taker_buy_base_asset_volume numeric,
    taker_buy_quote_asset_volume numeric
);
