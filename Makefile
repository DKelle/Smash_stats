all: clear
	rm -f smash.log
	touch smash.log
	python3 app.py

noclear:
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

compare:
	python3 compare_dbs.py

test: compare
	python3 sql_utils.py clear smash_test
	python3 tests.py
