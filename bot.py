import os
import random
import string
import threading
from flask import Flask
import requests
import telebot
from telebot import types

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Massive Expanded Data Lists
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
    'Arman',
    'Rashed',
    'Jewel',
    'Parvez',
    'Imran',
    'Shohag',
    'Shuvo',
    'Al-Amin',
    'Rafsan',
    'Ferdous',
    'Asif',
    'Bijoy',
    'Monir',
    'Zaber',
    'Fahad',
    'Tarek',
    'Rimon',
    'Jishan',
    'Nabil',
    'Rifat',
    'Sazzad',
    'Joy',
    'Shihab',
    'Hasan',
    'Tareq',
    'Tanim',
    'Shakil',
    'Ashraful',
    'Mahbub',
    'Mustafiz',
    'Nafees',
    'Rony',
    'Sohel',
    'Rubel',
    'Liton',
    'Mamun',
    'Jamal',
    'Kamal',
    'Borhan',
    'Zahid',
    'Sujon',
    'Ripon',
    'Anik',
    'Touhid',
    'Sagor',
    'Nipun',
    'Pranto',
    'Raihan',
    'Sohan',
    'Titu',
    'Bappi',
    'Rasel',
    'Sumon',
    'Biplob',
    'Adnan',
    'Rakin',
    'Mabrur',
    'Sajid',
    'Ashik',
    'Ridoy',
    'Nihad',
    'Zihad',
    'Faiyaz',
    'Ayman',
    'Zayan',
    'Rayhan',
    'Tanim',
    'Samin',
    'Ahnaf',
    'Abrar',
    'Mushfiq',
    'Tamim',
    'Likhon',
    'Sabbir',
    'Nafis',
    'Shiam',
    'Shawon',
    'Mehedi',
    'Sohanur',
    'Imtiaz',
    'Tanvir',
    'Mahfuz',
    'Sajib',
    'Prozen',
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
    'Farhana',
    'Tasnim',
    'Bushra',
    'Nadia',
    'Sabrina',
    'Farzana',
    'Mehzabien',
    'Puspita',
    'Bristy',
    'Lamia',
    'Sneha',
    'Tanha',
    'Mahi',
    'Oishee',
    'Puja',
    'Sanjida',
    'Roksana',
    'Sharmin',
    'Taslima',
    'Lima',
    'Sultana',
    'Akhi',
    'Afroza',
    'Moushumi',
    'Popy',
    'Sonia',
    'Kona',
    'Tania',
    'Tonmoyee',
    'Shanta',
    'Rina',
    'Mina',
    'Tina',
    'Diba',
    'Rumpa',
    'Swarna',
    'Meem',
    'Megha',
    'Nila',
    'Purnima',
    'Simu',
    'Bably',
    'Mou',
    'Sathi',
    'Jui',
    'Nipa',
    'Mehreen',
    'Adiba',
    'Farha',
    'Tasnuva',
    'Raisa',
    'Maisha',
    'Lamisa',
    'Samia',
    'Fariha',
    'Jerin',
    'Maliha',
    'Afifa',
    'Zarin',
    'Nazifa',
    'Tabassum',
    'Sabiha',
    'Nabila',
    'Farheen',
    'Mahjabin',
    'Sanjida',
    'Suraiya',
    'Mithila',
    'Puspita',
    'Trisha',
    'Sneha',
    'Anjum',
    'Farha',
    'Ritu',
    'Nusrat',
    'Subah',
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
    'Majumder',
    'Miah',
    'Sheikh',
    'Bhuiyan',
    'Ali',
    'Hawlader',
    'Siddique',
    'Mia',
    'Prodhan',
    'Mollah',
    'Sikder',
    'Patwary',
    'Dewan',
    'Kazi',
    'Bepari',
    'Sardar',
    'Munshi',
    'Roy',
    'Sen',
    'Barua',
    'Deb',
    'Nath',
    'Pal',
    'Saha',
    'Bhowmik',
    'Dey',
    'Bardhan',
    'Gosh',
    'Chakma',
    'Baidya',
    'Talukder',
]
emojis = ['🔥', '✨', '👑', '😎', '💫', '🌟', '🚀', '🎯', '💯', '⚡', '💎']

# Words for Hotmail/Outlook style mail generation
mail_words1 = [
    'grey',
    'dark',
    'cool',
    'swift',
    'frost',
    'shadow',
    'neon',
    'iron',
    'alpha',
    'cyber',
    'mega',
    'lunar',
]
mail_words2 = [
    'savage',
    'knight',
    'coder',
    'gamer',
    'wolf',
    'dragon',
    'storm',
    'ninja',
    'Vortex',
    'blaze',
]
mail_words3 = ['cedc', 'pro', 'x', 'zen', 'bot', 'hub', 'net', 'sec']


def generate_username(gender):
  if gender == 'male':
    f_name = random.choice(male_first_names).lower()
  else:
    f_name = random.choice(female_first_names).lower()
  l_name = random.choice(last_names).lower()
  number = random.randint(10, 999)
  return f'{f_name}_{l_name}{number}'


def generate_password(length):
  chars = string.ascii_letters + string.digits + '@#$%&!-_'
  return ''.join(random.choice(chars) for _ in range(length))


# Custom Hotmail/Outlook style Temp Mail Generator
def generate_temp_mail():
  w1 = random.choice(mail_words1)
  w2 = random.choice(mail_words2)
  w3 = random.choice(mail_words3)
  custom_username = f'{w1}{w2}{w3}'

  domains = ['1secmail.com', '1secmail.org', '1secmail.net']
  domain = random.choice(domains)

  # API-তে রেজিস্টার করার জন্য
  try:
    requests.get(
        f'https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1'
    )
  except:
    pass

  return f'{custom_username}@hotmail.com', f'{custom_username}@{domain}'


def check_inbox_messages(real_email):
  try:
    login, domain = real_email.split('@')
    url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
    response = requests.get(url)
    if response.status_code == 200:
      return response.json()
  except:
    pass
  return []


def read_mail_content(real_email, msg_id):
  try:
    login, domain = real_email.split('@')
    url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}'
    response = requests.get(url)
    if response.status_code == 200:
      return response.json()
  except:
    pass
  return None


def apply_unicode_font(text, style):
  emj = random.choice(emojis)
  res = ''
  for c in text:
    o = ord(c)
    if style == 'bold_sans':
      if 65 <= o <= 90:
        res += chr(120276 + (o - 65))
      elif 97 <= o <= 122:
        res += chr(120302 + (o - 97))
      else:
        res += c
    elif style == 'italic':
      if 65 <= o <= 90:
        res += chr(119808 + (o - 65))
      elif 97 <= o <= 122:
        res += chr(119834 + (o - 97))
      else:
        res += c
    elif style == 'mono':
      if 65 <= o <= 90:
        res += chr(120432 + (o - 65))
      elif 97 <= o <= 122:
        res += chr(120458 + (o - 97))
      else:
        res += c
    elif style == 'circled':
      if 65 <= o <= 90:
        res += chr(9398 + (o - 65))
      elif 97 <= o <= 122:
        res += chr(9424 + (o - 97))
      else:
        res += c
    elif style == 'bold_serif':
      if 65 <= o <= 90:
        res += chr(119964 + (o - 65))
      elif 97 <= o <= 122:
        res += chr(119990 + (o - 97))
      else:
        res += c
    else:
      res += c
  return f'{res} {emj}'


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
  btn_mail = types.InlineKeyboardButton(
      '📧 Outlook Mail', callback_data='gen_outlook_mail'
  )

  markup.add(
      btn_male,
      btn_female,
      btn_stylish,
      btn_random,
      btn_user,
      btn_pass,
      btn_mail,
  )

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

  if call.data == 'boy_font_menu':
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            '𝗔-𝗭 Bold Sans', callback_data='boy_bold_sans'
        ),
        types.InlineKeyboardButton('𝐴-𝑍 Italic', callback_data='boy_italic'),
        types.InlineKeyboardButton('𝙰-𝚣 Monospace', callback_data='boy_mono'),
        types.InlineKeyboardButton('Ⓐ-Ⓩ Circled', callback_data='boy_circled'),
        types.InlineKeyboardButton(
            '𝐀-𝐳 Bold Serif', callback_data='boy_bold_serif'
        ),
        types.InlineKeyboardButton(
            '🔙 Back to Menu', callback_data='main_menu'
        ),
    )
    bot.edit_message_text(
        '👦 *Select Boy Font Style:*',
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

  if call.data == 'girl_font_menu':
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            '𝗔-𝗭 Bold Sans', callback_data='girl_bold_sans'
        ),
        types.InlineKeyboardButton('𝐴-𝑍 Italic', callback_data='girl_italic'),
        types.InlineKeyboardButton('𝙰-𝚣 Monospace', callback_data='girl_mono'),
        types.InlineKeyboardButton('Ⓐ-Ⓩ Circled', callback_data='girl_circled'),
        types.InlineKeyboardButton(
            '𝐀-𝐳 Bold Serif', callback_data='girl_bold_serif'
        ),
        types.InlineKeyboardButton(
            '🔙 Back to Menu', callback_data='main_menu'
        ),
    )
    bot.edit_message_text(
        '👧 *Select Girl Font Style:*',
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

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

  # Outlook/Hotmail Mail Generation (Displaying hotmail.com format, working inbox backend)
  if call.data == 'gen_outlook_mail':
    display_mail, real_mail = generate_temp_mail()
    text = f'📧 *Generated Hotmail/Outlook Address:*\n\n`{display_mail}`\n\nNicher button-e click kore inbox check korun:'
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            '📥 Inbox Check', callback_data=f'inbox_{real_mail}'
        ),
        types.InlineKeyboardButton(
            '🔄 New Mail', callback_data='gen_outlook_mail'
        ),
        types.InlineKeyboardButton(
            '🏠 Main Menu', callback_data='main_menu'
        ),
    )
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

  if call.data.startswith('inbox_'):
    real_email = call.data.replace('inbox_', '')
    # Display email formatting back to hotmail style for user clarity
    username = real_email.split('@')[0]
    display_email = f'{username}@hotmail.com'

    messages = check_inbox_messages(real_email)

    text = f'📧 *Email:* `{display_email}`\n\n'
    markup = types.InlineKeyboardMarkup(row_width=1)

    if messages:
      text += f'📥 *Inbox-e {len(messages)} টি মেসেজ পাওয়া গেছে:*'
      for msg in messages:
        subject = msg.get('subject', 'No Subject')
        sender = msg.get('from', 'Unknown Sender')
        msg_id = msg.get('id')
        markup.add(
            types.InlineKeyboardButton(
                f'📩 {subject[:20]} ({sender[:15]})',
                callback_data=f'read_{real_email}_{msg_id}',
            )
        )
    else:
      text += '📭 *Inbox is empty! (Kono message asheni)*'

    markup.add(
        types.InlineKeyboardButton('🔄 Refresh Inbox', callback_data=call.data),
        types.InlineKeyboardButton(
            '📧 New Email', callback_data='gen_outlook_mail'
        ),
        types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'),
    )

    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

  if call.data.startswith('read_'):
    parts = call.data.split('_', 2)
    real_email = parts[1]
    msg_id = parts[2]

    msg_data = read_mail_content(real_email, msg_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            '🔙 Back to Inbox', callback_data=f'inbox_{real_email}'
        )
    )

    if msg_data:
      sender = msg_data.get('from', 'Unknown')
      subject = msg_data.get('subject', 'No Subject')
      body = msg_data.get('textBody', 'No text content available.')
      date = msg_data.get('date', '')

      text = (
          f'📩 *From:* `{sender}`\n📌 *Subject:* `{subject}`\n🕒 *Date:*'
          f' `{date}`\n\n💬 *Message Body:*\n`{body}`'
      )
    else:
      text = '❌ Message read korte shomossha hoyeche.'

    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )
    return

  name = ''
  markup = types.InlineKeyboardMarkup(row_width=2)

  if call.data.startswith('boy_'):
    style = call.data.replace('boy_', '')
    raw_name = (
        f'{random.choice(male_first_names)} {random.choice(last_names)}'
    )
    name = apply_unicode_font(raw_name, style)
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data=call.data
        )
    )
    markup.add(
        types.InlineKeyboardButton('🔙 Change Font', callback_data='boy_font_menu')
    )

  elif call.data.startswith('girl_'):
    style = call.data.replace('girl_', '')
    raw_name = (
        f'{random.choice(female_first_names)} {random.choice(last_names)}'
    )
    name = apply_unicode_font(raw_name, style)
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
    all_firsts = male_first_names + female_first_names
    f_name = random.choice(all_firsts).lower()
    l_name = random.choice(last_names).lower()
    stylish_styles = [
        f'{f_name} {l_name} 😎⚡',
        f'{f_name} {l_name} !¡ 🚩',
        f'{f_name} {l_name} 🖤✨',
        f'{f_name} {l_name} ⚡🔥',
        f'{f_name} {l_name} 🍁🥀',
        f'{f_name} {l_name} 👑💫',
        f'{f_name} {l_name} 💯🔥',
        f'{f_name} {l_name} ☠️⚡',
    ]
    name = random.choice(stylish_styles)
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
    name = (
        f'{random.choice(all_names)} {random.choice(last_names)}'
        f' {random.choice(emojis)}'
    )
    markup.add(
        types.InlineKeyboardButton(
            '🔄 Generate Again', callback_data='gen_random'
        )
    )
    markup.add(
        types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
    )

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
