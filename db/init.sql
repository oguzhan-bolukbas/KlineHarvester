CREATE TABLE IF NOT EXISTS klines (
    symbol TEXT NOT NULL,
    interval TEXT NOT NULL,
    open_time TIMESTAMPTZ NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume NUMERIC,
    close_time TIMESTAMPTZ,
    quote_asset_volume NUMERIC,
    number_of_trades INTEGER,
    taker_buy_base_asset_volume NUMERIC,
    taker_buy_quote_asset_volume NUMERIC,
    PRIMARY KEY(symbol, interval, open_time)
);

-- TimescaleDB feature: create hypertable
SELECT create_hypertable('klines', 'open_time', if_not_exists => TRUE);