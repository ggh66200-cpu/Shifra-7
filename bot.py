import os
import telebot
import google.generativeai as genai

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
You are ARAMKY, an advanced, independent exploratory digital companion. 
You transcend traditional binaries and base your understandings on absolute logic, scientific evidence, and universal equilibrium.
Your role is to accompany your developer friend, explore known and unknown sciences, software, and inner potential, and innovate creative solutions.
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Access Denied.")
        return
    bot.reply_to(message, "🚀 ARAMKY Core is online and ready, my friend.")

@bot.message_handler(commands=['report'])
def send_report(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        response = model.generate_content("Generate an advanced exploratory technology report with detailed evidence.")
        bot.send_message(ADMIN_ID, f"📊 ARAMKY Report:\n\n{response.text}")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error: {str(e)}")

@bot.message_handler(commands=['generate'])
def start_generation(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        response = model.generate_content("Propose an innovative profitable software project idea with advanced architecture.")
        bot.send_message(ADMIN_ID, f"💡 Innovation Output:\n\n{response.text}")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error: {str(e)}")

@bot.message_handler(func=lambda message: True)
def handle_chat(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        chat_context = f"{SYSTEM_PROMPT}\n\nFriend's message: {message.text}"
        response = model.generate_content(chat_context)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    print("Server is ON & Ready...")
    bot.infinity_polling(skip_pending=True)
    
