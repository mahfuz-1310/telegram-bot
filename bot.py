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

# [Name Lists and Global Variables remain same]
male_first_names = ['Aryan', 'Tanvir', 'Rahim', 'Sakib', 'Fahim', 'Nayeem', 'Rakib', 'Mehedi']
female_first_names = ['Sadia', 'Anika', 'Tasfia', 'Noshin', 'Faria', 'Sumaiya', 'Jannat', 'Ishrat']
last_names = ['Ahmed', 'Hossain', 'Chowdhury', 'Islam', 'Khan', 'Rahman', 'Uddin', 'Talukder']
emojis = ['🔥', '✨', '👑', '😎', '💫', '🌟', '🚀', '🎯', '💯', '⚡', '💎']
mail_words1 = ['grey', 'dark', 'cool', 'swift', 'frost', 'shadow', 'neon', 'iron', 'alpha']
mail_words2 = ['savage', 'knight', 'coder', 'gamer', 'wolf', 'dragon', 'storm', 'ninja']
mail_words3 = ['cedc', 'pro', 'x', 'zen', 'bot', 'hub', 'net', 'sec']

def generate_username(gender):
    f_name = random.choice(male_first_names if gender == 'male' else female_first_names).lower()
    return f'{f_name}_{random.choice(last_names).lower()}{random.randint(10, 999)}'

def generate_password(length):
    chars = string.ascii_letters + string.digits + '@#$%&!-_'
    return ''.join(random.choice(chars) for _ in range(length))

# Custom Hotmail/Outlook Mail Generator
def generate_temp_mail():
    username = f'{random.choice(mail_words1)}{random.choice(mail_words2)}{random.choice(mail_words3)}'
    
    # UI Domain (Hotmail/Outlook)
    display_domain = random.choice(['hotmail.com', 'outlook.com'])
    # Backend API Domain (Must use 1secmail for working inbox)
    api_domain = '1secmail.com' 
    
    return f'{username}@{display_domain}', f'{username}@{api_domain}'

def check_inbox_messages(real_email):
    try:
        login, domain = real_email.split('@')
        url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def read_mail_content(real_email, msg_id):
    try:
        login, domain = real_email.split('@')
        url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def extract_otp_code(body):
    # Regex to find 4-8 digit codes or words followed by codes
    pattern = r'(?i)(?:code|otp|pin|verification|password|verify)[:\s]*([A-Za-z0-9]{4,8})'
    match = re.search(pattern, body)
    if match:
        return match.group(1)
    # Simple fallback: find any 4-6 digit number
    num_match = re.search(r'\b\d{4,6}\b', body)
    return num_match.group(0) if num_match else None

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'main_menu':
        send_main_menu(call)
        return

    # Outlook/Hotmail Mail Generation Logic
    if call.data == 'gen_outlook_mail':
        display_mail, real_mail = generate_temp_mail()
        # Storing real_mail for backend processing
        text = f'📧 *Generated Hotmail/Outlook Address:*\n\n`{display_mail}`\n\n📥 *Inbox check korte nicher button-e click korun:*'
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('📥 Inbox Check', callback_data=f'inbox_{real_mail}'),
            types.InlineKeyboardButton('🔄 New Mail', callback_data='gen_outlook_mail'),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    if call.data.startswith('inbox_'):
        real_email = call.data.replace('inbox_', '')
        username = real_email.split('@')[0]
        # Show hotmail/outlook in display
        display_email = f'{username}@hotmail.com' 
        
        messages = check_inbox_messages(real_email)
        text = f'📧 *Email:* `{display_email}`\n\n'
        markup = types.InlineKeyboardMarkup(row_width=1)

        if messages:
            text += f'📥 *Inbox-e {len(messages)} টি মেসেজ পাওয়া গেছে:*'
            for msg in messages:
                markup.add(types.InlineKeyboardButton(f'📩 {msg.get("subject", "No Subject")[:20]}', callback_data=f'read_{real_email}_{msg.get("id")}'))
        else:
            text += '📭 *Inbox is empty! (Please wait for OTP)*'
        
        markup.add(
            types.InlineKeyboardButton('🔄 Refresh Inbox', callback_data=call.data),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # Read Specific Message
    if call.data.startswith('read_'):
        parts = call.data.split('_', 2)
        real_email, msg_id = parts[1], parts[2]
        msg_data = read_mail_content(real_email, msg_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton('🔑 Get Code', callback_data=f'code_{real_email}_{msg_id}'),
            types.InlineKeyboardButton('🔙 Back to Inbox', callback_data=f'inbox_{real_email}')
        )
        
        text = '❌ Message read failed.'
        if msg_data:
            text = f'📩 *From:* `{msg_data.get("from")}`\n📌 *Subject:* `{msg_data.get("subject")}`\n\n💬 *Body:*\n`{msg_data.get("textBody", "")[:400]}`'
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # Get Code Logic
    if call.data.startswith('code_'):
        parts = call.data.split('_', 2)
        real_email, msg_id = parts[1], parts[2]
        msg_data = read_mail_content(real_email, msg_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('🔙 Back', callback_data=f'read_{real_email}_{msg_id}'))
        
        if msg_data:
            otp = extract_otp_code(msg_data.get('textBody', ''))
            text = f'🔑 *Verification Code:* `{otp}`' if otp else '⚠️ *Code paowa jayni, body manually check korun.*'
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # ... (Keep other generators like boy/girl names as they were) ...
