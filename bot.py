import os
import random
import threading
from flask import Flask
import telebot
from telebot import types

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Category-wise name lists
male_names = [
    'Aryan Ahmed',
    'Tanvir Hossain',
    'Rahim Chowdhury',
    'Sakib Islam',
    'Fahim Khan',
    'Nayeem Rahman',
    'Rakib Hasan',
    'Mehedi Sarker',
    'Mahin Biswas',
    'Sabbir Karim',
    'Arif Kabir',
    'Shanto Das',
    'Farhan Majumder',
    'Niloy Miah',
    'Siam Sheikh',
    'Hridoy Bhuiyan',
]

female_names = [
    'Sadia Ahmed',
    'Anika Hossain',
    'Tasfia Chowdhury',
    'Noshin Islam',
    'Faria Khan',
    'Sumaiya Rahman',
    'Jannat Hasan',
    'Ishrat Mondol',
    'Riya Sarker',
    'Muna Biswas',
    'Tisha Deb',
    'Mim Karim',
    'Priya Das',
    'Nusrat Barua',
    'Mehzabien Haider',
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
]


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  # Modern Grid UI layout with 2 buttons per row
  markup = types.InlineKeyboardMarkup(row_width=2)
  btn_male = types.InlineKeyboardButton(
      '👦 Boy Names', callback_data='gen_male'
  )
  btn_female = types.InlineKeyboardButton(
      '👧 Girl Names', callback_data='gen_female'
  )
  btn_stylish = types.InlineKeyboardButton(
      '😎 Stylish Names', callback_data='gen_stylish'
  )
  btn_random = types.InlineKeyboardButton(
      '🎲 Random Name', callback_data='gen_random'
  )
  markup.add(btn_male, btn_female, btn_stylish, btn_random)

  welcome_text = (
      '🌟 *Welcome to Ultimate Name Generator Bot!*\n\nNicher option gulo'
      ' theke apnar pochhonder category select korun:'
  )
  bot.reply_to(
      message, welcome_text, parse_mode='Markdown', reply_markup=markup
  )


def get_name_by_category(category):
  if category == 'gen_male':
    return random.choice(male_names)
  elif category == 'gen_female':
    return random.choice(female_names)
  elif category == 'gen_stylish':
    return random.choice(stylish_names)
  else:
    return f'{random.choice(["Aryan", "Sadia", "Tanvir", "Anika"])} {random.choice(last_names)}'


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('gen_')
    or call.data == 'main_menu'
)
def handle_callback(call):
  if call.data == 'main_menu':
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_male = types.InlineKeyboardButton(
        '👦 Boy Names', callback_data='gen_male'
    )
    btn_female = types.InlineKeyboardButton(
        '👧 Girl Names', callback_data='gen_female'
    )
    btn_stylish = types.InlineKeyboardButton(
        '😎 Stylish Names', callback_data='gen_stylish'
    )
    btn_random = types.InlineKeyboardButton(
        '🎲 Random Name', callback_data='gen_random'
    )
    markup.add(btn_male, btn_female, btn_stylish, btn_random)

    bot.edit_message_text(
        '🌟 *Main Menu*\n\nNicher option gulo theke category select korun:',
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
  else:
    name = get_name_by_category(call.data)
    # Code block for easy tap-to-copy functionality
    text = f'✨ *Generated Name:*\n\n`{name}`'

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
