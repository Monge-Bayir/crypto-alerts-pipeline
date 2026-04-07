import random
import datetime
import requests
from config.settings import BINANCE_API_URL
from src.utils.logger import get_logger


def get_mock_price(symbol: str) -> dict:
    fake_price = random.uniform(-2000, 2000)
    return {
        "symbol": symbol,
        'price': 65000 + fake_price,
        'event_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source': 'mock_source'
    }


def get_real_price(symbol: str) -> dict:
    logger = get_logger('get_real_price')

    response = requests.get(
        url=BINANCE_API_URL,
        params={'symbol': symbol},
        timeout=10
    )
    response.raise_for_status()

    data = response.json()

    event = {
        'symbol': data['symbol'],
        'price': float(data['price']),
        'event_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source': 'binance_api'
    }

    logger.info(f'Fetched real price: {event}')

    return event
