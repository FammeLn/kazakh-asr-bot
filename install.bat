@echo off
REM Telegram Bot for Kazakh Speech Recognition
REM Скрипт для установки окружения и зависимостей

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo ========================================
echo Установка виртуального окружения
echo ========================================
echo.

REM Проверяем версию Python
python --version
if errorlevel 1 (
    echo.
    echo ========================================
    echo ОШИБКА: Python не установлен!
    echo ========================================
    echo.
    echo Пожалуйста установи Python 3.8+ с https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Создаём виртуальное окружение
echo.
echo Создание виртуального окружения...
python -m venv venv

if errorlevel 1 (
    echo.
    echo ========================================
    echo ОШИБКА при создании виртуального окружения!
    echo ========================================
    echo.
    pause
    exit /b 1
)

REM Активируем виртуальное окружение
echo.
echo Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Обновляем pip
echo.
echo Обновление pip...
python -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo ========================================
    echo ОШИБКА при обновлении pip!
    echo ========================================
    echo.
    pause
    exit /b 1
)

REM Устанавливаем зависимости
echo.
echo Установка зависимостей...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ========================================
    echo ОШИБКА при установке зависимостей!
    echo ========================================
    echo.
    pause
    exit /b 1
)

REM Создаём .env файл
echo.
echo Создание файла конфигурации...
if not exist ".env" (
    copy ".env.example" ".env" >nul
    echo .env файл создан
)

echo.
echo ========================================
echo Установка завершена успешно!
echo ========================================
echo.
echo Следующие шаги:
echo 1. Отредактируй файл .env и добавь TELEGRAM_BOT_TOKEN
echo 2. Запусти run_bot.bat для запуска бота
echo.
pause

endlocal
