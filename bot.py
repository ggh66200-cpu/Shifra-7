import os
import telebot
from groq import Groq

# قراءة المتغيرات
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
GROQ_API_KEY = os.getenv('GROQ_API_KEY') # تأكد من استخدام هذا الاسم في Railway

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# تهيئة عميل Groq
client = Groq(api_key=GROQ_API_KEY)

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
    bot.reply_to(message, "🚀 ARAMKY Core (Groq Engine) is online and ready, my friend.")

@bot.message_handler(func=lambda message: True)
def handle_chat(message):
    if message.from_user.id != ADMIN_ID:
        return
    try:
        # إرسال الرسالة إلى Groq
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            temperature=0.7,
        )
        reply_text = completion.choices[0].message.content
        bot.reply_to(message, reply_text)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error Details:\n{str(e)}")

if __name__ == "__main__":
    print("Server is ON & Ready with Groq Engine...")
    bot.infinity_polling(skip_pending=True)
    
