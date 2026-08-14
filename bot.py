import os, telebot, requests
from groq import Groq

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@bot.message_handler(commands=['film'])
def generate_content(message):
    prompt = message.text.replace('/film', '').strip()
    if not prompt:
        bot.reply_to(message, "اكتب فكرتك بعد /film")
        return
    
    msg = bot.reply_to(message, "جاري تحضير المحتوى والمشهد البصري...")
    
    try:
        # 1. توليد السيناريو والحوار
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": f"اكتب سيناريو سينمائي قصير ومختصر للفكرة التالية: {prompt}"}]
        )
        script_text = res.choices[0].message.content
        
        # 2. توليد صورة سينمائية
        img_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1024&height=576&nologo=true"
        
        # 3. إرسال الصورة والسيناريو في رسالتين منفصلتين لتجنب الخطأ
        bot.send_photo(message.chat.id, img_url, caption=f"🎬 المشهد البصري لـ: {prompt}")
        bot.send_message(message.chat.id, f"📝 **السيناريو:**\n\n{script_text}")
        
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {e}")

bot.infinity_polling()
