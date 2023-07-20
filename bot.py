import os
from io import BytesIO
from PIL import Image
from moviepy.editor import VideoFileClip
from telegram.ext import Updater, MessageHandler, Filters

# Fungsi untuk menambahkan logo pada foto
def add_logo_to_photo(photo_path, logo_path, output_path):
    photo = Image.open(photo_path)
    logo = Image.open(logo_path)

    # Menyesuaikan ukuran logo dengan foto
    logo = logo.resize((int(photo.width / 4), int(photo.height / 4)))

    # Menambahkan logo pada foto
    photo.paste(logo, (photo.width - logo.width, photo.height - logo.height), logo)

    # Menyimpan foto yang sudah ditambahkan logo
    photo.save(output_path)

# Fungsi untuk menambahkan logo pada video
def add_logo_to_video(video_path, logo_path, output_path):
    video = VideoFileClip(video_path)
    logo = Image.open(logo_path)

    # Menyesuaikan ukuran logo dengan video
    logo = logo.resize((int(video.w / 4), int(video.h / 4)))

    # Menggabungkan logo dengan video
    video = video.set_position(("right", "bottom")).set_duration(video.duration)
    video = video.set_make_frame(lambda t: add_logo_to_frame(video.get_frame(t), logo))

    # Menyimpan video yang sudah ditambahkan logo
    video.write_videofile(output_path, codec="libx264")

# Fungsi untuk menambahkan logo pada setiap frame video
def add_logo_to_frame(frame, logo):
    frame = Image.fromarray(frame)
    frame.paste(logo, (frame.width - logo.width, frame.height - logo.height), logo)
    return frame

# Fungsi yang akan dipanggil ketika ada gambar yang dikirim pengguna
def photo_handler(update, context):
    photo_file = update.message.photo[-1].get_file()
    photo_path = f"photo_{update.message.chat_id}.jpg"
    photo_file.download(photo_path)

    logo_path = "resource/watermark.png"
    output_path = f"output_photo_{update.message.chat_id}.jpg"

    add_logo_to_photo(photo_path, logo_path, output_path)

    update.message.reply_photo(photo=open(output_path, "rb"))

# Fungsi yang akan dipanggil ketika ada video yang dikirim pengguna
def video_handler(update, context):
    video_file = update.message.video.get_file()
    video_path = f"video_{update.message.chat_id}.mp4"
    video_file.download(video_path)

    logo_path = "path_ke_logo_anda.png"
    output_path = f"output_video_{update.message.chat_id}.mp4"

    add_logo_to_video(video_path, logo_path, output_path)

    update.message.reply_video(video=open(output_path, "rb"))

def main():
    # Inisialisasi bot
    updater = Updater("6033844635:AAFyS1UGT8MmGTOUDjFITn_bWkJaGPInA5g", use_context=True)
    dp = updater.dispatcher

    # Menambahkan handler untuk foto dan video
    dp.add_handler(MessageHandler(Filters.photo, photo_handler))
    dp.add_handler(MessageHandler(Filters.video, video_handler))

    # Memulai bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
