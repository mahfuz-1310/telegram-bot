import os
import random
import threading
from flask import Flask
import telebot
from telebot import types

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Data Lists
male_names = ['Aryan Ahmed', 'Tanvir Hossain', 'Rahim Chowdhury', 'Sakib Islam', 'Fahim Khan', 'Nayeem Rahman', 'Rakib Hasan', 'Mehedi Sarker', 'Mahin Biswas', 'Sabbir Karim', 'Arif Kabir', 'Shanto Das', 'Farhan Majumder', 'Niloy Miah', 'Siam Sheikh', 'Hridoy Bhuiyan']
female_names = ['Sadia Ahmed', 'Anika Hossain', 'Tasfia Chowdhury', 'Noshin Islam', 'Faria Khan', 'Sumaiya Rahman', 'Jannat Hasan', 'Ishrat Mondol', 'Riya Sarker', 'Muna Biswas', 'Tisha Deb', 'Mim Karim', 'Priya Das', 'Nusrat Barua', 'Mehzabien Haider']
stylish_names = ['⚡ Shadow ⚡', '🔥 Vortex 🔥', '👑 King 👑', '💀 Ghost 💀', '💎 Diamond 💎', '🌪️ Storm 🌪️', '⚡ Flash ⚡', '🔥 Blaze 🔥', '❄️ Frost ❄️', '🌙 Eclipse 🌙']

# Username lists for Generator
adjectives = ['Swift', 'Happy', 'Silent', 'Dark', 'Cool', 'Neon', 'Iron', 'Cyber', 'Mega', 'Lunar', 'Mystic', 'Turbo']
nouns = ['Dragon', 'Tiger', 'Wizard', 'Bot', 'Player', 'Coder', 'Phoenix', 'Knight', 'Storm', 'Force', 'Ninja', 'Rider']

def generate_username():
    return f"{random.choice(adjectives)}{random.choice(nouns)}{random.randint(10, 999)}"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    send_main_menu(message)

def send_main_menu(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_male = types.InlineKeyboardButton('👦 Boy', callback_data='gen_male')
    btn_female = types.InlineKeyboardButton('👧 Girl', callback_data='gen_female')
    btn_stylish = types.InlineKeyboardButton('😎 Stylish', callback_data='gen_stylish')
    btn_random = types.InlineKeyboardButton('🎲 Random', callback_data='gen_random')
    btn_user = types.InlineKeyboardButton('👤 Username', callback_data='gen_username')
    markup.add(btn_male, btn_female, btn_stylish, btn_random, btn_user)

    welcome_text = '🌟 *Ultimate Generator Bot*\n\nSelect a category:'
    if hasattr(message, 'message_id'):
        bot.edit_message_text(welcome_text, chat_id=message.chat.id, message_id=message.message_id, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'main_menu':
        send_main_menu(call.message)
        return

    if call.data == 'gen_username':
        name = generate_username()
    elif call.data == 'gen_male':
        name = random.choice(male_names)
    elif call.data == 'gen_female':
        name = random.choice(female_names)
    elif call.data == 'gen_stylish':
        name = random.choice(stylish_names)
    else:
        name = f"{random.choice(['Aryan', 'Sadia'])} {random.choice(['Ahmed', 'Khan'])}"

    text = f'✨ *Result:*\n\n`{name}`'
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_again = types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data)
    btn_menu = types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu')
    markup.add(btn_again, btn_menu)

    bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)

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
