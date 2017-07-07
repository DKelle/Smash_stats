all:
	rm temp.txt
	python3 get_results.py > temp.txt
	vim temp.txt
