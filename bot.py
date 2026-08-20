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

# Mail.tm API Functions
def get_mail_tm_domain():
    try:
        res = requests.get("https://api.mail.tm/domains", timeout=10)
        if res.status_code == 200:
            domains = res.json()
            if domains:
                return domains[0]['domain']
    except:
        pass
    return None

def create_mail_tm_account():
    domain = get_mail_tm_domain()
    if not domain:
        return None, None, None
    
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"{username}@{domain}"
    password = "SecurePassword123!"
    
    try:
        res = requests.post("https://api.mail.tm/accounts", json={"address": email, "password": password}, timeout=10)
        if res.status_code in [200, 201]:
            token_res = requests.post("https://api.mail.tm/token", json={"address": email, "password": password}, timeout=10)
            if token_res.status_code == 200:
                token = token_res.json().get('token')
                return email, password, token
    except:
        pass
    return None, None, None

def get_mail_tm_messages(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get("https://api.mail.tm/messages", headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return []

def read_mail_tm_message(token, msg_id):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        res = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers, timeout=10)
        if res.status_code == 200:
            return res.json()
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
    btn_mail = types.InlineKeyboardButton('📧 Mail.tm Temp Mail', callback_data='gen_mailtm')
    
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

    # Mail.tm Handlers
    if call.data == 'gen_mailtm':
        email, password, token = create_mail_tm_account()
        if not email:
            bot.answer_callback_query(call.id, "Failed to create mail. Try again!")
            return
        
        text = f'📧 *Generated Mail:*\n\n`{email}`\n\n📥 *Inbox check korte nicher button-e click korun:*'
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton('📥 Inbox Check', callback_data=f'inbox_{token}_{email}'),
            types.InlineKeyboardButton('🔄 New Mail', callback_data='gen_mailtm'),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data.startswith('inbox_'):
        parts = call.data.split('_', 2)
        token = parts[1]
        email = parts[2]
        
        messages = get_mail_tm_messages(token)
        text = f'📧 *Email:* `{email}`\n\n'
        markup = types.InlineKeyboardMarkup(row_width=1)

        if messages:
            text += f'📥 *Inbox-e {len(messages)} টি মেসেজ পাওয়া গেছে:*'
            for msg in messages:
                markup.add(types.InlineKeyboardButton(f'📩 {msg.get("subject", "No Subject")[:20]}', callback_data=f'read_{token}_{msg.get("id")}_{email}'))
        else:
            text += '📭 *Inbox is empty! (Waiting for messages)*'
        
        markup.add(
            types.InlineKeyboardButton('🔄 Refresh Inbox', callback_data=call.data),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data.startswith('read_'):
        parts = call.data.split('_', 3)
        token = parts[1]
        msg_id = parts[2]
        email = parts[3]
        
        msg_data = read_mail_tm_message(token, msg_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if msg_data:
            sender = msg_data.get('from', {}).get('address', 'Unknown')
            subject = msg_data.get('subject', 'No Subject')
            body = msg_data.get('text', 'No text content available.')
            text = f'📩 *From:* `{sender}`\n📌 *Subject:* `{subject}`\n\n💬 *Body:*\n`{body[:400]}`'
            markup.add(types.InlineKeyboardButton('🔑 Get Code', callback_data=f'code_{token}_{msg_id}_{email}'))
        else:
            text = '❌ Message read failed.'
        markup.add(types.InlineKeyboardButton('🔙 Back to Inbox', callback_data=f'inbox_{token}_{email}'))
        
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data.startswith('code_'):
        parts = call.data.split('_', 3)
        token = parts[1]
        msg_id = parts[2]
        email = parts[3]
        
        msg_data = read_mail_tm_message(token, msg_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('🔙 Back to Message', callback_data=f'read_{token}_{msg_id}_{email}'))
        
        if msg_data:
            body = msg_data.get('text', '')
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
