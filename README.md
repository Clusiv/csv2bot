# Бот для фильтра данных из xlsx

## Требования:
1. Ubuntu Server 20.04
2. Белый IP адрес
3. Открытый порт 8443 на файрволе

## Установка
```bash
sudo apt update && sudo apt upgrade -y && sudo apt install python3-pip -y
```
## Скачиваем репозиторий
```bash
git clone https://github.com/Clusiv/csv2bot
```
Установка зависимостей
```bash
cd csv2bot && pip3 install -r requirements.txt
```
## Настройка бота

Запустите install.sh
```bash
chmod +x install.sh && ./install.sh

#Token: 
#IP Address: 
#Telegram User ID:
```
## Запуск

Запуск бота
```bash
./start.sh
```
Остановка бота
```bash
./stop.sh
```