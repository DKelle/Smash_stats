all: 
	uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app --enable-threads

kill:
	sh kill.sh

clean:
	rm .*

tail:
	tail -f -n 50 logs/smash.log

wsgi:
	tail -f -n 50 logs/uwsgi.log

clear:
	rm logs/*
	python3 sql_utils.py clear
	sh rm_web_pickles.sh
	uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app --enable-threads

clearanks:
	rm logs/*
	python3 sql_utils.py clear ranks
	sh rm_web_pickles.sh
	uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app --enable-threads

watch:
	watch python3 sql_utils.py watch valids

anal:
	watch python3 sql_utils.py watch analyzed

grep:
	tail -f -n 50 logs/smash.log | grep dallas

test:
	tox -e py3
	python3 sql_utils.py clear smash_test
	python3 tests.py
