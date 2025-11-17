"""
Модуль для распознавания казахской речи
"""
import torch
import librosa
import numpy as np
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class KazakhSpeechRecognizer:
    """Класс для распознавания казахской речи используя Whisper"""

    def __init__(self, model_path: str, device: str = "cuda"):
        """
        Инициализация распознавателя речи

        Args:
            model_path: Путь к тренированной модели
            device: Устройство для выполнения (cuda/cpu)
        """
        self.device = device if torch.cuda.is_available() else "cpu"
        self.model_path = model_path

        logger.info(f"Загрузка модели с пути: {model_path}")
        logger.info(f"Использование устройства: {self.device}")

        try:
            # Загружаем модель и процессор
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
                model_path, torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            )
            self.model = self.model.to(self.device)

            self.processor = AutoProcessor.from_pretrained(model_path)

            logger.info("Модель успешно загружена")
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели: {e}")
            raise

    def preprocess_audio(self, audio_path: str) -> np.ndarray:
        """
        Предварительная обработка аудиофайла

        Args:
            audio_path: Путь к аудиофайлу

        Returns:
            Обработанный аудиосигнал
        """
        try:
            # Загружаем аудиофайл
            audio, sr = librosa.load(audio_path, sr=16000)

            # Нормализуем амплитуду
            if np.max(np.abs(audio)) > 0:
                audio = audio / np.max(np.abs(audio))

            return audio
        except Exception as e:
            logger.error(f"Ошибка при обработке аудиофайла: {e}")
            raise

    def recognize(self, audio_path: str) -> Tuple[str, float]:
        """
        Распознавание речи из аудиофайла

        Args:
            audio_path: Путь к аудиофайлу

        Returns:
            Кортеж (распознанный текст, уверенность)
        """
        try:
            # Предварительно обрабатываем аудио
            audio = self.preprocess_audio(audio_path)

            # Подготавливаем входные данные для модели
            inputs = self.processor(
                audio, sampling_rate=16000, return_tensors="pt"
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            # Выполняем распознавание
            with torch.no_grad():
                generated_ids = self.model.generate(
                    **inputs,
                    num_beams=5,
                    max_length=225,
                    forced_decoder_ids=None,
                )

            # Декодируем результат
            transcription = self.processor.batch_decode(
                generated_ids, skip_special_tokens=True
            )[0]

            confidence = 0.95  # Примерная уверенность (можно улучшить)

            logger.info(f"Распознан текст: {transcription}")
            return transcription, confidence

        except Exception as e:
            logger.error(f"Ошибка при распознавании речи: {e}")
            raise

    def batch_recognize(self, audio_paths: list) -> list:
        """
        Распознавание нескольких аудиофайлов

        Args:
            audio_paths: Список путей к аудиофайлам

        Returns:
            Список распознанных текстов
        """
        results = []
        for audio_path in audio_paths:
            try:
                text, confidence = self.recognize(audio_path)
                results.append({"text": text, "confidence": confidence})
            except Exception as e:
                logger.error(f"Ошибка при обработке {audio_path}: {e}")
                results.append({"text": "", "confidence": 0.0, "error": str(e)})

        return results
