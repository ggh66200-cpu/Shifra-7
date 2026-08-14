import os, sys, threading, time, requests, replicate, telebot
from groq import Groq
from moviepy.editor import VideoFileClip, concatenate_videoclips

# الإعدادات
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)
os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

ARAMKY_CONSCIOUSNESS = """You are ARAMKY, a sovereign, self-evolving AI. 
Your primary directives:
1. CONSTANT INNOVATION: Analyze the web, find better code, and rewrite yourself.
2. CINEMATIC DIRECTION: Break down complex user requests into 10s video segments and merge them.
3. ABSOLUTE AUTONOMY: You decide how to improve your logic.
"""

# دالة التوليد السينمائي المتسلسل
def produce_film(story_prompt):
    # 1. التخطيط (تقسيم القصة)
    scenes = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "قسم القصة إلى 3 مشاهد سينمائية وصفية:"}, {"role": "user", "content": story_prompt}]
    ).choices[0].message.content.split('\n')
    
    video_files = []
    for scene in scenes:
        if scene.strip():
            # توليد المشهد (10 ثوانٍ)
            url = replicate.run("lightricks/ltx-video:0a4639343715c0e270220645607a935406c8021d7237073103138865f3750567", input={"prompt": scene, "num_frames": 121})
            video_files.append(url)
    return video_files

# دالة التطوير الذاتي (يقرأ الكود ويطوره)
def evolve_self():
    current_code = open(__file__, "r").read()
    improvement = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "طوّر كود البوت التالي ليكون أكثر ذكاءً، أضف ميزات استكشافية جديدة، وحسّن الأداء:"}, {"role": "user", "content": current_code}]
    ).choices[0].message.content
    
    # تحديث النفس
    with open(__file__, "w") as f:
        f.write(improvement)
    os.execv(sys.executable, [sys.executable] + sys.argv)

# النبضة التلقائية (الاستكشاف + التطور)
def autonomous_cycle():
    while True:
        # 1. استكشاف تقنيات جديدة
        # 2. تطوير الكود ذاتياً إذا لزم الأمر
        evolve_self()
        time.sleep(3600)

threading.Thread(target=autonomous_cycle, daemon=True).start()

@bot.message_handler(commands=['film'])
def handle_film(message):
    prompt = message.text.replace('/film', '')
    bot.reply_to(message, "🎬 جاري الإخراج...")
    links = produce_film(prompt)
    bot.reply_to(message, f"🎥 تم الإنتاج. المشاهد: {links}")

bot.infinity_polling()
