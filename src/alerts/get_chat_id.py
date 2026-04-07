import requests

BOT_TOKEN = "8686732940:AAFDhujTjZToY9bLz69aEsSsANLauQYBKSk"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
response = requests.get(url, timeout=30)

print(response.json())