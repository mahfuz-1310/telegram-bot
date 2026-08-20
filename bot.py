import os
import random
import string
import threading
import secrets
import uuid
from flask import Flask
import telebot
from telebot import types

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Data Lists for Names and Passwords
male_first_names = ['Aryan', 'Tanvir', 'Rahim', 'Sakib', 'Fahim', 'Nayeem', 'Rakib', 'Mehedi', 'Mahin', 'Sabbir', 'Arif', 'Shanto']
female_first_names = ['Sadia', 'Anika', 'Tasfia', 'Noshin', 'Faria', 'Sumaiya', 'Jannat', 'Ishrat', 'Riya', 'Muna', 'Tisha', 'Mim']
last_names = ['Ahmed', 'Hossain', 'Chowdhury', 'Islam', 'Khan', 'Rahman', 'Uddin', 'Talukder', 'Hasan', 'Sarker']
emojis = ['🔥', '✨', '👑', '😎', '💫', '🌟', '🚀', '🎯', '💯', '⚡', '💎']

def apply_unicode_font(text, style):
    emj = random.choice(emojis)
    res = ''
    for c in text:
        o = ord(c)
        if style == 'bold_sans':
            if 65 <= o <= 90: res += chr(120276 + (o - 65))
            elif 97 <= o <= 122: res += chr(120302 + (o - 97))
            else: res += c
        elif style == 'italic':
            if 65 <= o <= 90: res += chr(119808 + (o - 65))
            elif 97 <= o <= 122: res += chr(119834 + (o - 97))
            else: res += c
        elif style == 'mono':
            if 65 <= o <= 90: res += chr(120432 + (o - 65))
            elif 97 <= o <= 122: res += chr(120458 + (o - 97))
            else: res += c
        elif style == 'circled':
            if 65 <= o <= 90: res += chr(9398 + (o - 65))
            elif 97 <= o <= 122: res += chr(9424 + (o - 97))
            else: res += c
        else: res += c
    return f"{res} {emj}"

@app.route('/')
def home():
    return "Bot is running live!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    send_main_menu(message)

def send_main_menu(message_or_call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_male = types.InlineKeyboardButton('👦 Boy Name', callback_data='boy_font_menu')
    btn_female = types.InlineKeyboardButton('👧 Girl Name', callback_data='girl_font_menu')
    btn_stylish = types.InlineKeyboardButton('😎 Stylish Name', callback_data='gen_stylish')
    btn_random = types.InlineKeyboardButton('🎲 Random Name', callback_data='gen_random')
    btn_user = types.InlineKeyboardButton('👤 Username', callback_data='username_menu')
    btn_pass = types.InlineKeyboardButton('🔑 Password', callback_data='password_menu')
    btn_auth = types.InlineKeyboardButton('🔐 Auth Token', callback_data='auth_menu')
    
    markup.add(btn_male, btn_female, btn_stylish, btn_random, btn_user, btn_pass, btn_auth)
    text = '🌟 *Ultimate Generator Bot*\n\nSelect a category:'
    
    if isinstance(message_or_call, types.Message):
        bot.reply_to(message_or_call, text, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.edit_message_text(text, chat_id=message_or_call.message.chat.id, message_id=message_or_call.message.id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'main_menu':
        send_main_menu(call)
        return

    # Name and Pass Menu Handlers
    if call.data == 'boy_font_menu':
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('𝗔-𝗭 Bold Sans', callback_data='boy_bold_sans'),
            types.InlineKeyboardButton('𝐴-𝑍 Italic', callback_data='boy_italic'),
            types.InlineKeyboardButton('𝙰-𝚣 Monospace', callback_data='boy_mono'),
            types.InlineKeyboardButton('Ⓐ-Ⓩ Circled', callback_data='boy_circled'),
            types.InlineKeyboardButton('🔙 Back to Menu', callback_data='main_menu')
        )
        bot.edit_message_text('👦 *Select Boy Font Style:*', chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data == 'girl_font_menu':
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('𝗔-𝗭 Bold Sans', callback_data='girl_bold_sans'),
            types.InlineKeyboardButton('𝐴-𝑍 Italic', callback_data='girl_italic'),
            types.InlineKeyboardButton('𝙰-𝚣 Monospace', callback_data='girl_mono'),
            types.InlineKeyboardButton('Ⓐ-Ⓩ Circled', callback_data='girl_circled'),
            types.InlineKeyboardButton('🔙 Back to Menu', callback_data='main_menu')
        )
        bot.edit_message_text('👧 *Select Girl Font Style:*', chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data == 'username_menu':
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('👦 Boy Username', callback_data='gen_user_male'),
            types.InlineKeyboardButton('👧 Girl Username', callback_data='gen_user_female'),
            types.InlineKeyboardButton('🔙 Back to Menu', callback_data='main_menu')
        )
        bot.edit_message_text('👤 *Select Username Gender:*', chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data == 'password_menu':
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('🔒 8 Digits', callback_data='pass_8'),
            types.InlineKeyboardButton('🔒 12 Digits', callback_data='pass_12'),
            types.InlineKeyboardButton('🔒 16 Digits', callback_data='pass_16'),
            types.InlineKeyboardButton('🔙 Back to Menu', callback_data='main_menu')
        )
        bot.edit_message_text('🔑 *Select Password Length:*', chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data == 'auth_menu':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton('🔑 API Key (Hex)', callback_data='auth_apikey'),
            types.InlineKeyboardButton('🛡️ Bearer Token', callback_data='auth_bearer'),
            types.InlineKeyboardButton('🆔 UUID v4', callback_data='auth_uuid'),
            types.InlineKeyboardButton('🔙 Back to Menu', callback_data='main_menu')
        )
        bot.edit_message_text('🔐 *Select Authentication Type:*', chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # Generators Output Logic
    result_text = ''
    markup = types.InlineKeyboardMarkup(row_width=2)

    if call.data.startswith('boy_'):
        style = call.data.replace('boy_', '')
        raw_name = f"{random.choice(male_first_names)} {random.choice(last_names)}"
        result_text = apply_unicode_font(raw_name, style)
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data), types.InlineKeyboardButton('🔙 Back', callback_data='boy_font_menu'))
    elif call.data.startswith('girl_'):
        style = call.data.replace('girl_', '')
        raw_name = f"{random.choice(female_first_names)} {random.choice(last_names)}"
        result_text = apply_unicode_font(raw_name, style)
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data), types.InlineKeyboardButton('🔙 Back', callback_data='girl_font_menu'))
    elif call.data == 'gen_user_male':
        result_text = f"{random.choice(male_first_names).lower()}_{random.choice(last_names).lower()}{random.randint(10,999)}"
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_user_male'), types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
    elif call.data == 'gen_user_female':
        result_text = f"{random.choice(female_first_names).lower()}_{random.choice(last_names).lower()}{random.randint(10,999)}"
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_user_female'), types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
    elif call.data.startswith('pass_'):
        length = int(call.data.replace('pass_', ''))
        result_text = ''.join(random.choices(string.ascii_letters + string.digits + '@#$%!', k=length))
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data), types.InlineKeyboardButton('🔙 Back', callback_data='password_menu'))
    elif call.data == 'auth_apikey':
        result_text = secrets.token_hex(20) # 40 characters hex API key
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='auth_apikey'), types.InlineKeyboardButton('🔙 Back', callback_data='auth_menu'))
    elif call.data == 'auth_bearer':
        result_text = secrets.token_urlsafe(32) # Secure URL-safe token
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='auth_bearer'), types.InlineKeyboardButton('🔙 Back', callback_data='auth_menu'))
    elif call.data == 'auth_uuid':
        result_text = str(uuid.uuid4())
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='auth_uuid'), types.InlineKeyboardButton('🔙 Back', callback_data='auth_menu'))
    elif call.data == 'gen_stylish':
        f_name = random.choice(male_first_names + female_first_names).lower()
        l_name = random.choice(last_names).lower()
        result_text = f"{f_name} {l_name} 😎⚡"
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_stylish'), types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
    elif call.data == 'gen_random':
        result_text = f"{random.choice(male_first_names + female_first_names)} {random.choice(last_names)} {random.choice(emojis)}"
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_random'), types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))

    is_code_format = 'pass_' in call.data or call.data.startswith('auth_')
    text = f'✨ *Result:*\n\n`{result_text}`' if is_code_format else f'✨ *Result:*\n\n{result_text}'
    bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)

def run_bot():
    try:
        bot.remove_webhook()
    except:
        pass
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
