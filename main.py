import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# ضع التوكن الخاص بك هنا
TOKEN = '8701970648:AAHWP7Jbj_JawtRZwmQD9bjeAGCYbrMUhbo'

# دالة التحميل باستخدام yt-dlp
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',  # اسم الملف المؤقت
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'video.mp4'

# رسالة الترحيب /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي رابط فيديو من (يوتيوب، فيسبوك، تيك توك) وسأقوم بتحميله لك.")

# معالجة الروابط وتحميلها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        await update.message.reply_text("من فضلك أرسل رابطاً صحيحاً.")
        return

    msg = await update.message.reply_text("جاري المعالجة والتحميل... انتظر قليلاً ⏳")

    try:
        # تنفيذ التحميل في "thread" منفصل عشان ميعطلش البوت
        file_path = await asyncio.to_thread(download_video, url)
        
        # إرسال الفيديو للمستخدم
        await update.message.reply_video(video=open(file_path, 'rb'), caption="تم التحميل بنجاح ✅")
        
        # حذف الملف بعد الإرسال لتوفير المساحة
        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await update.message.reply_text(f"حدث خطأ أثناء التحميل: {str(e)}")

# تشغيل البوت
if __name__ == '__main__':
    print("البوت يعمل الآن...")
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()
