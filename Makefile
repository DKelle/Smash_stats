all:
	rm temp.txt
	python3 manual_get_results.py > temp.txt
	vim temp.txt

bracket:
	rm bracket.txt
	python3 get_brackets.py > bracket.txt
	vim bracket.txt

html:
	rm html.txt
	python3 gen_html.py > html.txt
	cp html.txt smashco.html
	cp smashco.html ../../dkelle.github.io/
	vim smashco.html
	echo "don't forget to commit dkelle.github.io"

rank:
	rm rank.txt
	python3 get_rank.py > rank.txt
	vim rank.txt

smashbrews:
	rm html.txt
	python3 gen_html.py > html.txt
	cp html.txt smashbrews.html
	vim smashco.html
