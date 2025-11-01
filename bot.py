import telebot
from functions import get_random_fact, translate_text, wait_hours
from config import API_KEY, BOT_TOKEN, CHANNEL_USERNAME, POST_INTERVAL_HOURS

bot = telebot.TeleBot(BOT_TOKEN)

print("✅ البوت يعمل الآن وينتظر أول عملية نشر...")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 مرحبًا! هذا بوت نشر معلومات سريعة ومترجمة. سيتم إرسال المعلومة لك أولًا للموافقة قبل النشر.")

def main_loop():
    """الحلقة الرئيسية للنشر التلقائي"""
    while True:
        fact = get_random_fact(API_KEY)
        if fact:
            translated = translate_text(fact)
            
            preview_text = f"🔹 المعلومة الأصلية:\n{fact}\n\n🇸🇦 الترجمة:\n{translated}\n\nهل تريد نشرها؟ (اكتب نعم أو لا)"
            print(preview_text)
            
            # إرسال لك في الخاص للموافقة
            # ملاحظة: لازم تكتب ID المستخدم اللي يتحكم بالموافقة
            USER_ID = 5578860398
            bot.send_message(USER_ID, preview_text)
            
            # استنى الرد منك
            @bot.message_handler(func=lambda m: m.chat.id == USER_ID and m.text.lower() in ['نعم', 'لا'])
            def handle_response(msg):
                if msg.text.lower() == 'نعم':
                    bot.send_message(CHANNEL_USERNAME, f"🌍 معلومة سريعة:\n\n{translated}")
                    bot.send_message(USER_ID, "✅ تم نشر المعلومة بنجاح!")
                else:
                    bot.send_message(USER_ID, "🚫 تم تجاهل المعلومة.")
            
            wait_hours(POST_INTERVAL_HOURS)
        else:
            print("❌ فشل في جلب المعلومة. سيُعاد المحاولة بعد قليل.")
            wait_hours(1)

if __name__ == "__main__":
    import threading
    threading.Thread(target=bot.polling, daemon=True).start()
    main_loop()
