@echo off
title Yandex Market Bot v3.0
color 0A

echo ========================================
echo    YANDEX MARKET BOT v3.0
echo
echo.
echo 1 Запуск Telegram бота
echo 2 Тест парсинга (один аккаунт)
echo 3 Массовая проверка всех аккаунтов
echo 4 Очистить базу данных
echo 5 Выход
echo.
set /p choice="Выберите действие (1-5): "

if "%choice%"=="1" goto bot
if "%choice%"=="2" goto test
if "%choice%"=="3" goto bulk
if "%choice%"=="4" goto clear
if "%choice%"=="5" goto exit

:bot
cls
echo Запуск Telegram бота...
python main.py
pause
goto menu

:test
cls
echo Запуск тестового парсинга...
python testparser.py
pause
goto menu

:bulk
cls
echo Массовая проверка аккаунтов...
python bulkcheck.py
pause
goto menu

:clear
cls
echo ВНИМАНИЕ! Это удалит ВСЕ данные!
set /p confirm="Вы уверены? (yes/no): "
if "%confirm%"=="yes" (
    del data\accounts.db
    echo База данных очищена!
)
pause
goto
menu

:exit
exit

:menu
cls
goto start