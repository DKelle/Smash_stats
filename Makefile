all: 
	uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app --enable-threads --logto logs/uwsgi.log

kill:
	sh kill.sh

clean:
	rm .*

tail:
	tail -f -n 50 logs/smash.log

wsgi:
	tail -f -n 50 logs/uwsgi.log

clear:
	python3 sql_utils.py clear
	sh rm_web_pickles.sh
	uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app --enable-threads --logto logs/uwsgi.log

clearanks:
	python3 sql_utils.py clear ranks
	sh rm_web_pickles.sh
	uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app --enable-threads --logto logs/uwsgi.log

watch:
	watch python3 sql_utils.py watch valids

anal:
	watch python3 sql_utils.py watch analyzed

test:
	python3 sql_utils.py clear smash_test
	python3 tests.py

grep:
	tail -f -n 50 logs/smash.log | grep dallas

test:
	tox
