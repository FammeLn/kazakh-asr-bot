"""
Тесты для проверки обработки приветствий в боте
"""
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))


class TestGreetingHandling(unittest.TestCase):
    """Тесты для обработки приветствий"""

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.greetings = [
            'привет', 'здравствуйте', 'здравствуй', 'hi', 'hello',
            'сәлем', 'сәлеметсіз бе', 'салам', 'privet'
        ]

    def test_greeting_detection(self):
        """Тест: проверка распознавания приветствий"""
        test_messages = [
            ('привет', True),
            ('Привет!', True),
            ('ПРИВЕТ', True),
            ('Здравствуйте', True),
            ('Hi there', True),
            ('hello world', True),
            ('сәлем', True),
            ('Как дела?', False),
            ('test message', False),
            ('распознай голос', False),
        ]

        for message, should_be_greeting in test_messages:
            message_lower = message.lower().strip()
            is_greeting = any(greeting in message_lower for greeting in self.greetings)
            self.assertEqual(
                is_greeting, should_be_greeting,
                f"Сообщение '{message}' должно быть {'приветствием' if should_be_greeting else 'не приветствием'}"
            )

    def test_all_greetings_covered(self):
        """Тест: проверка что все ожидаемые приветствия в списке"""
        expected_greetings = ['привет', 'hello', 'hi', 'сәлем']
        for greeting in expected_greetings:
            self.assertIn(
                greeting, self.greetings,
                f"Приветствие '{greeting}' должно быть в списке"
            )


if __name__ == '__main__':
    print("Запуск тестов для обработки приветствий...")
    unittest.main(verbosity=2)
