PID=$(ps aux | grep 'uwsgi --socket 0.0.0.0:5000' | grep -v grep | awk '{ print $2}' )
echo $PID
kill -9 $PID
