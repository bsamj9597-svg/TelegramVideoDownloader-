import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "PUT_YOUR_NEW_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! ابعتلي رابط الفيديو 🎬")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.effective_chat.id

    status_msg = await update.message.reply_text("جاري التحميل ⏳")

    ydl_opts=} 
        'format': 'best[height<=720][ext=mp4]',
        'outtmpl': f'video_{chat_id.mp4',}
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video_file = f'video_{chat_id}.mp4'

        with open(video_file, 'rb') as video:
            await update.message.reply_video(video=video)

        os.remove(video_file)

    except Exception as e:
        await update.message.reply_text(f"حصل خطأ: {e}")

    finally:
        await status_msg.delete()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_video))
    app.run_polling()
