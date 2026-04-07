from datetime import timedelta
from src.alerts.telegram_alert import send_telegram_alert
from kafka import KafkaConsumer
import json
import pandas as pd

BOT_TOKEN = "8686732940:AAFDhujTjZToY9bLz69aEsSsANLauQYBKSk"
CHAT_ID = '1150571264'


def create_costumer() -> KafkaConsumer:
    return KafkaConsumer(
        'crypto_prices',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='crypto_consumer_group',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

def main() -> None:
    costumer = create_costumer()
    df = pd.DataFrame(columns=['valute', 'price', 'event_date'])
    print('Costumer ждет сообщения...')

    try:
        for message in costumer:
            event = message.value

            event_df = pd.DataFrame([event])
            event_df['event_date'] = pd.to_datetime(event_df['event_date'])

            df = pd.concat([df, event_df], ignore_index=True)
            df['price'] = df['price'].astype(float)
            df['event_date'] = pd.to_datetime(df['event_date'])

            max_date = df['event_date'].max()
            df = df[df['event_date'] >= max_date - timedelta(minutes=5)].copy()

            current_valute = event['valute']
            current_price = float(event['price'])

            valute_df = df[df['valute'] == current_valute].copy()

            if len(valute_df) >= 2:
                rolling_avg = valute_df['price'].mean()

                drop_pct = ((current_price - rolling_avg) / rolling_avg) * 100
                print(f"Symbol: {current_valute}")
                print(f"Current price: {current_price}")
                print(f"Rolling avg (5 min): {rolling_avg:.2f}")
                print(f"Drop pct: {drop_pct:.2f}%")

                if drop_pct <= -3:
                    alert_text = (f'ВНИМАНИЕ!\n ВАЛЮТА УМЕНЬШИЛАСЬ НА {round(abs(drop_pct), 2)}%')
                    send_telegram_alert(text=alert_text, bot_token=BOT_TOKEN, chat_id=CHAT_ID)
                    print('=' * 40)
                else:
                    print('-' * 40)

            else:
                print('-' * 40)

    except KeyboardInterrupt:
        pass
    finally:
        costumer.close()


if __name__ == '__main__':
    main()