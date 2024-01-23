import os
import requests
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import os
import telegram
from telegram.ext import Updater, CommandHandler

# Set your Google Drive API credentials file path
credentials_file = '/path/to/your/credentials.json'

# Set your Google Drive folder ID
folder_id = 'your_folder_id'

# Set your Telegram bot token
bot_token = 'your_bot_token'

# Create a Google Drive service
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = service_account.Credentials.from_service_account_file(credentials_file)
drive_service = build('drive', 'v3', credentials=credentials)

# Define the Telegram bot command handlers
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Send me a file and I will upload it to your Google Drive.')

def upload_file(update, context):
    file = context.bot.get_file(update.message.document.file_id)
    file.download('temp_file')
    file_name = update.message.document.file_name

    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = drive_service.media_file(filepath='temp_file', mimetype='application/octet-stream')
    drive_service.files().create(body=file_metadata, media_body=media).execute()

    os.remove('temp_file')
    context.bot.send_message(chat_id=update.effective_chat.id, text='File uploaded successfully!')

# Create the Telegram bot
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Add the command handlers
start_handler = CommandHandler('start', start)
upload_handler = telegram.ext.MessageHandler(telegram.ext.Filters.document, upload_file)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(upload_handler)

# Start the bot
updater.start_polling()
updater.idle()
