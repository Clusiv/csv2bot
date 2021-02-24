read -p "Token: " TOKEN
read -p "IP Address: " IP
read -p "Telegram User ID: " ID

openssl genrsa -out webhook_pkey.pem 2048

openssl req -new -x509 -days 3650 \
-key webhook_pkey.pem -out webhook_cert.pem \
-subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN="$IP

mv webhook* app/
chmod +x start.sh stop.sh

echo "# Токен 
TOKEN = '$TOKEN'

# Пользователи которым разрешено обновлять базу
# Числа разделенные запятой
ADMIN_CHAT_ID = $ID,

# IP Адрес вашего сервера
IP = '$IP'" > app/config.py

if test -f app/webhook_cert.pem; then
    echo "###########"
    echo "# Success #"
    echo "###########"
    echo "Run bot with ./start.sh"
    echo "Stop bot with .stop.sh"
else
    echo "Error"
fi