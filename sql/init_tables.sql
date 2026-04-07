CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    price NUMERIC(18, 8) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crypto_alerts (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    current_price NUMERIC(18, 8) NOT NULL,
    rolling_avg NUMERIC(18, 8) NOT NULL,
    drop_pct NUMERIC(10, 4) NOT NULL,
    alert_time TIMESTAMP NOT NULL
);