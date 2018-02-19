all:
	rm -f smash.log
	touch smash.log
	python3 app.py

kill:
	sh kill.sh

clean:
	rm .*

tail:
	tail -f -n 50 smash.log
