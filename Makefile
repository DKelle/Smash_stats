all: clear
	rm -f smash.log
	touch smash.log
	python3 app.py

kill:
	sh kill.sh

clean:
	rm .*

tail:
	tail -f -n 50 smash.log

clear:
	python3 sql_utils.py clear

watch:
	watch python3 sql_utils.py watch valids

test: clear
	python3 tests.py
