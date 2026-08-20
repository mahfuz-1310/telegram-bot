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

@app.route('/')
def home():
    return "Mail.tm Bot is running live!"

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
        # Create Account
        res = requests.post("https://api.mail.tm/accounts", json={"address": email, "password": password}, timeout=10)
        if res.status_code in [200, 201]:
            # Get Token
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

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    send_main_menu(message)

def send_main_menu(message_or_call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('📧 Generate Mail.tm Email', callback_data='gen_mailtm'),
        types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
    )
    text = '🌟 *Mail.tm Temp Mail Bot*\n\nClick below to generate a working temporary email:'
    
    if isinstance(message_or_call, types.Message):
        bot.reply_to(message_or_call, text, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.edit_message_text(text, chat_id=message_or_call.message.chat.id, message_id=message_or_call.message.id, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'main_menu':
        send_main_menu(call)
        return

    if call.data == 'gen_mailtm':
        email, password, token = create_mail_tm_account()
        if not email:
            bot.answer_callback_query(call.id, "Failed to create mail. Try again!")
            return
        
        text = f'📧 *Generated Mail:*\n\n`{email}`\n\n📥 *Inbox check korte nicher button-e click korun:*'
        markup = types.InlineKeyboardMarkup(row_width=1)
        # Storing token securely in callback data or use alternative mapping (passing token in callback for simplicity)
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
