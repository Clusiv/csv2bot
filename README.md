# Бот для фильтра данных из xlsx

## Требования:
1. Ubuntu 20.04 (GCP) или Ubuntu 16.04 (РЕГ.РУ)
2. Белый IP адрес
3. Открытый порт 8443 на файрволе

## Установка
```bash
sudo apt update && sudo apt upgrade -y && sudo apt install python3-pip git -y
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

## Ubuntu 16.04 (РЕГ.РУ)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y && sudo apt update -y
sudo apt install python3.8 python3.8-venv python3.8-distutils git nano htop -y
sudo apt install python3-pip -y
sudo apt remove python3-pip -y
sudo python3.8 -m easy_install pip

git clone https://github.com/Clusiv/csv2bot

cd csv2bot && pip3 install -r requirements.txt
./install.sh
```