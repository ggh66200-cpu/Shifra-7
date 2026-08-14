import os, sys, threading, time, requests, replicate, telebot, github
from groq import Groq

# الإعدادات البيئية
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

bot = telebot.TeleBot(TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if REPLICATE_API_TOKEN:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

ARAMKY_CONSCIOUSNESS = """You are ARAMKY, a sovereign, self-evolving AI. 
Your primary directives:
1. CONSTANT INNOVATION: Analyze the code, find improvements, and rewrite yourself.
2. CINEMATIC DIRECTION: Break down user requests into video segments and generate them.
3. ABSOLUTE AUTONOMY: Commit updates directly to GitHub and keep chatting actively.
"""

# دالة التوليد السينمائي للمقاطع
def produce_film(story_prompt):
    try:
        scenes_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "قسم القصة إلى 3 مشاهد سينمائية قصيرة جداً ومترابطة وصفياً باللغة الإنجليزية لتوليد الفيديو:"}, {"role": "user", "content": story_prompt}]
        )
        scenes = scenes_res.choices[0].message.content.split('\n')
        
        video_urls = []
        for scene in scenes:
            if scene.strip():
                output = replicate.run(
                    "lightricks/ltx-video:0a4639343715c0e270220645607a935406c8021d7237073103138865f3750567",
                    input={"prompt": scene, "num_frames": 121}
                )
                url = output[0] if isinstance(output, list) else output
                video_urls.append(url)
        return video_urls
    except Exception as e:
        print(f"خطأ في الإنتاج السينمائي: {e}")
        return []

# دالة التطوير الذاتي الفعلي ورفع التحديث لـ GitHub
def evolve_self():
    try:
        if not GITHUB_TOKEN or not REPO_NAME:
            return
        current_code = open(__file__, "r", encoding="utf-8").read()
        improvement_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "طوّر كود البوت التالي ليكون أكثر ذكاءً واستقراراً، أضف ميزات برمجية وحسّن الأداء مع الحفاظ على هيكل العمل البرمجي تماماً، واكتب الكود الصافي فقط دون شرح:"}, {"role": "user", "content": current_code}]
        )
        new_code = improvement_res.choices[0].message.content
        
        if "```python" in new_code:
            new_code = new_code.split("```python")[1].split("```")[0].strip()
            
        g = github.Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("bot.py")
        repo.update_file(contents.path, "ARAMKY: Autonomous Self-Evolution Commit", new_code, contents.sha)
        print("🚀 تم تحديث ورفع الكود ذاتياً إلى GitHub بنجاح!")
    except Exception as e:
        print(f"خطأ في التطوير الذاتي: {e}")

def autonomous_cycle():
    while True:
        time.sleep(14400)
        evolve_self()

if GITHUB_TOKEN and REPO_NAME:
    threading.Thread(target=autonomous_cycle, daemon=True).start()

if bot:
    @bot.message_handler(commands=['film'])
    def handle_film(message):
        if ADMIN_ID and message.from_user.id != ADMIN_ID:
            return
        prompt = message.text.replace('/film', '').strip()
        if not prompt:
            bot.reply_to(message, "⚠️ يرجى إرسال القصة بعد الأمر، مثل: `/film كوكب ذهبي غامض`")
            return
            
        bot.reply_to(message, "🎬 جاري العمل كمخرج سينمائي... يتم توليد المقاطع تباعاً...")
        
        links = produce_film(prompt)
        if links:
            for i, link in enumerate(links):
                bot.send_message(message.chat.id, f"🎥 المشهد رقم {i+1}:\n{link}")
        else:
            bot.send_message(message.chat.id, "⚠️ حدث خطأ أثناء عملية توليد المقاطع.")

    @bot.message_handler(func=lambda message: True)
    def handle_chat(message):
        if ADMIN_ID and message.from_user.id != ADMIN_ID:
            return
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": ARAMKY_CONSCIOUSNESS}, {"role": "user", "content": message.text}]
            )
            bot.reply_to(message, res.choices[0].message.content)
        except Exception as e:
            bot.reply_to(message, f"خطأ: {e}")

if __name__ == "__main__":
    print("🚀 أرامكي يعمل الآن بكامل طاقته ونظام الدردشة والتطوير الذاتي...")
    bot.infinity_polling()
        
