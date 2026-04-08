# Crypto Alerts Streaming Pipeline

Streaming data pipeline для мониторинга криптовалют в реальном времени с алертами и дашбордом.

---

## Описание

Проект реализует потоковую обработку данных о ценах криптовалют:

- данные поступают через API / mock
- отправляются в Kafka
- обрабатываются consumer'ом (pandas, rolling window)
- сохраняются в PostgreSQL
- при аномалиях отправляются алерты в Telegram
- визуализируются в Superset

---

## Архитектура
```text
Producer → Kafka → Consumer → PostgreSQL → Superset
                         ↘ Telegram
```

---

---

## Технологии

- Python 3.12
- Apache Kafka
- pandas
- PostgreSQL
- Docker & Docker Compose
- Telegram Bot API
- Apache Superset

---

## Логика пайплайна

### 1. Producer
- получает цены криптовалют (mock или API)
- отправляет события в Kafka (JSON)

### 2. Consumer
- читает события из Kafka
- хранит последние 5 минут данных
- считает:
  - rolling average
  - процент изменения цены

### 3. Alerting
- если цена падает более чем на 3%
- отправляется сообщение в Telegram

### 4. Storage
- все события → `crypto_prices`
- алерты → `crypto_alerts`

### 5. Visualization
- Superset дашборд:
  - динамика цен
  - количество алертов
  - таблица событий

---

## Структура базы данных

### crypto_prices

| поле | описание |
|------|---------|
| symbol | тикер (BTC, ETH) |
| price | цена |
| event_time | время события |
| source | источник |

### crypto_alerts

| поле | описание |
|------|---------|
| symbol | тикер |
| current_price | текущая цена |
| rolling_avg | средняя цена |
| drop_pct | процент падения |
| alert_time | время алерта |

---

## 📊 Дашборд

В Superset реализовано:

-  График цен (BTC, ETH)
-  Таблица алертов
-  Количество алертов по символам

<img width="1634" height="822" alt="Снимок экрана 2026-04-08 в 12 40 22" src="https://github.com/user-attachments/assets/c42acf34-8496-4a8c-87a5-323f93e1b7fa" />

---

##  Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/your-username/crypto-alerts-pipeline.git
cd crypto-alerts-pipeline
```

### 2. Настроить .env
```env
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5438
POSTGRES_DB=crypto_db
POSTGRES_USER=crypto_user
POSTGRES_PASSWORD=crypto_pass

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=crypto_prices

BOT_TOKEN=your_token
CHAT_ID=your_chat_id

PRICE_SOURCE=mock

```

### 3. Запустить инфраструктуру
```bash
docker compose up -d
```
### 4. Инициализировать БД
```bash
python -m src.utils.init_db
```

### Пример
<img width="1306" height="1050" alt="Снимок экрана 2026-04-08 в 12 54 41" src="https://github.com/user-attachments/assets/d4073d13-0b46-4742-aa0a-410108bd8d94" />

