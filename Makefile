all:
	rm temp.txt
	python3 manual_get_results.py > temp.txt
	vim temp.txt

bracket:
	rm bracket.txt
	python3 get_brackets.py > bracket.txt
	vim bracket.txt

challonge:
	rm temp.txt
	python3 get_results.py > temp.txt
	vim temp.txt
