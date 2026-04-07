from kafka import KafkaConsumer
import json


def create_costumer() -> KafkaConsumer:
    return KafkaConsumer(
        'crypto_prices',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='crypto_consumer_group',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

def main() -> None:
    costumer = create_costumer()
    print('Costumer ждет message')

    try:
        for message in costumer:
            event = message.value

            print('Получено event:')
            print(f"Валюта: {event['valute']}")
            print(f"Цена: {event['price']}")
            print(f"Дата события: {event['event_loop']}")
            print('-' * 20)

    except KeyboardInterrupt:
        pass
    finally:
        costumer.close()

if __name__ == '__main__':
    main()