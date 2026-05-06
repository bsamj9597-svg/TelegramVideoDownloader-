import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# توكن البوت الخاص بك
TOKEN = '8793504257:AAGZ4rBZzvomOKD9uR09VawooozsuSjm3q4'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أرسل لي رابط فيديو من يوتيوب أو إنستغرام وسأقوم بتحميله لك.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status_message = await update.message.reply_text("جاري معالجة الرابط وتحميل الفيديو... انتظر قليلاً ⏳")

    # إعدادات yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # اختيار أفضل جودة mp4
        'outtmpl': 'downloads/%(title)s.%(ext)s', # مسار الحفظ
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            # إرسال الفيديو للمستخدم
            await update.message.reply_video(video=open(file_path, 'rb'), caption=info.get('title', 'تم التحميل بواسطة البوت'))
            
            # حذف الملف بعد الإرسال لتوفير المساحة
            os.remove(file_path)
            await status_message.delete()

    except Exception as e:
        await status_message.edit_text(f"عذراً، حدث خطأ أثناء التحميل: {str(e)}")

if __name__ == '__main__':
    # إنشاء مجلد للتحميلات إذا لم يكن موجوداً
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))

    print("البوت يعمل الآن...")
    app.run_polling()
