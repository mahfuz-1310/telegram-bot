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

# [Name Lists - Keep your existing lists here]
male_first_names = ['Aryan', 'Tanvir', 'Rahim', 'Sakib', 'Fahim', 'Nayeem', 'Rakib', 'Mehedi']
female_first_names = ['Sadia', 'Anika', 'Tasfia', 'Noshin', 'Faria', 'Sumaiya', 'Jannat', 'Ishrat']
last_names = ['Ahmed', 'Hossain', 'Chowdhury', 'Islam', 'Khan', 'Rahman', 'Uddin', 'Talukder']
emojis = ['🔥', '✨', '👑', '😎', '💫', '🌟', '🚀', '🎯', '💯', '⚡', '💎']
mail_words1 = ['grey', 'dark', 'cool', 'swift', 'frost', 'shadow', 'neon', 'iron', 'alpha']
mail_words2 = ['savage', 'knight', 'coder', 'gamer', 'wolf', 'dragon', 'storm', 'ninja']
mail_words3 = ['cedc', 'pro', 'x', 'zen', 'bot', 'hub', 'net', 'sec']

def generate_temp_mail():
    username = f'{random.choice(mail_words1)}{random.choice(mail_words2)}{random.choice(mail_words3)}'
    # Display domain for user
    display_domain = random.choice(['hotmail.com', 'outlook.com'])
    # Backend domain for functionality
    real_domain = '1secmail.com' 
    return f'{username}@{display_domain}', f'{username}@{real_domain}'

def check_inbox_messages(real_email):
    try:
        login, domain = real_email.split('@')
        url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except: pass
    return []

def read_mail_content(real_email, msg_id):
    try:
        login, domain = real_email.split('@')
        url = f'https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except: pass
    return None

def extract_otp_code(body):
    pattern = r'(?i)(?:code|otp|pin|verification|password|verify)[:\s]*([A-Za-z0-9]{4,8})'
    match = re.search(pattern, body)
    if match: return match.group(1)
    num_match = re.search(r'\b\d{4,6}\b', body)
    return num_match.group(0) if num_match else None

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'main_menu':
        send_main_menu(call)
        return

    # GENERATE MAIL LOGIC (FORCING HOTMAIL/OUTLOOK)
    if call.data == 'gen_outlook_mail':
        display_mail, real_mail = generate_temp_mail()
        text = f'📧 *Generated Email Address:*\n\n`{display_mail}`\n\n📥 *Inbox check korte nicher button-e click korun:*'
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton('📥 Inbox Check', callback_data=f'inbox_{real_mail}_{display_mail}'),
            types.InlineKeyboardButton('🔄 New Mail', callback_data='gen_outlook_mail'),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # INBOX LOGIC
    if call.data.startswith('inbox_'):
        parts = call.data.split('_', 2)
        real_email, display_email = parts[1], parts[2]
        
        messages = check_inbox_messages(real_email)
        text = f'📧 *Email:* `{display_email}`\n\n'
        markup = types.InlineKeyboardMarkup(row_width=1)

        if messages:
            text += f'📥 *Inbox-e {len(messages)} টি মেসেজ পাওয়া গেছে:*'
            for msg in messages:
                markup.add(types.InlineKeyboardButton(f'📩 {msg.get("subject", "No Subject")[:20]}', callback_data=f'read_{real_email}_{display_email}_{msg.get("id")}'))
        else:
            text += '📭 *Inbox is empty! (Please wait for OTP)*'
        
        markup.add(
            types.InlineKeyboardButton('🔄 Refresh Inbox', callback_data=call.data),
            types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
        )
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # READ LOGIC
    if call.data.startswith('read_'):
        parts = call.data.split('_', 3)
        real_email, display_email, msg_id = parts[1], parts[2], parts[3]
        msg_data = read_mail_content(real_email, msg_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton('🔑 Get Code', callback_data=f'code_{real_email}_{display_email}_{msg_id}'),
            types.InlineKeyboardButton('🔙 Back to Inbox', callback_data=f'inbox_{real_email}_{display_email}')
        )
        
        text = '❌ Message read failed.'
        if msg_data:
            text = f'📩 *From:* `{msg_data.get("from")}`\n📌 *Subject:* `{msg_data.get("subject")}`\n\n💬 *Body:*\n`{msg_data.get("textBody", "")[:400]}`'
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

    # GET CODE LOGIC
    if call.data.startswith('code_'):
        parts = call.data.split('_', 3)
        real_email, display_email, msg_id = parts[1], parts[2], parts[3]
        msg_data = read_mail_content(real_email, msg_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton('🔙 Back to Message', callback_data=f'read_{real_email}_{display_email}_{msg_id}'))
        
        if msg_data:
            otp = extract_otp_code(msg_data.get('textBody', ''))
            text = f'🔑 *Verification Code:* `{otp}`' if otp else '⚠️ *Code paowa jayni, body manually check korun.*'
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        return

# [Keep your other existing functions (apply_unicode_font, send_welcome, etc) as they were]
