import os
import random
import re
import string
import threading
from flask import Flask
import requests
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
mail_words1 = ['grey', 'dark', 'cool', 'swift', 'frost', 'shadow', 'neon', 'iron', 'alpha']
mail_words2 = ['savage', 'knight', 'coder', 'gamer', 'wolf', 'dragon', 'storm', 'ninja']
mail_words3 = ['cedc', 'pro', 'x', 'zen', 'bot', 'hub', 'net', 'sec']

def generate_temp_mail():
    w1 = random.choice(mail_words1)
    w2 = random.choice(mail_words2)
    w3 = random.choice(mail_words3)
    username = f"{w1}{w2}{w3}{random.randint(10,999)}"
    display_domain = random.choice(['hotmail.com', 'outlook.com', 'gmail.com'])
    real_domain = '1secmail.com'
    return f"{username}@{display_domain}", f"{username}@{real_domain}"

def check_inbox_messages(real_email):
    try:
        login, domain = real_email.split('@')
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except: 
        pass
    return []

def read_mail_content(real_email, msg_id):
    try:
        login, domain = real_email.split('@')
        url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except: 
        pass
    return None

def extract_otp_code(body):
    pattern = r'(?i)(?:code|otp|pin|verification|password|verify)[:\s]*([A-Za-z0-9]{4,8})'
    match = re.search(pattern, body)
    if match: return match.group(1)
    num_match = re.search(r'\b\d{4,6}\b', body)
    return num_match.group(0) if num_match else None

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
    btn_mail = types.InlineKeyboardButton('📧 Temp Mail', callback_data='gen_temp_mail')
    
    markup.add(btn_male, btn_female, btn_stylish, btn_random, btn_user, btn_pass, btn_mail)
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

    # Temp Mail Handlers
    if call.data == 'gen_temp_mail':
        display_mail, real_mail = generate_temp_mail()
        text = f'📧 *Generated Mail:*\n\n`{display_mail}`\n\n📥 *Inbox check korte nicher button-e click korun:*'
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton('📥 Inbox Check', callback_data=f'inbox_{real_mail}'),
            types.InlineKeyboardButton('🔄 New Mail', callback_data='gen_temp_mail'),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data.startswith('inbox_'):
        real_email = call.data.replace('inbox_', '')
        username = real_email.split('@')[0]
        display_email = f"{username}@hotmail.com"
        
        messages = check_inbox_messages(real_email)
        text = f'📧 *Email:* `{display_email}`\n\n'
        markup = types.InlineKeyboardMarkup(row_width=1)

        if messages:
            text += f'📥 *Inbox-e {len(messages)} টি মেসেজ পাওয়া গেছে:*'
            for msg in messages:
                markup.add(types.InlineKeyboardButton(f'📩 {msg.get("subject", "No Subject")[:20]}', callback_data=f'read_{real_email}_{msg.get("id")}'))
        else:
            text += '📭 *Inbox is empty! (Waiting for messages)*'
        
        markup.add(
            types.InlineKeyboardButton('🔄 Refresh Inbox', callback_data=call.data),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data.startswith('read_'):
        parts = call.data.split('_', 2)
        real_email, msg_id = parts[1], parts[2]
        
        msg_data = read_mail_content(real_email, msg_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if msg_data:
            sender = msg_data.get('from', 'Unknown')
            subject = msg_data.get('subject', 'No Subject')
            body = msg_data.get('textBody', 'No text content available.')
            text = f'📩 *From:* `{sender}`\n📌 *Subject:* `{subject}`\n\n💬 *Body:*\n`{body[:400]}`'
            markup.add(types.InlineKeyboardButton('🔑 Get Code', callback_data=f'code_{real_email}_{msg_id}'))
        else:
            text = '❌ Message read failed.'
        markup.add(types.InlineKeyboardButton('🔙 Back to Inbox', callback_data=f'inbox_{real_email}'))
        
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data.startswith('code_'):
        parts = call.data.split('_', 2)
        real_email, msg_id = parts[1], parts[2]
        
        msg_data = read_mail_content(real_email, msg_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('🔙 Back to Message', callback_data=f'read_{real_email}_{msg_id}'))
        
        if msg_data:
            body = msg_data.get('textBody', '')
            otp = extract_otp_code(body)
            text = f'🔑 *Verification Code:* `{otp}`' if otp else '⚠️ *Code paowa jayni!*'
        else:
            text = '❌ Failed to fetch.'
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
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

    # Generators Output Logic
    name = ''
    markup = types.InlineKeyboardMarkup(row_width=2)

    if call.data.startswith('boy_'):
        style = call.data.replace('boy_', '')
        raw_name = f"{random.choice(male_first_names)} {random.choice(last_names)}"
        name = apply_unicode_font(raw_name, style)
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data), types.InlineKeyboardButton('🔙 Back', callback_data='boy_font_menu'))
    elif call.data.startswith('girl_'):
        style = call.data.replace('girl_', '')
        raw_name = f"{random.choice(female_first_names)} {random.choice(last_names)}"
        name = apply_unicode_font(raw_name, style)
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data), types.InlineKeyboardButton('🔙 Back', callback_data='girl_font_menu'))
    elif call.data == 'gen_user_male':
        name = f"{random.choice(male_first_names).lower()}_{random.choice(last_names).lower()}{random.randint(10,999)}"
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_user_male'), types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
    elif call.data == 'gen_user_female':
        name = f"{random.choice(female_first_names).lower()}_{random.choice(last_names).lower()}{random.randint(10,999)}"
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_user_female'), types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
    elif call.data.startswith('pass_'):
        length = int(call.data.replace('pass_', ''))
        name = ''.join(random.choices(string.ascii_letters + string.digits + '@#$%!', k=length))
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data), types.InlineKeyboardButton('🔙 Back', callback_data='password_menu'))
    elif call.data == 'gen_stylish':
        f_name = random.choice(male_first_names + female_first_names).lower()
        l_name = random.choice(last_names).lower()
        name = f"{f_name} {l_name} 😎⚡"
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_stylish'), types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
    elif call.data == 'gen_random':
        name = f"{random.choice(male_first_names + female_first_names)} {random.choice(last_names)} {random.choice(emojis)}"
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_random'), types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))

    text = f'✨ *Result:*\n\n`{name}`' if 'pass_' in call.data or 'user_' in call.data else f'✨ *Result:*\n\n{name}'
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
