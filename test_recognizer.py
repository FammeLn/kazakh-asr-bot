"""
Тестовый скрипт для проверки работы распознавателя речи
"""
import os
import sys
import logging
from pathlib import Path

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

from speech_recognizer import KazakhSpeechRecognizer
from config import MODEL_PATH

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def test_model_loading():
    """Тест загрузки модели"""
    logger.info("=" * 50)
    logger.info("Тест 1: Загрузка модели")
    logger.info("=" * 50)

    try:
        recognizer = KazakhSpeechRecognizer(MODEL_PATH)
        logger.info("✅ Модель успешно загружена")
        return recognizer
    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке модели: {e}")
        return None


def test_audio_preprocessing(recognizer, audio_path):
    """Тест предварительной обработки аудио"""
    logger.info("=" * 50)
    logger.info("Тест 2: Предварительная обработка аудио")
    logger.info("=" * 50)

    try:
        audio = recognizer.preprocess_audio(audio_path)
        logger.info(f"✅ Аудио успешно обработано")
        logger.info(f"   - Длина: {len(audio)} сэмплов")
        logger.info(f"   - Min: {audio.min():.4f}, Max: {audio.max():.4f}")
        return audio
    except Exception as e:
        logger.error(f"❌ Ошибка при обработке аудио: {e}")
        return None


def test_recognition(recognizer, audio_path):
    """Тест распознавания речи"""
    logger.info("=" * 50)
    logger.info("Тест 3: Распознавание речи")
    logger.info("=" * 50)

    try:
        text, confidence = recognizer.recognize(audio_path)
        logger.info(f"✅ Речь успешно распознана")
        logger.info(f"   - Текст: {text}")
        logger.info(f"   - Уверенность: {confidence:.2%}")
        return text, confidence
    except Exception as e:
        logger.error(f"❌ Ошибка при распознавании: {e}")
        return None, 0.0


def main():
    """Главная функция для тестирования"""
    logger.info("Начало тестирования распознавателя казахской речи")
    logger.info(f"Путь к модели: {MODEL_PATH}")

    # Проверяем существование модели
    if not os.path.exists(MODEL_PATH):
        logger.error(f"❌ Модель не найдена по пути: {MODEL_PATH}")
        logger.info("Пожалуйста, убедись что модель находится в указанной папке")
        return

    # Тест 1: Загрузка модели
    recognizer = test_model_loading()
    if recognizer is None:
        return

    # Тест 2: Поиск тестовых аудиофайлов
    logger.info("=" * 50)
    logger.info("Поиск тестовых аудиофайлов")
    logger.info("=" * 50)

    test_audio_files = []
    for ext in ['*.wav', '*.ogg', '*.mp3']:
        test_audio_files.extend(Path('.').glob(f'test_audio/{ext}'))

    if not test_audio_files:
        logger.warning("⚠️  Тестовые аудиофайлы не найдены в папке test_audio/")
        logger.info("Для полного тестирования добавь казахские аудиофайлы в папку test_audio/")
        logger.info("Основные тесты пройдены успешно!")
        return

    # Тест 3: Обработка тестовых файлов
    for audio_file in test_audio_files[:3]:  # Тестируем первые 3 файла
        logger.info(f"\nОбработка файла: {audio_file.name}")
        test_recognition(recognizer, str(audio_file))

    logger.info("\n" + "=" * 50)
    logger.info("Тестирование завершено!")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
