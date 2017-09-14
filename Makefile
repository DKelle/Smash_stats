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
	python3 gen_html.py 'https://challonge.com/NP9ATX###' 'https://austinsmash4.challonge.com/atx###' > html.txt
	cp html.txt smashco.html
	cp smashco.html ../../../dkelle.github.io/smash/
	vim smashco.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

rank:
	rm rank.txt
	python3 get_rank.py > rank.txt
	vim rank.txt

colorado:
	rm colorado.txt
	python3 gen_html.py 'http://smashco.challonge.com/CSUWW###WUS' 'http://smashco.challonge.com/CSUWW###WUD' 'http://smascho.challonge.com/FCWUA###' 'http://smascho.challonge.com/FCWUIB###' 'http://smashco.challonge.com/FCWUDC###'> colorado.txt
	cp colorado.txt coloradosmash.html
	vim coloradosmash.html

smashbrews:
	rm smashbrews.txt
	python3 gen_html.py 'https://challonge.com/Smashbrews###' > smashbrews.txt
	cp smashbrews.txt smashbrews.html
	vim smashbrews.html

austin:
	rm austin.txt
	python3 gen_html.py 'https://challonge.com/NP9ATX###' 'https://austinsmash4.challonge.com/atx###' > austin.txt
	cp austin.txt austinsmash.html
	vim austinsmash.html

urltest:
	python3 url_test.py
