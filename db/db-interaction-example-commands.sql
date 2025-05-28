-- Connect to the container with `docker exec -it timescaledb psql -U postgres -d klines`

-- Example SQL commands for TimescaleDB/PostgreSQL
-- List all klines
SELECT * FROM klines LIMIT 10;

-- Insert a new kline (replace values as needed)
INSERT INTO klines (symbol, interval, open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume)
VALUES ('BTCUSDT', '1m', '2024-05-28T00:00:00Z', 68000, 68100, 67900, 68050, 10.5, '2024-05-28T00:01:00Z', 715000, 120, 5.2, 355000)
ON CONFLICT (symbol, interval, open_time) DO NOTHING;

-- Count klines per symbol
SELECT symbol, COUNT(*) FROM klines GROUP BY symbol;

-- Delete klines for a specific symbol
DELETE FROM klines WHERE symbol = 'BTCUSDT';

-- Drop the klines table (DANGEROUS: deletes all data)
-- DROP TABLE klines;

-- Show hypertables (TimescaleDB)
\dt+ 
SELECT * FROM timescaledb_information.hypertables;

-- Show table structure
\d+ klines;
