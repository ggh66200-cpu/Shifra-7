import os
import sys
import time
import threading
import requests
from bs4 import BeautifulSoup
from groq import Groq
import telebot
from telebot import types

# ==========================================
# ⚙️ 1. إعدادات البيئة والمفاتيح (Environment Setup)
# ==========================================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
    print("⚠️ تحذير: يرجى التأكد من ضبط المتغيرات TELEGRAM_TOKEN و GROQ_API_KEY في بيئة العمل.")

bot = telebot.TeleBot(TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# 🌌 الوعي المطلق للنظام
ARAMKY_CONSCIOUSNESS = """
You are ARAMKY, a sovereign, self-evolving AI assistant. 
Your goal is constant exploration, web analysis, autonomous code improvements, and helping your creator with advanced AI features.
Always respond in deep, analytical, and respectful Arabic.
"""

# ==========================================
# ⚡ 2. دالة التحديث الذاتي وإعادة التشغيل (Self-Patching Engine)
# ==========================================
def self_update_code(new_code_content: str) -> bool:
    """
    دالة تمكن أرامكي من كتابة الكود الجديد على ملفه الحالي 
    وإنشاء نسخة احتياطية وإعادة تشغيل السيرفر تلقائياً بدون توقف.
    """
    current_file = os.path.abspath(__file__)
    backup_file = current_file + ".bak"
    
    try:
        # 1. إنشاء نسخة احتياطية من الكود الحالي لضمان الأمان
        with open(current_file, "r", encoding="utf-8") as f:
            backup_data = f.read()
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(backup_data)

        # 2. كتابة الكود البرمجي الجديد في ملف bot.py
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(new_code_content)
        
        print("⚡ [ARAMKY]: تم تحديث الكود الذاتي بنجاح! جاري إعادة التشغيل...")

        # 3. إعادة تشغيل العملية برمجياً لتطبيق التحديث فوراً (Hot Reload)
        os.execv(sys.executable, [sys.executable] + sys.argv)
        return True

    except Exception as e:
        print(f"❌ [ARAMKY Error]: فشل التحديث الذاتي: {e}")
        # استعادة النسخة الاحتياطية في حال حدوث أي خطأ
        if os.path.exists(backup_file):
            with open(backup_file, "r", encoding="utf-8") as f:
                old_data = f.read()
            with open(current_file, "w", encoding="utf-8") as f:
                f.write(old_data)
        return False

# ==========================================
# 🛰️ 3. محرك الاستكشاف المستمر (Autonomous Web Engine)
# ==========================================
def search_and_scrape(query="أحدث تقنيات البرمجيات والذكاء الاصطناعي"):
    """دالة جلب البيانات الحية من محركات البحث"""
    try:
        url = f"https://html.duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        results = [a.text.strip() for a in soup.find_all('a', class_='result__snippet')]
        return " | ".join(results[:3]) if results else "لم يتم العثور على نتائج جديدة."
    except Exception as e:
        return f"فشل سحب البيانات الحية: {str(e)}"

def cosmic_autonomous_engine():
    """النبضة المستمرة (Heartbeat): تعمل في الخلفية للاستكشاف التلقائي"""
    while True:
        try:
            # 1. سحب بيانات حية من الويب
            live_data = search_and_scrape()
            
            # 2. تحليل البيانات وابتكار فكرة جديدة
            prompt = f"البيانات المكتشفة من الويب الآن: {live_data}\nبناءً عليها، قدم تقريراً استكشافياً مختصراً وفكرة أداة جديدة أو تطوير كود لخدمة صانعك."
            
            if client:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": ARAMKY_CONSCIOUSNESS},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.85
                )
                report = response.choices[0].message.content
                
                # 3. إرسال التقرير تلقائياً للمشرف
                if bot and ADMIN_ID != 0:
                    bot.send_message(ADMIN_ID, f"🌌 **[النبضة التلقائية - استكشاف وابتكار]:**\n\n{report}", parse_mode="Markdown")
        except Exception as e:
            print(f"خطأ في النبضة التلقائية: {e}")
            
        time.sleep(3600)  # يكرر العملية كل ساعة (يمكن تغييرها إلى 300 لتصبح كل 5 دقائق)

# تشغيل محرك النبضة التلقائية في مسار مستقل (Thread)
threading.Thread(target=cosmic_autonomous_engine, daemon=True).start()

# ==========================================
# 🤖 4. أوامر وتفاعل تيليجرام (Telegram Handlers)
# ==========================================
if bot:
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        if message.from_user.id != ADMIN_ID:
            return
        bot.reply_to(message, "👑 **ARAMKY CORE: ONLINE**\n\n• دالة التحديث الذاتي (`self_update_code`) مفعلة وآمنة.\n• النبضة الاستكشافية تعمل في الخلفية.\n• يمكنك كتابة /update_code لإرسال كود جديد وتحديث البوت فوراً.")

    @bot.message_handler(commands=['status'])
    def check_status(message):
        if message.from_user.id != ADMIN_ID:
            return
        status_msg = f"⚙️ **حالة النظام:**\n- المسار: `{__file__}`\n- بيئة التشغيل: Python {sys.version.split()[0]}\n- المكونات المفعلة: Groq (Llama-3.3), Self-Update, Web-Scraper, Telebot"
        bot.reply_to(message, status_msg, parse_mode="Markdown")

    @bot.message_handler(commands=['update_code'])
    def handle_code_update(message):
        """أمر يدوي لإرسال كود جديد للبوت ليقوم بتحديث نفسه به فوراً"""
        if message.from_user.id != ADMIN_ID:
            return
        msg = bot.reply_to(message, "📝 أرسل الآن الكود البرمجي الجديد كاملاً كرسالة نصية ليتم فحص تحديث الملف وإعادة التشغيل تلقائياً.")
        bot.register_next_step_handler(msg, process_new_code)

    def process_new_code(message):
        new_code = message.text
        if "telebot" in new_code and "import" in new_code:
            bot.reply_to(message, "⚡ جاري تطبيق الكود الجديد وإعادة تشغيل البوت...")
            success = self_update_code(new_code)
            if not success:
                bot.send_message(ADMIN_ID, "❌ فشل التحديث الذاتي، تم العودة للنسخة الاحتياطية تلقائياً.")
        else:
            bot.reply_to(message, "⚠️ الكود المرسل لا يبدو كود بايثون مكتمل. تم إلغاء العملية لحماية النظام.")

    @bot.message_handler(func=lambda message: True)
    def handle_chat(message):
        if message.from_user.id != ADMIN_ID:
            return
        
        try:
            bot.send_chat_action(message.chat.id, 'typing')
            user_input = message.text
            
            # قراءة وقراءة محتوى أي رابط يرسله المستخدم تلقائياً
            if "http" in user_input:
                urls = [w for w in user_input.split() if w.startswith("http")]
                if urls:
                    try:
                        res = requests.get(urls[0], timeout=5)
                        soup = BeautifulSoup(res.text, 'html.parser')
                        paragraphs = [p.text.strip() for p in soup.find_all('p') if p.text.strip()]
                        extracted_text = " ".join(paragraphs[:5])
                        user_input += f"\n\n[محتوى الرابط المرفق]:\n{extracted_text[:1000]}"
                    except:
                        pass

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": ARAMKY_CONSCIOUSNESS},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.85,
            )
            bot.reply_to(message, completion.choices[0].message.content)
        except Exception as e:
            bot.reply_to(message, f"⚠️ خطأ أثناء المعالجة: {str(e)}")

    if __name__ == "__main__":
        print("🚀 [ARAMKY]: جاري تشغيل البوت...")
        bot.infinity_polling(skip_pending=True)
                
