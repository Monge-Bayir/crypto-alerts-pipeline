from telegram_alert import send_telegram_alert

BOT_TOKEN = "8686732940:AAFDhujTjZToY9bLz69aEsSsANLauQYBKSk"
CHAT_ID = '1150571264'

send_telegram_alert(
    bot_token=BOT_TOKEN,
    chat_id=CHAT_ID,
    text='Здарова брат'
)
