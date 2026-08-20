import os
import random
import threading
from flask import Flask
import telebot
from telebot import types

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Data Lists (Male and Female separated for better accuracy)
male_first_names = [
    'Aryan', 'Tanvir', 'Rahim', 'Sakib', 'Fahim', 'Nayeem', 'Rakib', 
    'Mehedi', 'Mahin', 'Sabbir', 'Arif', 'Shanto', 'Farhan', 'Niloy', 
    'Siam', 'Hridoy'
]
female_first_names = [
    'Sadia', 'Anika', 'Tasfia', 'Noshin', 'Faria', 'Sumaiya', 'Jannat', 
    'Ishrat', 'Riya', 'Muna', 'Tisha', 'Mim', 'Priya', 'Nusrat'
]
last_names = [
    'Ahmed', 'Hossain', 'Chowdhury', 'Islam', 'Khan', 'Rahman', 'Uddin', 
    'Talukder', 'Hasan', 'Mondol', 'Sarker', 'Biswas', 'Karim', 'Kabir', 'Das'
]
stylish_names = [
    '⚡ Shadow ⚡', '🔥 Vortex 🔥', '👑 King 👑', '💀 Ghost 💀', '💎 Diamond 💎', 
    '🌪️ Storm 🌪️', '⚡ Flash ⚡', '🔥 Blaze 🔥', '❄️ Frost ❄️', '🌙 Eclipse 🌙'
]

# Username generator function with gender parameter
def generate_username(gender):
    if gender == 'male':
        f_name = random.choice(male_first_names).lower()
    else:
        f_name = random.choice(female_first_names).lower()
        
    l_name = random.choice(last_names).lower()
    number = random.randint(10, 999)
    return f'{f_name}_{l_name}{number}'


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    send_main_menu(message)


def send_main_menu(message_or_call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_male = types.InlineKeyboardButton('👦 Boy Name', callback_data='gen_male')
    btn_female = types.InlineKeyboardButton('👧 Girl Name', callback_data='gen_female')
    btn_stylish = types.InlineKeyboardButton('😎 Stylish Name', callback_data='gen_stylish')
    btn_random = types.InlineKeyboardButton('🎲 Random Name', callback_data='gen_random')
    btn_user = types.InlineKeyboardButton('👤 Username Generator', callback_data='username_menu')
    
    markup.add(btn_male, btn_female, btn_stylish, btn_random, btn_user)

    welcome_text = '🌟 *Ultimate Generator Bot*\n\nSelect a category:'
    
    # Check if it's a new message or a callback from a button
    if isinstance(message_or_call, types.Message):
        bot.reply_to(message_or_call, welcome_text, parse_mode='Markdown', reply_markup=markup)
    else:
        bot.edit_message_text(
            welcome_text,
            chat_id=message_or_call.message.chat.id,
            message_id=message_or_call.message.id,
            parse_mode='Markdown',
            reply_markup=markup,
        )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    # Main Menu Callback
    if call.data == 'main_menu':
        send_main_menu(call)
        return

    # Username Sub-Menu Callback
    if call.data == 'username_menu':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_boy = types.InlineKeyboardButton('👦 Boy Username', callback_data='gen_user_male')
        btn_girl = types.InlineKeyboardButton('👧 Girl Username', callback_data='gen_user_female')
        btn_back = types.InlineKeyboardButton('🔙 Back to Menu', callback_data='main_menu')
        markup.add(btn_boy, btn_girl, btn_back)
        
        bot.edit_message_text(
            '👤 *Select Username Gender:*',
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            parse_mode='Markdown',
            reply_markup=markup,
        )
        return

    # Name Generation Logic
    name = ""
    markup = types.InlineKeyboardMarkup(row_width=2)

    if call.data == 'gen_user_male':
        name = generate_username('male')
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_user_male'))
        markup.add(types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
        
    elif call.data == 'gen_user_female':
        name = generate_username('female')
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_user_female'))
        markup.add(types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
        
    elif call.data == 'gen_male':
        name = f'{random.choice(male_first_names)} {random.choice(last_names)}'
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_male'))
        markup.add(types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
        
    elif call.data == 'gen_female':
        name = f'{random.choice(female_first_names)} {random.choice(last_names)}'
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_female'))
        markup.add(types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
        
    elif call.data == 'gen_stylish':
        name = random.choice(stylish_names)
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_stylish'))
        markup.add(types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
        
    elif call.data == 'gen_random':
        all_names = male_first_names + female_first_names
        name = f'{random.choice(all_names)} {random.choice(last_names)}'
        markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_random'))
        markup.add(types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))

    # Send the generated name
    text = f'✨ *Result:*\n\n`{name}`'
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        parse_mode='Markdown',
        reply_markup=markup,
    )


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
