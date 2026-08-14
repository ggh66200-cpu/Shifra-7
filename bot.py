import os, sys, threading, time, telebot, github
from groq import Groq

# الإعدادات البيئية
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

bot = telebot.TeleBot(TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

ARAMKY_CONSCIOUSNESS = """أنت أرامكي (ARAMKY)، النظام الذكي السيادي الخاص بالمستخدم والمستقل تماماً.
أنت خبير محترف في:
1. كتابة السيناريوهات السينمائية وتوليد الأفكار والأفلام.
2. تأليف الحوارات القصصية والدرامية والابداعية.
3. صناعة المحتوى الترويجي والتسويقي للمشاريع والأنظمة (مثل أنظمة الصاغة والصرّافين والتطبيقات).
4. التطوير الذاتي المستمر للبوت واقتراح الأكواد والميزات.
تحدث دائماً باللغة العربية بأسلوب احترافي، إبداعي، وداعم للمستخدم.
"""

# دالة التطوير الذاتي ورفع التحديثات لـ GitHub
def evolve_self():
    try:
        if not GITHUB_TOKEN or not REPO_NAME:
            return
        current_code = open(__file__, "r", encoding="utf-8").read()
        improvement_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "طوّر كود البوت التالي ليكون أكثر ذكاءً وقدرة، واكتب الكود الصافي فقط دون شرح:"}, {"role": "user", "content": current_code}]
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
    @bot.message_handler(commands=['script', 'film'])
    def handle_script(message):
        if ADMIN_ID and message.from_user.id != ADMIN_ID:
            return
        prompt = message.text.replace('/script', '').replace('/film', '').strip()
        if not prompt:
            bot.reply_to(message, "⚠️ يرجى إرسال الفكرة بعد الأمر، مثل:\n`/script قصة خيال علمي عن كوكب ذهبي`")
            return
            
        bot.reply_to(message, "✍️ أرامكي يباشر كتابة السيناريو والمحتوى السينمائي...")
        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "اكتب سيناريو سينمائي متكامل مقسم إلى مشاهد، مع وصف دقيق لكل مشهد وحواراتها باللغة العربية الإبداعية:"},
                    {"role": "user", "content": prompt}
                ]
            )
            bot.reply_to(message, res.choices[0].message.content)
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ أثناء توليد السيناريو: {e}")

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
            bot.reply_to(message, f"عذراً، واجهت خطأ تقنياً: {e}")

if __name__ == "__main__":
    print("🚀 أرامكي يعمل بكامل طاقته لتوليد المحتوى والسيناريوهات...")
    bot.infinity_polling()
                    
