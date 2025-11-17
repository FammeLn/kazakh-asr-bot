"""
Конфигурация для Telegram бота с распознаванием казахской речи
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Основные параметры
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MODEL_PATH = os.getenv("MODEL_PATH", "../whisper-finetuned-kk")

# Параметры обработки аудио
SAMPLE_RATE = 16000
MAX_AUDIO_DURATION = 300  # секунды
AUDIO_TEMP_DIR = "temp_audio"

# Параметры модели
DEVICE = "cuda"  # используем GPU если доступен
MODEL_TYPE = "whisper"  # тип модели

# Создаём директорию для временных файлов
Path(AUDIO_TEMP_DIR).mkdir(exist_ok=True)

# Проверка конфигурации
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env файле")
