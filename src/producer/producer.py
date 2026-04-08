import time
from config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, PRICE_SOURCE
from kafka import KafkaProducer
import json
from src.producer.price_source import get_real_price, get_mock_price
from src.utils.logger import get_logger

logger = get_logger('producer')

def create_producer() -> KafkaProducer:
    """
    Создаем продюсер, который отправляет сообщение в топик уже в JSON-формате
    """

    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def generate_price() -> list[dict]:
    if PRICE_SOURCE == 'real':
        btc_event = get_real_price('BTSUSDT')
        eth_event = get_real_price("ETHUSDT")
    else:
        btc_event = get_mock_price('BTSUSDT')
        eth_event = get_mock_price("ETHUSDT")

    return [btc_event, eth_event]


def main() -> None:
    producer = create_producer() #создаем продюсер
    try:
        while True:
            events = generate_price()
            for event in events:
                producer.send(KAFKA_TOPIC, event)
                logger.info(f"Sent event: {event}")

            producer.flush()
            time.sleep(5)

    except KeyboardInterrupt:
        pass

    finally:
        producer.close()

if __name__ == '__main__':
    main()