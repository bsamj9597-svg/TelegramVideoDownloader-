import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8675744580:AAHEd5NHGqSqJELTwUiPaunwJYvBZ0igsvs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً يا بطل! ابعتلي رابط الفيديو وهنزلهولك فوراً 🚀")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id
    status_msg = await update.message.reply_text("جاري التحميل... انتظر قليلاً ⏳")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': f'video_{chat_id}.mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        video_file = f'video_{chat_id}.mp4'
        
        with open(video_file, 'rb') as video:
            await update.message.reply_video(video=video, caption="تم التحميل بواسطة بوتك الخاص ✅")
        
        if os.path.exists(video_file):
            os.remove(video_file)

    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {str(e)}")
    
    finally:
        await status_msg.delete()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    app.run_polling()
