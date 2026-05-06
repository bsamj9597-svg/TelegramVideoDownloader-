
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pytube import YouTube

# التوكن الخاص بك تم وضعه هنا
TOKEN = "8793504257:AAGZ4rBZzvomOKD9uR09VawooozsuSjm3q4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا بوت تحميل فيديوهات يوتيوب الجديد. أرسل لي الرابط وسأبدأ فوراً.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        status_msg = await update.message.reply_text("⏳ جاري سحب الفيديو... انتظر لحظة.")
        try:
            # استخدام pytube لجلب الفيديو
            yt = YouTube(url)
            # اختيار جودة متوسطة (360p أو 720p) لضمان سرعة الرفع وعدم فشل السيرفر
            stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
            
            # التحميل
            file_path = stream.download()
            
            # إرسال الفيديو
            await update.message.reply_video(video=open(file_path, 'rb'), caption=f"✅ تم التحميل:\n{yt.title}")
            
            # تنظيف المكان (حذف الملف من السيرفر)
            os.remove(file_path)
            await status_msg.delete()
            
        except Exception as e:
            await update.message.reply_text(f"❌ حدثت مشكلة: {str(e)}")
    else:
        await update.message.reply_text("⚠️ من فضلك أرسل رابط يوتيوب صحيح.")

def main():
    # بناء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # إضافة الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    # تشغيل البوت
    print("البوت شغال حالياً...")
    application.run_polling()

if __name__ == '__main__':
    main()
