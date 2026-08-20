import os
import random
import string
import threading
from flask import Flask
import telebot
from telebot import types

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Data Lists
male_first_names = [
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
]
female_first_names = [
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


# Username Generator Function
def generate_username(gender):
  if gender == 'male':
    f_name = random.choice(male_first_names).lower()
  else:
    f_name = random.choice(female_first_names).lower()

  l_name = random.choice(last_names).lower()
  number = random.randint(10, 999)
  return f'{f_name}_{l_name}{number}'


# Password Generator Function with Length
def generate_password(length):
  chars = string.ascii_letters + string.digits + '@#$%&!-_'
  return ''.join(random.choice(chars) for _ in range(length))


# Font/Style Application Function
def apply_font(text, font_style):
  if font_style == 'bold':
    return f'*{text}*'
  elif font_style == 'italic':
    return f'_{text}_'
  elif font_style == 'mono':
    return f'`{text}`'
  elif font_style == 'strike':
    return f'~{text}~'
  else:
    return text


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  send_main_menu(message)


def send_main_menu(message_or_call):
  markup = types.InlineKeyboardMarkup(row_width=2)
  btn_male = types.InlineKeyboardButton('👦 Boy Name', callback_data='boy_font_menu')
  btn_female = types.InlineKeyboardButton(
      '👧 Girl Name', callback_data='girl_font_menu'
  )
  btn_stylish = types.InlineKeyboardButton(
      '😎 Stylish Name', callback_data='gen_stylish'
  )
  btn_random = types.InlineKeyboardButton(
      '🎲 Random Name', callback_data='gen_random'
  )
  btn_user = types.InlineKeyboardButton(
      '👤 Username', callback_data='username_menu'
  )
  btn_pass = types.InlineKeyboardButton(
      '🔑 Password', callback_data='password_menu'
  )

  markup.add(btn_male, btn_female, btn_stylish, btn_random, btn_user, btn_pass)

  welcome_text = '🌟 *Ultimate Generator Bot*\n\nSelect a category:'

  if isinstance(message_or_call, types.Message):
    bot.reply_to(
        message_or_call, welcome_text, parse_mode='Markdown', reply_markup=markup
    )
  else:
    bot.edit_message_text(
        welcome_text,
        chat_id=message_or_call.message.chat.id,
        message_id=message_or_call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
  if call.data == 'main_menu':
    send_main_menu(call)
    return

  # Boy Font Selection Menu
  if call.data == 'boy_font_menu':
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('<b>Bold</b>', callback_data='boy_bold'),
        types.InlineKeyboardButton('<i>Italic</i>', callback_data='boy_italic'),
        types.InlineKeyboardButton('<code>Mono</code>', callback_data='boy_mono'),
        types.InlineKeyboardButton('<s>Strike</s>', callback_data='boy_strike'),
        types.InlineKeyboardButton('Normal', callback_data='boy_normal'),
        types.InlineKeyboardButton(
            '🔙 Back to Menu', callback_data='main_menu'
        ),
    )
    bot.edit_message_text(
        '👦 *Select Boy Name Font Style:*',
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

  # Girl Font Selection Menu
  if call.data == 'girl_font_menu':
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton('<b>Bold</b>', callback_data='girl_bold'),
        types.InlineKeyboardButton('<i>Italic</i>', callback_data='girl_italic'),
        types.InlineKeyboardButton('<code>Mono</code>', callback_data='girl_mono'),
        types.InlineKeyboardButton('<s>Strike</s>', callback_data='girl_strike'),
        types.InlineKeyboardButton('Normal', callback_data='girl_normal'),
        types.InlineKeyboardButton(
            '🔙 Back to Menu', callback_data='main_menu'
        ),
    )
    bot.edit_message_text(
        '👧 *Select Girl Name Font Style:*',
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

  # Username Sub-Menu
  if call.data == 'username_menu':
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_boy = types.InlineKeyboardButton(
        '👦 Boy Username', callback_data='gen_user_male'
    )
    btn_girl = types.InlineKeyboardButton(
        '👧 Girl Username', callback_data='gen_user_female'
    )
    btn_back = types.InlineKeyboardButton(
        '🔙 Back to Menu', callback_data='main_menu'
    )
    markup.add(btn_boy, btn_girl, btn_back)

    bot.edit_message_text(
        '👤 *Select Username Gender:*',
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

  # Password Sub-Menu (Length Selection up to 45)
  if call.data == 'password_menu':
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_8 = types.InlineKeyboardButton('🔒 8 Digits', callback_data='pass_8')
    btn_12 = types.InlineKeyboardButton('🔒 12 Digits', callback_data='pass_12')
    btn_16 = types.InlineKeyboardButton('🔒 16 Digits', callback_data='pass_16')
    btn_45 = types.InlineKeyboardButton('🔒 45 Digits', callback_data='pass_45')
    btn_back = types.InlineKeyboardButton(
        '🔙 Back to Menu', callback_data='main_menu'
    )
    markup.add(btn_8, btn_12, btn_16, btn_45, btn_back)

    bot.edit_message_text(
        '🔑 *Select Password Length:*',
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

  # Generation Logic
  name = ''
  markup = types.InlineKeyboardMarkup(row_width=2)

  # Boy Fonts Logic
  if call.data.startswith('boy_'):
    style = call.data.split('_')[1]
    raw_name = (
        f'{random.choice(male_first_names)} {random.choice(last_names)}'
    )
    name = apply_font(raw_name, style)
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data=call.data
        )
    )
    markup.add(
        types.InlineKeyboardButton('🔙 Change Font', callback_data='boy_font_menu')
    )

  # Girl Fonts Logic
  elif call.data.startswith('girl_'):
    style = call.data.split('_')[1]
    raw_name = (
        f'{random.choice(female_first_names)} {random.choice(last_names)}'
    )
    name = apply_font(raw_name, style)
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data=call.data
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            '🔙 Change Font', callback_data='girl_font_menu'
        )
    )

  elif call.data == 'gen_user_male':
    name = generate_username('male')
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data='gen_user_male'
        )
    )
    markup.add(
        types.InlineKeyboardButton('🔙 Back', callback_data='username_menu')
    )

  elif call.data == 'gen_user_female':
    name = generate_username('female')
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data='gen_user_female'
        )
    )
    markup.add(
        types.InlineKeyboardButton('🔙 Back', callback_data='username_menu')
    )

  elif call.data == 'pass_8':
    name = generate_password(8)
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data='pass_8'
        )
    )
    markup.add(
        types.InlineKeyboardButton('🔙 Back', callback_data='password_menu')
    )

  elif call.data == 'pass_12':
    name = generate_password(12)
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data='pass_12'
        )
    )
    markup.add(
        types.InlineKeyboardButton('🔙 Back', callback_data='password_menu')
    )

  elif call.data == 'pass_16':
    name = generate_password(16)
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data='pass_16'
        )
    )
    markup.add(
        types.InlineKeyboardButton('🔙 Back', callback_data='password_menu')
    )

  elif call.data == 'pass_45':
    name = generate_password(45)
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data='pass_45'
        )
    )
    markup.add(
        types.InlineKeyboardButton('🔙 Back', callback_data='password_menu')
    )

  elif call.data == 'gen_stylish':
    name = random.choice(stylish_names)
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data='gen_stylish'
        )
    )
    markup.add(
        types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
    )

  elif call.data == 'gen_random':
    all_names = male_first_names + female_first_names
    name = f'{random.choice(all_names)} {random.choice(last_names)}'
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data='gen_random'
        )
    )
    markup.add(
        types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
    )

  # Send the result
  text = f'✨ *Result:*\n\n`{name}`' if 'pass_' in call.data or 'user_' in call.data else f'✨ *Result:*\n\n{name}'
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
