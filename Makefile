all:
	rm temp.txt
	python3 manual_get_results.py > temp.txt
	vim temp.txt

challonge:
	rm temp.txt
	python3 get_results.py > temp.txt
	vim temp.txt
