import os
import random
import threading
from flask import Flask
import telebot
from telebot import types

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
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
    'Rakib',
    'Mehedi',
    'Faria',
    'Sumaiya',
    'Mahin',
    'Jannat',
    'Sabbir',
    'Ishrat',
    'Arif',
    'Shanto',
    'Riya',
    'Dipu',
    'Muna',
    'Farhan',
    'Tisha',
    'Rafsan',
    'Mim',
    'Niloy',
    'Siam',
    'Ratul',
    'Priya',
    'Joy',
    'Hridoy',
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
    'Hasan',
    'Mondol',
    'Sarker',
    'Biswas',
    'Deb',
    'Karim',
    'Kabir',
    'Barua',
    'Das',
    'Majumder',
    'Haider',
    'Miah',
    'Sheikh',
    'Bhuiyan',
]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  markup = types.InlineKeyboardMarkup()
  btn = types.InlineKeyboardButton(
      '🎲 Generate Name', callback_data='generate_name'
  )
  markup.add(btn)
  bot.reply_to(
      message,
      'Welcome! Name Generator Bot-e apnake shagotom.\nNicher button-e click'
      ' kore name generate korun:',
      reply_markup=markup,
  )


@bot.message_handler(commands=['generate'])
def generate_name_msg(message):
  send_generated_name(message.chat.id)


def send_generated_name(chat_id, call=None):
  name = f'{random.choice(first_names)} {random.choice(last_names)}'
  # Code block (```) use korar fole tap korlei copy hoye jabe
  text = f'Apnar generated name:\n`{name}`'

  markup = types.InlineKeyboardMarkup()
  btn = types.InlineKeyboardButton(
      '🔄 Another Name', callback_data='generate_name'
  )
  markup.add(btn)

  if call:
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
  else:
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'generate_name')
def callback_query(call):
  send_generated_name(call.message.chat.id, call=call)


@app.route('/')
def home():
  return 'Telegram Bot is running smoothly!'


def run_bot():
  bot.infinity_polling()


if __name__ == '__main__':
  t = threading.Thread(target=run_bot)
  t.start()
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
