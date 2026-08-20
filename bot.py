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

# [Name Lists remain the same as previous...]
# (Keeping code concise by using existing lists)
male_first_names = ['Aryan', 'Tanvir', 'Rahim', 'Sakib', 'Fahim', 'Nayeem', 'Rakib', 'Mehedi']
female_first_names = ['Sadia', 'Anika', 'Tasfia', 'Noshin', 'Faria', 'Sumaiya', 'Jannat', 'Ishrat']
last_names = ['Ahmed', 'Hossain', 'Chowdhury', 'Islam', 'Khan', 'Rahman', 'Uddin', 'Talukder']
emojis = ['🔥', '✨', '👑', '😎', '💫', '🌟', '🚀', '🎯', '💯', '⚡', '💎']

def generate_temp_mail():
    # Using more reliable domains
    domains = ['1secmail.com', '1secmail.org', '1secmail.net']
    domain = random.choice(domains)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f'{username}@{domain}'

def check_inbox_messages(email):
    try:
        login, domain = email.split('@')
        url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error checking inbox: {e}")
    return []

def read_mail_content(email, msg_id):
    try:
        login, domain = email.split('@')
        url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error reading mail: {e}")
    return None

def extract_otp_code(body):
    # Improved regex for finding OTP
    otp_patterns = [
        r'\b\d{4,8}\b', # Any 4-8 digit number
        r'(?i)(?:code|otp|verification)[:\s]*([A-Za-z0-9]{4,8})'
    ]
    for pattern in otp_patterns:
        match = re.search(pattern, body)
        if match:
            # If pattern has group, return group 1, else return whole match
            return match.group(1) if match.groups() else match.group(0)
    return None

# [Rest of the functions and bot handlers remain similar, just ensure the read_mail_content logic is updated as below]

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'main_menu':
        send_main_menu(call)
        return

    # ... (Keep other handlers as they were) ...

    # UPDATED Read Specific Message Logic
    if call.data.startswith('read_'):
        parts = call.data.split('_', 2)
        email = parts[1]
        msg_id = parts[2]

        msg_data = read_mail_content(email, msg_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # Always add Get Code button so user can try extraction
        markup.add(
            types.InlineKeyboardButton('🔑 Get Code', callback_data=f'code_{email}_{msg_id}'),
            types.InlineKeyboardButton('🔙 Back to Inbox', callback_data=f'inbox_{email}')
        )

        if msg_data:
            sender = msg_data.get('from', 'Unknown')
            subject = msg_data.get('subject', 'No Subject')
            body = msg_data.get('textBody', 'No text content available.')
            text = f'📩 *From:* `{sender}`\n📌 *Subject:* `{subject}`\n\n💬 *Body:*\n`{body[:500]}`'
        else:
            text = '❌ Message read korte shomossha hoyeche. Server slow thakte pare.'

        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # UPDATED Get Code Logic
    if call.data.startswith('code_'):
        parts = call.data.split('_', 2)
        email = parts[1]
        msg_id = parts[2]
        msg_data = read_mail_content(email, msg_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('🔙 Back to Message', callback_data=f'read_{email}_{msg_id}'))

        if msg_data:
            body = msg_data.get('textBody', '')
            otp = extract_otp_code(body)
            if otp:
                text = f'🔑 *Found Code:* `{otp}`'
            else:
                text = '⚠️ *Code paowa jayni!* Message-ti manually pore dekhun.'
        else:
            text = '❌ Message fetch korte shomossha hoyeche.'
            
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # ... (Keep other handlers as they were) ...
