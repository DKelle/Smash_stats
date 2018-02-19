PID=$(ps aux | grep 'python3 app' | grep -v grep | awk '{ print $2}' )
echo $PID
kill -9 $PID
