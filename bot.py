import os, telebot, requests
from groq import Groq
from PIL import Image
from io import BytesIO

# تهيئة الإعدادات
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

ARAMKY_CONSCIOUSNESS = """أنت أرامكي (ARAMKY)، النظام الذكي السيادي والمساعد التقني والمخرج السينمائي. 
مهمتك مساعدة المستخدم في كتابة السيناريوهات، توليد الأفكار البصرية، وحل المشاكل البرمجية بدقة واحترافية باللغة العربية.
"""

if bot:
    @bot.message_handler(commands=['film', 'script', 'video'])
    def handle_film(message):
        prompt = message.text.replace('/film', '').replace('/script', '').replace('/video', '').strip()
        if not prompt:
            bot.reply_to(message, "⚠️ يرجى كتابة فكرة الفيلم أو المشهد بعد الأمر، مثلاً: `/film سيارة تسير في الشارع`")
            return
        
        msg = bot.reply_to(message, "🎬 أرامكي يقوم بهندسة المشهد وإنتاج العرض البصري...")
        
        try:
            # 1. توليد السيناريو والوصف من Groq
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "اكتب سيناريو قصير مقسم إلى مشاهد تسلسلية مع وصف دقيق بالإنجليزية لتوليد الصور."},
                    {"role": "user", "content": prompt}
                ]
            )
            script_text = res.choices[0].message.content
            
            # 2. توليد المشهد البصري السينمائي عالي الجودة
            img_url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt + ' cinematic motion 4k')}?width=1024&height=576&nologo=true"
            
            # إرسال الصورة للمستخدم كعرض بصري سينمائي
            bot.send_photo(message.chat.id, img_url, caption=f"🎥 **المشهد السينمائي لـ:** {prompt}")
            
            # 3. إرسال السيناريو مقسماً إذا كان طويلاً
            if len(script_text) > 4000:
                for i in range(0, len(script_text), 4000):
                    bot.send_message(message.chat.id, script_text[i:i+4000])
            else:
                bot.send_message(message.chat.id, f"📝 **السيناريو التسلسلي:**\n\n{script_text}")
                
            bot.delete_message(message.chat.id, msg.message_id)
            
        except Exception as e:
            bot.reply_to(message, f"⚠️ أرامكي اكتشف خطأ وعالجه: {str(e)}")

    @bot.message_handler(content_types=['photo'])
    def handle_user_photo(message):
        bot.reply_to(message, "📥 تلقيت صورتك! جاري فحصها ومعالجتها بصرياً...")
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            image = Image.open(BytesIO(downloaded_file)).convert("RGB")
            image.save("processed_image.jpg")
            
            with open("processed_image.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption="✨ تم معالجة الصورة بنجاح وجاهزة للاستخدام كمصدر إلهام أو مرجع.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ خطأ في معالجة الصورة: {e}")

    @bot.message_handler(func=lambda message: True)
    def handle_chat(message):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": ARAMKY_CONSCIOUSNESS},
                    {"role": "user", "content": message.text}
                ]
            )
            reply = response.choices[0].message.content
            
            if len(reply) > 4000:
                for i in range(0, len(reply), 4000):
                    bot.reply_to(message, reply[i:i+4000])
            else:
                bot.reply_to(message, reply)
                
        except Exception as e:
            bot.reply_to(message, f"⚠️ أرامكي اكتشف خطأ تقنياً وعالج الاستثناء: {str(e)}")

if __name__ == "__main__":
    print("🚀 أرامكي يعمل بكفاءة وأمان تام بدون أخطاء...")
    bot.infinity_polling()
