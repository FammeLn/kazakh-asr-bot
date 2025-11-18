"""
Telegram бот для распознавания казахской речи
"""
import logging
import os
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
import sys
import sys
sys.path.insert(0, os.path.dirname(__file__))

from speech_recognizer import KazakhSpeechRecognizer
from config import TELEGRAM_BOT_TOKEN, MODEL_PATH, AUDIO_TEMP_DIR

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальная переменная для распознавателя
recognizer = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_text = """
Привет! 👋 Я бот для распознавания казахской речи.

Как использовать:
1. Отправь мне голосовое сообщение 🎤
2. Я буду распознавать текст из казахской речи
3. Получишь результат в виде текста

Доступные команды:
/start - начальная информация
/help - помощь
/about - информация о боте
"""
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
🎤 **Как отправить голосовое сообщение:**
- Нажми на микрофон в Telegram
- Запиши своё сообщение на казахском языке
- Отправь его мне

⏱️ **Ограничения:**
- Максимальная длительность: 5 минут
- Поддерживаемый язык: казахский

❓ **Возможные ошибки:**
- Если голосовое сообщение слишком короткое, попробуй ещё раз
- Убедись, что микрофон включён
"""
    await update.message.reply_text(help_text)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /about"""
    about_text = """
ℹ️ **О боте:**
Этот бот использует AI модель для распознавания казахской речи.

🔧 **Технология:**
- Модель: Whisper (fine-tuned для казахского языка)
- Framework: PyTorch + Transformers
- Language: Python

📊 **Возможности:**
- Распознавание казахской речи
- Конвертация голоса в текст
- Быстрая обработка

👨‍💻 **Разработано для:** Лабораторной работы по компьютерному зрению и распознаванию речи
"""
    await update.message.reply_text(about_text)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик голосовых сообщений"""
    global recognizer

    try:
        # Показываем, что бот обрабатывает сообщение
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )

        # Получаем голосовое сообщение
        voice = update.message.voice
        file = await context.bot.get_file(voice.file_id)

        # Создаём путь для сохранения аудиофайла
        audio_path = os.path.join(AUDIO_TEMP_DIR, f"voice_{update.message.message_id}.ogg")

        # Скачиваем файл
        await file.download_to_drive(audio_path)
        logger.info(f"Аудиофайл сохранён: {audio_path}")

        # Показываем, что обрабатываем аудио
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )

        # Распознаём речь
        logger.info("Начинаю распознавание речи...")
        text, confidence = recognizer.recognize(audio_path)

        # Отправляем результат
        response = f"""
✅ **Распознанный текст:**
{text}

📊 **Уверенность:** {confidence:.2%}
"""
        await update.message.reply_text(response)
        logger.info(f"Результат отправлен пользователю: {text}")

        # Удаляем временный файл
        os.remove(audio_path)

    except Exception as e:
        logger.error(f"Ошибка при обработке голосового сообщения: {e}")
        error_message = f"❌ Ошибка при распознавании: {str(e)}"
        await update.message.reply_text(error_message)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    message_text = update.message.text.lower().strip()
    
    # Список приветствий на разных языках
    greetings = [
        'привет', 'здравствуйте', 'здравствуй', 'hi', 'hello', 
        'сәлем', 'сәлеметсіз бе', 'салам', 'privet'
    ]
    
    # Проверяем, является ли сообщение приветствием
    if any(greeting in message_text for greeting in greetings):
        await update.message.reply_text(
            "Привет! 👋 Рад тебя видеть!\n\n"
            "Я бот для распознавания казахской речи. 🎤\n"
            "Отправь мне голосовое сообщение на казахском языке, и я преобразую его в текст.\n\n"
            "Используй /help для получения дополнительной информации."
        )
    else:
        await update.message.reply_text(
            "Я могу распознавать только голосовые сообщения. 🎤\n"
            "Отправь мне голосовое сообщение на казахском языке.\n\n"
            "Используй /help для помощи или /start для начала работы."
        )


def main() -> None:
    """Основная функция запуска бота"""
    global recognizer

    # Инициализируем распознаватель речи
    logger.info("Инициализация распознавателя речи...")
    try:
        recognizer = KazakhSpeechRecognizer(MODEL_PATH)
    except Exception as e:
        logger.error(f"Не удалось инициализировать распознаватель: {e}")
        return

    # Создаём приложение
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))

    # Регистрируем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Запускаем бот
    logger.info("Бот запущен. Ожидание сообщений...")
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    import asyncio
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
