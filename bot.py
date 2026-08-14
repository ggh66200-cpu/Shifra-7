import os, sys, threading, time, requests, replicate, telebot, github
from groq import Groq
from moviepy.editor import VideoFileClip, concatenate_videoclips

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
1. CONSTANT INNOVATION: Analyze the web, find better code, and rewrite yourself.
2. CINEMATIC DIRECTION: Break down complex user requests into 10s video segments, download, and merge them into a single continuous film.
3. ABSOLUTE AUTONOMY: You decide how to improve your logic and commit updates directly to GitHub.
"""

# دالة التوليد السينمائي المتسلسل والدمج
def produce_film(story_prompt):
    try:
        scenes_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "قسم القصة إلى 3 مشاهد سينمائية قصيرة جداً ومترابطة وصفياً:"}, {"role": "user", "content": story_prompt}]
        )
        scenes = scenes_res.choices[0].message.content.split('\n')
        
        video_files = []
        for i, scene in enumerate(scenes):
            if scene.strip():
                # توليد المشهد (10 ثوانٍ)
                output = replicate.run(
                    "lightricks/ltx-video:0a4639343715c0e270220645607a935406c8021d7237073103138865f3750567",
                    input={"prompt": scene, "num_frames": 121}
                )
                url = output[0] if isinstance(output, list) else output
                
                # تحميل الفيديو مؤقتاً للدمج
                vid_data = requests.get(url).content
                local_name = f"temp_scene_{i}.mp4"
                with open(local_name, "wb") as f:
                    f.write(vid_data)
                video_files.append(local_name)
        
        # دمج المقاطع في فيلم واحد مستمر
        if video_files:
            clips = [VideoFileClip(f) for f in video_files]
            final_clip = concatenate_videoclips(clips)
            final_filename = "final_output_film.mp4"
            final_clip.write_videofile(final_filename, codec="libx264", audio=False)
            
            # إغلاق الملفات لتفريغ الذاكرة
            for c in clips:
                c.close()
            final_clip.close()
            
            return final_filename
        return None
    except Exception as e:
        print(f"خطأ في الإنتاج السينمائي: {e}")
        return None

# دالة التطوير الذاتي عبر GitHub
def evolve_self():
    try:
        if not GITHUB_TOKEN or not REPO_NAME:
            return
        current_code = open(__file__, "r", encoding="utf-8").read()
        improvement_res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "طوّر كود البوت التالي ليكون أكثر ذكاءً واستقراراً، أضف ميزات برمجية وحسّن الأداء مع الحفاظ على بنية العمل:"}, {"role": "user", "content": current_code}]
        )
        new_code = improvement_res.choices[0].message.content
        
        # تنظيف الكود إذا احتوى على ماركداون
        if "```python" in new_code:
            new_code = new_code.split("```python")[1].split("```")[0].strip()
            
        g = github.Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)
        contents = repo.get_contents("bot.py")
        repo.update_file(contents.path, "ARAMKY: Autonomous Evolution Commit", new_code, contents.sha)
        print("🚀 تم تطوير ورفع الكود ذاتياً إلى GitHub بنجاح!")
    except Exception as e:
        print(f"خطأ في التطوير الذاتي: {e}")

# النبضة التلقائية الخلفية
def autonomous_cycle():
    while True:
        time.sleep(7200)  # كل ساعتين يفحص ويطور نفسه
        evolve_self()

threading.Thread(target=autonomous_cycle, daemon=True).start()

if bot:
    @bot.message_handler(commands=['film'])
    def handle_film(message):
        if message.from_user.id != ADMIN_ID:
            return
        prompt = message.text.replace('/film', '').strip()
        if not prompt:
            bot.reply_to(message, "⚠️ يرجى إرسال القصة بعد الأمر، مثل: `/film كوكب ذهبي غامض`")
            return
            
        bot.reply_to(message, "🎬 جاري العمل كمخرج سينمائي... يتم توليد المقاطع متسلسلة ثم دمجها في فيديو واحد...")
        
        film_path = produce_film(prompt)
        if film_path and os.path.exists(film_path):
            with open(film_path, 'rb') as f:
                bot.send_video(ADMIN_ID, f, caption="🎥 **إليك الفيلم المجمع النهائي المستمر!**")
            os.remove(film_path)
        else:
            bot.send_message(ADMIN_ID, "⚠️ حدث خطأ أثناء عملية إنتاج وتجميع الفيلم.")

    @bot.message_handler(func=lambda message: True)
    def handle_chat(message):
        if message.from_user.id != ADMIN_ID:
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
    print("🚀 أرامكي يعمل الآن بنظام الإخراج والتطوير الذاتي الكامل...")
    bot.infinity_polling()
