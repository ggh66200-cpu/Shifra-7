import os, telebot, requests
from groq import Groq

# الإعدادات: ضع التوكنز فقط، بدون تعقيد
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أرامكي جاهز. اطلب أي فكرة (مثلاً: /film كوكب ذهبي) وسأقوم بتوليد الصورة والسيناريو فوراً.")

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
            messages=[{"role": "user", "content": f"اكتب سيناريو سينمائي قصير وإبداعي للفكرة التالية: {prompt}"}]
        )
        
        # 2. توليد صورة سينمائية معبرة (مباشرة)
        img_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}?width=1024&height=576&nologo=true"
        
        # 3. إرسال الكل
        bot.send_photo(message.chat.id, img_url, caption=f"🎬 **السيناريو:**\n\n{res.choices[0].message.content}")
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.reply_to(message, f"خطأ: {e}")

bot.infinity_polling()
