# Бот для фильтра данных из xlsx

## Требования:
1. Ubuntu linux
2. Белый IP адрес
3. Открытый порт 8443 на файрволе

## Установка

Install pip
```bash

sudo apt update && sudo apt upgrade && sudo apt install python3-pip
```
Install requirements
```bash
cd csv2bot
pip3 install -r requirements.txt
```

## Настройка бота

Запустите install.sh
```bash
chmod +x install.sh
./install.sh
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