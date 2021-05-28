CREATE TABLE kraken_btceur (
    time timestamp without time zone PRIMARY KEY,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    vwap numeric,
    volume numeric,
    count integer
);
CREATE TABLE kraken_btcusd (
    time timestamp without time zone PRIMARY KEY,
    open numeric,
    high numeric,
    low numeric,
    close numeric,
    vwap numeric,
    volume numeric,
    count integer
);
