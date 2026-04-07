from datetime import timedelta
from src.alerts.telegram_alert import send_telegram_alert
from kafka import KafkaConsumer
import json
import pandas as pd
from config.settings import BOT_TOKEN, CHAT_ID, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_GROUP, KAFKA_TOPIC, ALERT_THRESHOLD
from src.utils.logger import get_logger


logger = get_logger('consumer')

def create_costumer() -> KafkaConsumer:
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id=KAFKA_CONSUMER_GROUP,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

def main() -> None:
    costumer = create_costumer()
    df = pd.DataFrame(columns=['symbol', 'price', 'event_date'])
    logger.info('Costumer ждет сообщения...')

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

            current_symbol = event['symbol']
            current_price = float(event['price'])

            valute_df = df[df['symbol'] == current_symbol].copy()

            if len(valute_df) >= 2:
                rolling_avg = valute_df['price'].mean()

                drop_pct = ((current_price - rolling_avg) / rolling_avg) * 100
                logger.info(
                    f"Symbol={current_symbol} | current_price={current_price} | "
                    f"rolling_avg={rolling_avg:.2f} | drop_pct={drop_pct:.2f}%"
                )

                if drop_pct <= ALERT_THRESHOLD:
                    alert_text = (
                        f"🚨 ВНИМАНИЕ!\n"
                        f"Валюта: {current_symbol}\n"
                        f"Текущая цена: {current_price}\n"
                        f"Средняя цена за 5 минут: {rolling_avg:.2f}\n"
                        f"Падение: {abs(drop_pct):.2f}%"
                    )
                    send_telegram_alert(text=alert_text, bot_token=BOT_TOKEN, chat_id=CHAT_ID)
                    logger.info(f'Валюта уменьшилась на {round(abs(drop_pct), 2)}%')

            else:
                logger.info('Еще не собрали нужное количество записей валюты')

    except KeyboardInterrupt:
        pass
    finally:
        costumer.close()


if __name__ == '__main__':
    main()