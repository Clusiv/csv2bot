# Бот для фильтра данных из xlsx

## Требования:
1. Ubuntu Server 20.04
2. Белый IP адрес
3. Открытый порт 8443 на файрволе

## Установка

Install pip
```bash

sudo apt update && sudo apt upgrade -y && sudo apt install python3-pip -y
```
Install requirements
```bash
cd csv2bot
pip3 install -r requirements.txt
```
## Скачиваем репозиторий
```bash
git clone https://github.com/Clusiv/csv2bot
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