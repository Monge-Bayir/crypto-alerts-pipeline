import os
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "crypto_prices")
KAFKA_CONSUMER_GROUP = os.getenv("KAFKA_CONSUMER_GROUP", "crypto-consumer-group")

ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", "-3"))

PRICE_SOURCE = os.getenv("PRICE_SOURCE", "mock")
BINANCE_API_URL = os.getenv('BINANCE_API_URL', 'https://api.binance.com/api/v3/ticker/price')