PIDFILE=app.pid
if test -f "$PIDFILE"; then
    echo "Bot is already running. Run ./stop.sh to stop current bot."
else
    nohup python3 app.py &
    echo "Running in background"
fi