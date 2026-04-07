from src.utils.db import get_connection


def save_price_event(symbol: str, price: float, event_time, source: str) -> None:
    query = """
        INSERT INTO crypto_prices (symbol, price, event_time, source)
        VALUES (%s, %s, %s, %s)
    """

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (symbol, price, event_time, source))
        conn.commit()
    finally:
        conn.close()


def save_alert_event(
    symbol: str,
    current_price: float,
    rolling_avg: float,
    drop_pct: float,
    alert_time,
) -> None:
    query = """
        INSERT INTO crypto_alerts (
            symbol,
            current_price,
            rolling_avg,
            drop_pct,
            alert_time
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                (symbol, current_price, rolling_avg, drop_pct, alert_time),
            )
        conn.commit()
    finally:
        conn.close()