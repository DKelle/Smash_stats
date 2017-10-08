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
	cp html.txt lib/smashco.html
	cp lib/smashco.html ../../../dkelle.github.io/smash/
	vim lib/smashco.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

colorado:
	rm colorado.txt
	python3 gen_html.py 'http://smashco.challonge.com/CSUWW###WUS' 'http://smashco.challonge.com/CSUWW###WUD' 'http://smascho.challonge.com/FCWUA###' 'http://smascho.challonge.com/FCWUIB###' 'http://smashco.challonge.com/FCWUDC###'> colorado.txt
	cp colorado.txt lib/colorado.html
	cp lib/colorado.html ../../../dkelle.github.io/smash/
	vim lib/colorado.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

smashbrews:
	rm smashbrews.txt
	python3 gen_html.py 'https://challonge.com/Smashbrews###' > smashbrews.txt
	cp smashbrews.txt lib/smashbrews.html
	cp lib/smashbrews.html ../../../dkelle.github.io/smash/
	vim lib/smashbrews.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

austin:
	rm austin.txt
	python3 gen_html.py 'https://challonge.com/NP9ATX###' 'https://austinsmash4.challonge.com/atx###' > austin.txt
	cp austin.txt lib/austin.html
	cp lib/austin.html ../../../dkelle.github.io/smash/
	vim lib/austin.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

austinmelee:
	rm austinmelee.txt
	python3 gen_html.py 'http://challonge.com/tipperoni###am' 'http://challonge.com/tipperoni###' 'http://challonge.com/longhornweekly###' 'http://challonge.com/apollosingles###' 'http://challonge.com/smashedhalffull###' 'http://gamerzgalaxy.challonge.com/TTT###' 'http://challonge.com/Magesmf###' 'http://challonge.com/varsity###am' 'http://challonge.com/varsity###' > austinmelee.txt
	cp austinmelee.txt lib/austinmeleesmash.html
	cp lib/austinmelee.html ../../../dkelle.github.io/smash/
	vim lib/austinmeleesmash.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

urltest:
	python3 url_test.py

clean:
	rm *.txt
