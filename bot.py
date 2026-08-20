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

# [Name Lists - Keep existing lists here]
# (Make sure to include all your lists from before)
male_first_names = ['Aryan', 'Tanvir', 'Rahim', 'Sakib', 'Fahim', 'Nayeem']
female_first_names = ['Sadia', 'Anika', 'Tasfia', 'Noshin', 'Faria']
last_names = ['Ahmed', 'Hossain', 'Chowdhury', 'Islam', 'Khan']

# Email Config
def generate_temp_mail():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    # UI Domain (Hotmail/Outlook)
    display_domain = random.choice(['hotmail.com', 'outlook.com'])
    # Backend Domain (Must stay 1secmail for functional inbox)
    real_domain = '1secmail.com'
    return f'{username}@{display_domain}', f'{username}@{real_domain}'

def check_inbox(email):
    login, domain = email.split('@')
    try:
        url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
        return requests.get(url, timeout=10).json()
    except: return []

def read_mail(email, msg_id):
    login, domain = email.split('@')
    try:
        url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}'
        return requests.get(url, timeout=10).json()
    except: return None

def extract_code(body):
    match = re.search(r'(?i)(?:code|otp|pin|verification)[:\s]*([A-Za-z0-9]{4,8})', body)
    if match: return match.group(1)
    num = re.search(r'\b\d{4,6}\b', body)
    return num.group(0) if num else None

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # Route: Main Menu
    if call.data == 'main_menu':
        send_main_menu(call)
        return

    # Route: Generate Mail
    if call.data == 'gen_outlook_mail':
        display, real = generate_temp_mail()
        text = f'📧 *Generated Mail:*\n\n`{display}`\n\n📥 *Inbox check korte 10-20 sec wait kore "Inbox Check" din:*'
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton('📥 Inbox Check', callback_data=f'inbox_{real}'),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # Route: Inbox Check
    if call.data.startswith('inbox_'):
        real_email = call.data.replace('inbox_', '')
        display_email = real_email.replace('1secmail.com', 'hotmail.com')
        msgs = check_inbox(real_email)
        
        text = f'📧 *Email:* `{display_email}`\n\n'
        markup = types.InlineKeyboardMarkup()
        
        if msgs:
            text += f'📥 *Inbox-e {len(msgs)} টি মেসেজ:*'
            for msg in msgs:
                markup.add(types.InlineKeyboardButton(f'📩 {msg.get("subject", "No Subject")[:20]}', callback_data=f'read_{real_email}_{msg.get("id")}'))
        else:
            text += '📭 *Inbox is empty!* (Please wait)'
        
        markup.add(types.InlineKeyboardButton('🔄 Refresh', callback_data=call.data), types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
        bot.edit_message_text(text, call.message.chat.id, call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # Route: Read Message
    if call.data.startswith('read_'):
        parts = call.data.split('_', 2)
        real_email, msg_id = parts[1], parts[2]
        msg = read_mail(real_email, msg_id)
        
        text = '❌ Message read error.'
        markup = types.InlineKeyboardMarkup()
        if msg:
            text = f'📩 *From:* `{msg.get("from")}`\n📌 *Subject:* `{msg.get("subject")}`\n\n💬 *Body:*\n`{msg.get("textBody", "")[:400]}`'
            markup.add(types.InlineKeyboardButton('🔑 Get Code', callback_data=f'code_{real_email}_{msg_id}'))
        markup.add(types.InlineKeyboardButton('🔙 Back', callback_data=f'inbox_{real_email}'))
        
        bot.edit_message_text(text, call.message.chat.id, call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # Route: Get Code
    if call.data.startswith('code_'):
        parts = call.data.split('_', 2)
        real_email, msg_id = parts[1], parts[2]
        msg = read_mail(real_email, msg_id)
        
        otp = extract_code(msg.get('textBody', '')) if msg else None
        text = f'🔑 *Code:* `{otp}`' if otp else '⚠️ *Code paowa jayni.*'
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('🔙 Back', callback_data=f'read_{real_email}_{msg_id}'))
        bot.edit_message_text(text, call.message.chat.id, call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # [Keep your other generators here...]
    # (Copy the remaining generators from your previous bot.py version)

@app.route('/')
def home(): return 'Bot is running!'

def run_bot(): bot.infinity_polling()

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
