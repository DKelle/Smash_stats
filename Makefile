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

clear:
	python3 sql_utils.py clear
	sh rm_web_pickles.sh
	rm -f smash.log
	touch smash.log
	python3 app.py

watch:
	watch python3 sql_utils.py watch valids

anal:
	watch python3 sql_utils.py watch analyzed

test:
	python3 sql_utils.py clear smash_test
	python3 tests.py

grep:
	tail -f -n 50 smash.log | grep dallas
