# -*- coding: utf-8 -*-
import os
import asyncio
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك
TOKEN = '8701970648:AAHWP7Jbj_JawtRZwmQD9bjeAGCYbrMUhbo'

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video_file.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل بنجاح! أرسل رابط الفيديو الآن.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        return

    status = await update.message.reply_text("⏳ جاري التحميل...")
    
    try:
        # تنفيذ التحميل في مسار منفصل لمنع تجميد البوت
        file_path = await asyncio.to_thread(download_video, url)
        
        # إرسال الملف للمستخدم
        await update.message.reply_video(video=open(file_path, 'rb'))
        
        # حذف الملف من السيرفر فوراً
        os.remove(file_path)
        await status.delete()
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البرنامج بدأ... اضغط Ctrl+C للإيقاف")
    app.run_polling()
