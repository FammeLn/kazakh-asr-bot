# Скрипт для установки виртуального окружения на Windows

Write-Host "========================================" -ForegroundColor Green
Write-Host "Установка виртуального окружения venv" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Проверяем версию Python
python --version

# Создаём виртуальное окружение
Write-Host "`nСоздание виртуального окружения..." -ForegroundColor Yellow
python -m venv venv

# Активируем виртуальное окружение
Write-Host "Активация виртуального окружения..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Обновляем pip
Write-Host "Обновление pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Устанавливаем зависимости
Write-Host "Установка зависимостей из requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

# Создаём .env файл если его нет
if (-Not (Test-Path .env)) {
    Write-Host "Создание .env файла..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host ".env файл создан. Пожалуйста отредактируй его и добавь твой TELEGRAM_BOT_TOKEN" -ForegroundColor Cyan
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Установка завершена!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nДля запуска бота используй:" -ForegroundColor Cyan
Write-Host "python bot.py" -ForegroundColor Yellow
