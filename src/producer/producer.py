from json import JSONDecoder

from kafka import KafkaProducer
import json
import random
import datetime


def create_producer() -> KafkaProducer:
    """
    Создаем продюсер, который отправляет сообщение в топик уже в JSON-формате
    """

    return KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def generate_fake_price(valute: str, price: float) -> dict:
    fake_price = random.uniform(-100, 100)
    return {
        'valute': valute,
        'price': round(price + fake_price, 2),
        'event_loop': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def main() -> None:
    producer = create_producer() #создаем продюсер
    try:
        while True:
            btc_event = generate_fake_price('BTC', 65000)
            producer.send('crypto_prices', btc_event) #отправляем сообщение в kafka
            producer.flush() # НЕМЕДЛЕННО отправляем ВСЕ сообщения из буфера и ЖДЁМ подтверждения

            print(f'Успешно отправилось {btc_event}')

    except KeyboardInterrupt:
        pass

    finally:
        producer.close()

if __name__ == '__main__':
    main()