import os
import random
import threading
from flask import Flask
import telebot
from telebot import types

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Data Lists
first_names = [
    'Aryan',
    'Tanvir',
    'Rahim',
    'Sakib',
    'Fahim',
    'Nayeem',
    'Rakib',
    'Mehedi',
    'Mahin',
    'Sabbir',
    'Arif',
    'Shanto',
    'Farhan',
    'Niloy',
    'Siam',
    'Hridoy',
    'Sadia',
    'Anika',
    'Tasfia',
    'Noshin',
    'Faria',
    'Sumaiya',
    'Jannat',
    'Ishrat',
    'Riya',
    'Muna',
    'Tisha',
    'Mim',
    'Priya',
    'Nusrat',
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
    'Karim',
    'Kabir',
    'Das',
]
stylish_names = [
    '⚡ Shadow ⚡',
    '🔥 Vortex 🔥',
    '👑 King 👑',
    '💀 Ghost 💀',
    '💎 Diamond 💎',
    '🌪️ Storm 🌪️',
    '⚡ Flash ⚡',
    '🔥 Blaze 🔥',
    '❄️ Frost ❄️',
    '🌙 Eclipse 🌙',
]


def generate_username():
  f_name = random.choice(first_names).lower()
  l_name = random.choice(last_names).lower()
  number = random.randint(10, 999)
  return f'{f_name}_{l_name}{number}'


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  markup = types.InlineKeyboardMarkup(row_width=2)
  btn_male = types.InlineKeyboardButton('👦 Boy', callback_data='gen_male')
  btn_female = types.InlineKeyboardButton('👧 Girl', callback_data='gen_female')
  btn_stylish = types.InlineKeyboardButton('😎 Stylish', callback_data='gen_stylish')
  btn_random = types.InlineKeyboardButton('🎲 Random', callback_data='gen_random')
  btn_user = types.InlineKeyboardButton(
      '👤 Username', callback_data='gen_username'
  )
  markup.add(btn_male, btn_female, btn_stylish, btn_random, btn_user)

  welcome_text = '🌟 *Ultimate Generator Bot*\n\nSelect a category:'
  bot.reply_to(
      message, welcome_text, parse_mode='Markdown', reply_markup=markup
  )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  if call.data == 'main_menu':
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_male = types.InlineKeyboardButton('👦 Boy', callback_data='gen_male')
    btn_female = types.InlineKeyboardButton('👧 Girl', callback_data='gen_female')
    btn_stylish = types.InlineKeyboardButton(
        '😎 Stylish', callback_data='gen_stylish'
    )
    btn_random = types.InlineKeyboardButton(
        '🎲 Random', callback_data='gen_random'
    )
    btn_user = types.InlineKeyboardButton(
        '👤 Username', callback_data='gen_username'
    )
    markup.add(btn_male, btn_female, btn_stylish, btn_random, btn_user)

    bot.edit_message_text(
        '🌟 *Ultimate Generator Bot*\n\nSelect a category:',
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

  if call.data == 'gen_username':
    name = generate_username()
  elif call.data == 'gen_male':
    name = f'{random.choice(first_names[:16])} {random.choice(last_names)}'
  elif call.data == 'gen_female':
    name = f'{random.choice(first_names[16:])} {random.choice(last_names)}'
  elif call.data == 'gen_stylish':
    name = random.choice(stylish_names)
  else:
    name = f'{random.choice(first_names)} {random.choice(last_names)}'

  text = f'✨ *Result:*\n\n`{name}`'

  markup = types.InlineKeyboardMarkup(row_width=2)
  btn_again = types.InlineKeyboardButton(
      '🔄 Generate Again', callback_data=call.data
  )
  btn_menu = types.InlineKeyboardButton(
      '🏠 Main Menu', callback_data='main_menu'
  )
  markup.add(btn_again, btn_menu)

  bot.edit_message_text(
      text,
      chat_id=call.message.chat.id,
      message_id=call.message.id,
      parse_mode='Markdown',
      reply_markup=markup,
  )


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
