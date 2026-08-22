import os
import random
import string
import threading
from flask import Flask
import telebot
from telebot import types

API_TOKEN = '8994060740:AAFpgfuGajnOA-HLAmae5QmWaypDdRIR_aE'
bot = telebot.TeleBot(API_TOKEN, threaded=True)
app = Flask(__name__)

# Expanded Data Lists for Names and Passwords
male_first_names = [
    'Aryan', 'Tanvir', 'Rahim', 'Sakib', 'Fahim', 'Nayeem', 'Rakib', 'Mehedi', 'Mahin', 'Sabbir', 'Arif', 'Shanto',
    'Imran', 'Tanim', 'Jahid', 'Raihan', 'Faysal', 'Nabil', 'Shihab', 'Ashik', 'Tariq', 'Sohan', 'Rokon', 'Nayem',
    'Arman', 'Rassel', 'Biplob', 'Shohan', 'Parvez', 'Rifat', 'Siam', 'Zihad', 'Al Amin', 'Touhid', 'Rahat',
    'Nafees', 'Adnan', 'Tamim', 'Mashrafe', 'Shakil', 'Sazzad', 'Joy', 'Nibir', 'Fahad', 'Ridoy', 'Alvi', 'Monir',
    'Sujon', 'Ripon', 'Shahed', 'Firoz', 'Masum', 'Belal', 'Sumon', 'Rashed', 'Nazmul', 'Mamun', 'Litón', 'Sohel'
]

female_first_names = [
    'Sadia', 'Anika', 'Tasfia', 'Noshin', 'Faria', 'Sumaiya', 'Jannat', 'Ishrat', 'Riya', 'Muna', 'Tisha', 'Mim',
    'Nusrat', 'Sabrina', 'Mehnaz', 'Farzana', 'Tabassum', 'Tanzina', 'Lamia', 'Maliha', 'Zerin', 'Priya', 'Puja',
    'Farhin', 'Bushra', 'Sanjida', 'Mitu', 'Bristy', 'Nila', 'Tania', 'Sharmin', 'Jerin', 'Fariha', 'Sneha', 'Meem',
    'Nadia', 'Prova', 'Mehjabin', 'Puspita', 'Mou', 'Swarna', 'Sneha', 'Trisha', 'Rumu', 'Porshi', 'Mouri', 'Mimia',
    'Afsana', 'Farha', 'Tania', 'Sultana', 'Jesmin', 'Roksana', 'Shorna', 'Tonima', 'Laboni', 'Nipa', 'Bristy'
]

last_names = [
    'Ahmed', 'Hossain', 'Chowdhury', 'Islam', 'Khan', 'Rahman', 'Uddin', 'Talukder', 'Hasan', 'Sarker',
    'Ali', 'Mollah', 'Bhuiyan', 'Mazumder', 'Siddique', 'Karim', 'Talukdar', 'Mia', 'Biswas', 'Roy',
    'Akther', 'Begum', 'Khatun', 'Dewan', 'Miah', 'Sheikh', 'Bhowmick', 'Sen', 'Das', 'Munshi',
    'Shikder', 'Sarder', 'Pramanik', 'Vhowmick', 'Barua', 'Chakma', 'Golder', 'Hajra', 'Kundu', 'Nag'
]

gamer_tags = ['Shadow', 'Viper', 'Ghost', 'Sniper', 'Ninja', 'Cyber', 'Nexus', 'Blaze', 'Storm', 'Titan', 'Apex', 'Phantom']
cool_words = ['Alpha', 'Beta', 'Zero', 'Dark', 'Swift', 'Prime', 'Elite', 'Legend', 'Savage', 'Cyborg']

bios_list = [
    "👑 King of my own world ✨",
    "🚀 Too glam to give a damn 😎",
    "🔥 Living life on my own terms 💯",
    "🤫 Silent killer in the game ⚡",
    "💫 Born to express, not to impress 🎯",
    "🌟 Dream big, work hard, stay humble 🙏",
    "💎 Reality is wrong, dreams are for real 🌙",
    "⚡ Attitude is my default setting 🔥"
]

nicknames_list = [
    "🔥『 ᴅᴇᴠɪʟ 』🔥",
    "👑 ʙᴀᴅ ʙᴏʏ 👑",
    "⚡ ʟᴇɢᴇɴᴅ ⚡",
    "😎 ꜱᴛʏʟɪꜱʜ ᴋɪɴɢ 😎",
    "💫 ᴍʏꜱᴛᴇʀɪᴏᴜꜱ 💫",
    "🎯 ꜱɴɪᴘᴇʀ ᴋɪɴɢ 🎯",
    "💎 ʀᴏʏᴀʟ ʙᴏʏ 💎",
    "🔥 ꜰɪʀᴇ ꜱᴛᴏʀᴍ 🔥"
]

emojis = ['🔥', '✨', '👑', '😎', '💫', '🌟', '🚀', '🎯', '💯', '⚡', '💎']

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
    return "Bot is running live and smooth!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        send_main_menu(message)
    except Exception as e:
        print(f"Error in welcome: {e}")

def send_main_menu(message_or_call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_male = types.InlineKeyboardButton('👦 Boy Name', callback_data='boy_font_menu')
    btn_female = types.InlineKeyboardButton('👧 Girl Name', callback_data='girl_font_menu')
    btn_stylish = types.InlineKeyboardButton('😎 Stylish Name', callback_data='gen_stylish')
    btn_random = types.InlineKeyboardButton('🎲 Random Name', callback_data='gen_random')
    btn_user = types.InlineKeyboardButton('👤 Username', callback_data='username_menu')
    btn_pass = types.InlineKeyboardButton('🔑 Password', callback_data='password_menu')
    btn_bio = types.InlineKeyboardButton('📝 Bio / Quotes', callback_data='gen_bio')
    btn_nick = types.InlineKeyboardButton('🏷️ Nickname', callback_data='gen_nick')
    
    markup.add(btn_male, btn_female, btn_stylish, btn_random, btn_user, btn_pass, btn_bio, btn_nick)
    text = '🌟 *Ultimate Generator Bot*\n\nSelect a category:'
    
    try:
        if isinstance(message_or_call, types.Message):
            bot.reply_to(message_or_call, text, parse_mode='Markdown', reply_markup=markup)
        else:
            bot.edit_message_text(text, chat_id=message_or_call.message.chat.id, message_id=message_or_call.message.id, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        print(f"Menu error: {e}")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if call.data == 'main_menu':
            send_main_menu(call)
            return

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
                types.InlineKeyboardButton('🎮 Gamer Username', callback_data='user_gamer'),
                types.InlineKeyboardButton('💼 Pro Username', callback_data='user_pro'),
                types.InlineKeyboardButton('😎 Cool Username', callback_data='user_cool'),
                types.InlineKeyboardButton('🎲 Random Username', callback_data='user_random'),
                types.InlineKeyboardButton('🔙 Back to Menu', callback_data='main_menu')
            )
            bot.edit_message_text('👤 *Select Username Style:*', chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
            return

        if call.data == 'password_menu':
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton('🔒 8 Digits', callback_data='pass_8'),
                types.InlineKeyboardButton('🔒 12 Digits', callback_data='pass_12'),
                types.InlineKeyboardButton('🔒 16 Digits', callback_data='pass_16'),
                types.InlineKeyboardButton('🔒 20 Digits', callback_data='pass_20'),
                types.InlineKeyboardButton('🔒 24 Digits', callback_data='pass_24'),
                types.InlineKeyboardButton('🔒 32 Digits', callback_data='pass_32'),
                types.InlineKeyboardButton('🔒 40 Digits', callback_data='pass_40'),
                types.InlineKeyboardButton('🔒 50 Digits', callback_data='pass_50'),
                types.InlineKeyboardButton('🔙 Back to Menu', callback_data='main_menu')
            )
            bot.edit_message_text('🔑 *Select Password Length:*', chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
            return

        # Generators Output Logic
        result_text = ''
        markup = types.InlineKeyboardMarkup(row_width=2)

        if call.data.startswith('boy_'):
            style = call.data.replace('boy_', '')
            raw_name = f"{random.choice(male_first_names)} {random.choice(last_names)}"
            result_text = apply_unicode_font(raw_name, style)
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data), types.InlineKeyboardButton('🔙 Back', callback_data='boy_font_menu'))
        elif call.data.startswith('girl_'):
            style = call.data.replace('girl_', '')
            raw_name = f"{random.choice(female_first_names)} {random.choice(last_names)}"
            result_text = apply_unicode_font(raw_name, style)
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data), types.InlineKeyboardButton('🔙 Back', callback_data='girl_font_menu'))
        elif call.data == 'user_gamer':
            result_text = f"{random.choice(gamer_tags)}_{random.choice(male_first_names).lower()}{random.randint(10,999)}"
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='user_gamer'), types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
        elif call.data == 'user_pro':
            result_text = f"{random.choice(male_first_names + female_first_names).lower()}.{random.choice(last_names).lower()}{random.randint(100,999)}"
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='user_pro'), types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
        elif call.data == 'user_cool':
            result_text = f"x_{random.choice(cool_words).lower()}_{random.choice(male_first_names + female_first_names).lower()}_x"
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='user_cool'), types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
        elif call.data == 'user_random':
            result_text = f"{random.choice(cool_words).lower()}{random.choice(last_names).lower()}{random.randint(1000,9999)}"
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='user_random'), types.InlineKeyboardButton('🔙 Back', callback_data='username_menu'))
        elif call.data.startswith('pass_'):
            length = int(call.data.replace('pass_', ''))
            result_text = ''.join(random.choices(string.ascii_letters + string.digits + '@#$%!', k=length))
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data=call.data), types.InlineKeyboardButton('🔙 Back', callback_data='password_menu'))
        elif call.data == 'gen_bio':
            result_text = random.choice(bios_list)
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_bio'), types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
        elif call.data == 'gen_nick':
            result_text = random.choice(nicknames_list)
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_nick'), types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
        elif call.data == 'gen_stylish':
            f_name = random.choice(male_first_names + female_first_names).lower()
            l_name = random.choice(last_names).lower()
            result_text = f"{f_name} {l_name} 😎⚡"
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_stylish'), types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))
        elif call.data == 'gen_random':
            result_text = f"{random.choice(male_first_names + female_first_names)} {random.choice(last_names)} {random.choice(emojis)}"
            markup.add(types.InlineKeyboardButton('🔄 Generate Again', callback_data='gen_random'), types.InlineKeyboardButton('🏠 Main Menu', callback_data='main_menu'))

        is_code_format = 'pass_' in call.data or call.data.startswith('user_')
        text = f'✨ *Result:*\n\n`{result_text}`' if is_code_format else f'✨ *Result:*\n\n{result_text}'
        
        try:
            bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.id, parse_mode='Markdown', reply_markup=markup)
        except Exception:
            pass
            
    except Exception as e:
        print(f"Callback error: {e}")

def run_bot():
    try:
        bot.remove_webhook()
    except:
        pass
    bot.infinity_polling(timeout=20, long_polling_timeout=10, skip_pending=True)

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
