import os;
from audio_to_text import ogg_to_wav, recognize_speech
from telegram import Update, File
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает.")
    
async def download_file(file_id: str, context: ContextTypes.DEFAULT_TYPE) -> str | None:
    try:
        file: File = await context.bot.get_file(file_id)

        file_extension = os.path.splitext(file.file_path)[1]
        filename = f"{file_id}{file_extension}"

        await file.download_to_drive(filename)
        return filename

    except Exception as e:
        print(f"Ошибка при скачивании файла: {e}")
        return None
    
async def process_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    voice = message.voice

    if not voice:
        return

    # Скачиваем голосовое сообщение
    try:
        file = await context.bot.get_file(voice.file_id)
        original_filename = f"voice_{voice.file_id}.ogg"
        await file.download_to_drive(original_filename)
    except Exception as e:
        await message.reply_text(f"Не удалось скачать файл: {e}")
        return

    # Конвертация в WAV
    wav_filename = None
    try:
        wav_filename = ogg_to_wav(original_filename)
    except Exception as e:
        await message.reply_text(f"Ошибка при конвертации файла: {e}")
        if os.path.exists(original_filename):
            os.remove(original_filename)
        return

    # Распознавание речи
    text = recognize_speech(wav_filename)

    # Очистка временных файлов
    for path in [original_filename, wav_filename]:
        if path and os.path.exists(path):
            os.remove(path)

    if text:
        await message.reply_text(f"Расшифровка:\n\n{text}")
    else:
        await message.reply_text("Не удалось распознать речь.")

def main():
    application = Application.builder().token("BOT_TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, process_voice_message))

    application.run_polling()

if __name__ == "__main__":
    main()
