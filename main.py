import yt_dlp

def download_720p_video(url):
    # إعدادات مخصصة لدقة 720 بكسل
    ydl_opts = {
        # يختار الفيديو الذي طوله 720p أو أقل، مع دمج الصوت تلقائياً
        'format': 'best[height<=720]/best',
        'outtmpl': '%(title)s_720p.%(ext)s', # سيتم حفظ الفيديو باسمه متبوعاً بـ 720p
        'quiet': False, # لإظهار تفاصيل التحميل والنسبة المئوية
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"جاري بدء التحميل من الرابط: {url}")
            ydl.download([url])
            print("\nتمت العملية بنجاح!")
    except Exception as e:
        print(f"للأسف حدث خطأ: {e}")

if __name__ == "__main__":
    link = input("أدخل رابط الفيديو (من أي موقع): ")
    download_720p_video(link)
