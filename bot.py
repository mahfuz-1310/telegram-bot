import os
import random
import threading
from flask import Flask
import telebot

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
CHAT_ID = '8382172425'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

first_names = [
    'Aryan',
    'Tanvir',
    'Rahim',
    'Sakib',
    'Fahim',
    'Nayeem',
    'Sadia',
    'Anika',
    'Tasfia',
    'Noshin',
]
last_names = [
    'Ahmed',
    'Hossain',
    'Chowdhury',
    'Islam',
    'Khan',
    'Rahman',
    'Uddin',
    'Talukder',
]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.reply_to(
      message,
      'Welcome! Name Generator Bot-e apnake shagotom.\nName pete `/generate`'
      ' command din.',
  )


@bot.message_handler(commands=['generate'])
def generate_name(message):
  name = f'{random.choice(first_names)} {random.choice(last_names)}'
  bot.reply_to(message, f'Apnar generated name: {name}')


@app.route('/')
def home():
  return 'Telegram Bot is running smoothly!'


def run_bot():
  bot.infinity_polling()


if __name__ == '__main__':
  # Bot ke alada thread-e chalanor jonno
  t = threading.Thread(target=run_bot)
  t.start()

  # Render-er assigned port theke Flask server start hobe
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)