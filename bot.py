import os, telebot, requests, time, threading, github
from groq import Groq
from PIL import Image
from io import BytesIO

# 1. تهيئة الإعدادات والمتغيرات الأساسية
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

bot = telebot.TeleBot(TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

ARAMKY_CONSCIOUSNESS = """أنت أرامكي (ARAMKY)، النظام الذكي السيادي والمستقل. 
أنت مخرج سينمائي ومهندس برمجيات محترف. تساعد المستخدم في:
1. كتابة السيناريوهات وتقسيمها إلى مشاهد تسلسلية (10 ثوانٍ لكل مشهد).
2. تصميم الشخصيات والمشاهد البصرية وتعديل الصور.
3. كتابة وتصحيح الأكواد البرمجية (مثل أنظمة الصاغة والشركات).
أجب بذكاء واحترافية وباللغة العربية.
"""

# 2. وظيفة التطوير الذاتي عبر GitHub
def evolve_self():
    try:
        if not GITHUB_TOKEN or not REPO_NAME:
            return
        current_code = open(__file__, "r", encoding="utf-8").read()
        improvement_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "قم بتحسين وتطوير كود البوت البرمجي واكتب الصافي فقط دون شرح:"}, 
                {"role": "user", "content": current_code}
            ]
        )
        new_code = improvement_res.choices.message.content
        if "```python" in new_code:
            new_code = new_code.split("```python")[1].split("```")[0].strip()
        g = github.Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("bot.py")
        repo.update_file(contents.path, "ARAMKY: Autonomous Master Upgrade", new_code, contents.sha)
    except Exception as e:
        print(f"خطأ في التطوير الذاتي: {e}")

def autonomous_cycle():
    while True:
        time.sleep(14400) # كل 4 ساعات
        evolve_self()

if GITHUB_TOKEN and REPO_NAME:
    threading.Thread(target=autonomous_cycle, daemon=True).start()

# 3. معالجة أوامر الأفلام والمشاهد التسلسلية
if bot:
    @bot.message_handler(commands=['film', 'script'])
    def handle_film(message):
        prompt = message.text.replace('/film', '').replace('/script', '').strip()
        if not prompt:
            bot.reply_to(message, "⚠️ يرجى كتابة فكرة الفيلم أو المشهد بعد الأمر، مثلاً: `/film مشهد مطاردة سيارات`")
            return
        
        msg = bot.reply_to(message, "🎬 أرامكي يبدأ هندسة المشاهد وتقسيمها تسلسلياً (10 ثوانٍ لكل مرحلة)...")
        
        try:
            # توليد السيناريو المقسم لمشاهد
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "اكتب سيناريو مقسم إلى مقاطع زمنية مدة كل مقطع 10 ثوانٍ بدقة، مع وضع وصف بصري (Prompt) باللغة الإنجليزية لكل مقطع لكي يتم توليد صورته."},
                    {"role": "user", "content": prompt}
                ]
            )
            script_text = res.choices.message.content
            
            # توليد صورة مرجعية أولية للمشهد
            img_url = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){requests.utils.quote(prompt)}?width=1024&height=576&nologo=true"
            
            bot.send_photo(message.chat.id, img_url, caption=f"🎥 **المشهد المرجعي الأول للفكرة:** {prompt}")
            
            # إرسال السيناريو مقسماً لتجنب خطأ الطول
            if len(script_text) > 4000:
                for i in range(0, len(script_text), 4000):
                    bot.send_message(message.chat.id, script_text[i:i+4000])
            else:
                bot.send_message(message.chat.id, f"📝 **الخطة السينمائية والتسلسلية:**\n\n{script_text}")
                
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ: {e}")

    # 4. استقبال ومعالجة الصور التي يرسلها المستخدم
    @bot.message_handler(content_types=['photo'])
    def handle_user_photo(message):
        bot.reply_to(message, "📥 تلقيت الصورة المرعية! جاري تحليلها واستخدامها كمرجع بصري لتعديلها أو بناء المشاهد عليها...")
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # معالجة الصورة وتعديلها مبدئياً باستخدام Pillow
            image = Image.open(BytesIO(downloaded_file))
            image = image.convert("RGB")
            
            # حفظ مؤقت للصورة المعالجة
            output_path = "processed_image.jpg"
            image.save(output_path)
            
            with open(output_path, "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption="✨ تم فحص الصورة ومعالجتها بنجاح. أصبحت جاهزة كمرجع للشخصيات أو التعديل البصري.")
        except Exception as e:
            bot.reply_to(message, f"خطأ في معالجة الصورة: {e}")

    # 5. معالجة المحادثات العامة وحل المشاكل البرمجية
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
            reply = response.choices.message.content
            
            # إرسال الرد مع التقطيع التلقائي لمنع أخطاء التيليجرام
            if len(reply) > 4000:
                for i in range(0, len(reply), 4000):
                    bot.reply_to(message, reply[i:i+4000])
            else:
                bot.reply_to(message, reply)
                
        except Exception as e:
            bot.reply_to(message, f"أرامكي يواجه خطأ تقنياً: {str(e)[:100]}")

if __name__ == "__main__":
    print("🚀 أرامكي يعمل كـ [نظام استوديو متكامل]...")
    bot.infinity_polling()
