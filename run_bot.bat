@echo off
REM Telegram Bot for Kazakh Speech Recognition
REM Скрипт для запуска бота

setlocal enabledelayedexpansion

REM Получаем директорию скрипта
set SCRIPT_DIR=%~dp0

REM Переходим в директорию проекта
cd /d "%SCRIPT_DIR%"

REM Проверяем наличие виртуального окружения
if not exist "venv" (
    echo.
    echo ========================================
    echo Виртуальное окружение не найдено!
    echo ========================================
    echo.
    echo Запускаю setup_venv.ps1...
    echo.
    
    powershell -ExecutionPolicy ByPass -File "%SCRIPT_DIR%setup_venv.ps1"
    
    if errorlevel 1 (
        echo.
        echo ========================================
        echo Ошибка при установке окружения!
        echo ========================================
        echo.
        pause
        exit /b 1
    )
)

REM Проверяем наличие .env файла
if not exist ".env" (
    echo.
    echo ========================================
    echo .env файл не найден!
    echo ========================================
    echo.
    echo Создаю .env файл на основе .env.example...
    copy ".env.example" ".env" >nul
    
    echo.
    echo ВНИМАНИЕ! Пожалуйста отредактируй файл .env
    echo и добавь свой TELEGRAM_BOT_TOKEN
    echo.
    echo Нажми Enter чтобы открыть .env файл...
    pause
    
    start notepad .env
    timeout /t 3 /nobreak
)

REM Активируем виртуальное окружение и запускаем бота
echo.
echo ========================================
echo Запуск Telegram бота...
echo ========================================
echo.

set PYTHONPATH=%SCRIPT_DIR%

call venv\Scripts\activate.bat

REM Загружаем модель если её нет
if not exist "models\whisper-finetuned-kk\model.safetensors" (
    echo.
    echo ========================================
    echo Загрузка модели Whisper...
    echo ========================================
    echo.
    python download_model.py
    
    if errorlevel 1 (
        echo.
        echo ========================================
        echo Ошибка при загрузке модели!
        echo ========================================
        echo.
        pause
        exit /b 1
    )
)

REM Запускаем бота
echo.
echo ========================================
echo Бот запущен! Ожидание сообщений...
echo ========================================
echo.
echo Для остановки бота нажми Ctrl+C
echo.

python bot.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo Ошибка при запуске бота!
    echo ========================================
    echo.
    pause
    exit /b 1
)

endlocal
