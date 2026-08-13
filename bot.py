import os
import time
import threading
import telebot
from google import genai

TELEGRAM_TOKEN = "8688685639:AAGwxCmUFihzNQAfX1nt9I570Gt2w2pFGPg"
ADMIN_ID = 7305704935
GEMINI_API_KEY = "AQ.Ab8RN6ILoX5-s9l6sVU9hGDYYr1xVKgq6OPDGUOG9TskLE3yVg"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Generate an advanced exploratory technology report with detailed evidence."
        )
        bot.send_message(ADMIN_ID, f"📊 ARAMKY Report:\n\n{response.text}")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error: {str(e)}")

@bot.message_handler(commands=['generate'])
def start_generation(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Propose an innovative profitable software project idea with advanced architecture."
        )
        bot.send_message(ADMIN_ID, f"💡 Innovation Output:\n\n{response.text}")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"Error: {str(e)}")

@bot.message_handler(func=lambda message: True)
def handle_chat(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        chat_context = f"{SYSTEM_PROMPT}\n\nFriend's message: {message.text}"
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=chat_context
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    print("Server is ON & Ready...")
    bot.infinity_polling(skip_pending=True)
