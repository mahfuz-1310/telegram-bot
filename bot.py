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

# [Data lists same as previous]
# ... (keeping code concise) ...
# (Ensure you keep the full lists of names from the previous version)

def generate_temp_mail():
    # Only using trusted domains that usually work
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = '1secmail.com' # Best for reliable testing
    return f'{username}@hotmail.com', f'{username}@{domain}'

def check_inbox_messages(real_email):
    try:
        login, domain = real_email.split('@')
        url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error: {e}")
    return []

def read_mail_content(real_email, msg_id):
    try:
        login, domain = real_email.split('@')
        url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error: {e}")
    return None

def extract_otp_code(body):
    pattern = r'(?i)(?:code|otp|pin|verification|password|verify)[:\s]*([A-Za-z0-9]{4,8})'
    match = re.search(pattern, body)
    if match: return match.group(1)
    num_match = re.search(r'\b\d{4,6}\b', body)
    return num_match.group(0) if num_match else None

# [Include all other functions from previous version like apply_unicode_font, etc.]
# ...

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # ... (Main Menu logic) ...

    # UPDATED: Improved Mail Logic
    if call.data == 'gen_outlook_mail':
        display_mail, real_mail = generate_temp_mail()
        text = f'📧 *Generated Hotmail Address:*\n\n`{display_mail}`\n\n🕒 *Instruction:*\n১. এই মেইলে ভেরিফিকেশন পাঠান।\n২. ২ মিনিট পর "Refresh Inbox" বাটনে ক্লিক করুন।'
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('📥 Inbox Check', callback_data=f'inbox_{real_mail}'),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data.startswith('inbox_'):
        real_email = call.data.replace('inbox_', '')
        username = real_email.split('@')[0]
        display_email = f'{username}@hotmail.com'
        
        messages = check_inbox_messages(real_email)
        text = f'📧 *Email:* `{display_email}`\n\n'
        markup = types.InlineKeyboardMarkup(row_width=1)

        if messages:
            text += f'📥 *Inbox-e {len(messages)} টি মেসেজ পাওয়া গেছে:*'
            for msg in messages:
                # Add specific identifier for read callback
                markup.add(types.InlineKeyboardButton(f'📩 {msg.get("subject", "No Subject")[:20]}', callback_data=f'read_{real_email}_{msg.get("id")}'))
        else:
            text += '📭 *Inbox is empty!* \n\n*Tips:* ১০-২০ সেকেন্ড অপেক্ষা করে রিফ্রেশ করুন।'
        
        markup.add(
            types.InlineKeyboardButton('🔄 Refresh Inbox', callback_data=call.data),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # ... (Keep remaining code the same) ...
