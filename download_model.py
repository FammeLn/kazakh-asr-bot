"""
Скрипт для загрузки модели Whisper для казахского языка с Hugging Face
"""
import os
from pathlib import Path
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import logging

logger = logging.getLogger(__name__)


def download_model(model_name: str = "openai/whisper-medium", output_dir: str = "./models"):
    """
    Загружает модель и процессор с Hugging Face

    Args:
        model_name: Название модели на Hugging Face
        output_dir: Директория для сохранения модели
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    model_path = output_dir / "whisper-finetuned-kk"

    # Если модель уже загружена, пропустить
    if (model_path / "model.safetensors").exists():
        logger.info(f"Модель уже существует в {model_path}")
        return str(model_path)

    logger.info(f"Загрузка модели {model_name}...")

    try:
        # Загружаем модель и сохраняем её локально
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_name,
            cache_dir=str(model_path)
        )
        processor = AutoProcessor.from_pretrained(
            model_name,
            cache_dir=str(model_path)
        )

        logger.info(f"✅ Модель успешно загружена и сохранена в {model_path}")
        return str(model_path)

    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке модели: {e}")
        raise


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    model_path = download_model()
    print(f"Модель готова к использованию: {model_path}")
