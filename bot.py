import os
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Maxfiy ma'lumotlar
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")

def analyze_image(image_data):
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_KEY,
        'Content-Type': 'application/octet-stream'
    }
    response = requests.post(AZURE_ENDPOINT, headers=headers, data=image_data)
    result = response.json()
    try:
        return result["description"]["captions"][0]["text"]
    except:
        return "❌ AI tahlilda xatolik yuz berdi."

def handle_photo(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]
    photo_file = photo.get_file()
    image_data = photo_file.download_as_bytearray()
    description = analyze_image(image_data)
    update.message.reply_text(f"🧠 AI tahlil: {description}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
