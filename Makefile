all:
	[ -e temp.txt ] && rm -f temp.txt
	python3 manual_get_results.py > temp.txt
	vim temp.txt

html:
	[ -e html.txt ] && rm -f html.txt
	python3 gen_html.py 'https://challonge.com/NP9ATX###' 'https://austinsmash4.challonge.com/atx###' 'http://challonge.com/heatwave###'> html.txt
	cp html.txt lib/smashco.html
	cp lib/smashco.html ../../dkelle.github.io/smash/
	vim lib/smashco.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

colorado:
	[ -e colorado.txt ] && rm -f colorado.txt
	python3 gen_html.py 'http://smashco.challonge.com/CSUWW###WUS' 'http://smashco.challonge.com/CSUWW###WUD' 'http://smascho.challonge.com/FCWUA###' 'http://smascho.challonge.com/FCWUIB###' 'http://smashco.challonge.com/FCWUDC###'> colorado.txt
	cp colorado.txt lib/colorado.html
	cp lib/colorado.html ../../dkelle.github.io/smash/
	vim lib/colorado.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

smashbrews:
	[ -e smashbrews.txt ] && rm -f smashbrews.txt
	python3 gen_html.py 'https://challonge.com/Smashbrews###' > smashbrews.txt
	cp smashbrews.txt lib/smashbrews.html
	cp lib/smashbrews.html ../../dkelle.github.io/smash/
	vim lib/smashbrews.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

austin:
	[ -e austin.txt ] && rm -f austin.txt
	python3 gen_html.py 'https://challonge.com/NP9ATX###' 'https://austinsmash4.challonge.com/atx###' 'http://challonge.com/HW###'> austin.txt
	cp austin.txt lib/austin.html
	cp lib/austin.html ../../dkelle.github.io/smash/
	vim lib/austin.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

austinmelee:
	[ -e austinmelee.txt ] && rm -f austinmelee.txt
	python3 gen_html.py 'http://challonge.com/tipperoni###am' 'http://challonge.com/tipperoni###' 'http://challonge.com/longhornweekly###' 'http://challonge.com/apollosingles###' 'http://challonge.com/smashedhalffull###' 'http://gamerzgalaxy.challonge.com/TTT###' 'http://challonge.com/Magesmf###' 'http://challonge.com/varsity###am' 'http://challonge.com/varsity###' > austinmelee.txt
	cp austinmelee.txt lib/austinmelee.html
	cp lib/austinmelee.html ../../dkelle.github.io/smash/
	vim lib/austinmeleesmash.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

sms:
	[ -e sms.txt ] && rm -f sms.txt
	python3 gen_html.py 'http://challonge.com/RAA_###' > sms.txt
	cp sms.txt lib/sms.html
	cp lib/sms.html ../../dkelle.github.io/smash/
	vim lib/sms.html
	echo "~~~ don't forget to commit dkelle.github.io ~~~"

urltest:
	python3 url_test.py

clean:
	rm *.txt
	rm *.pyc
	rm -f *.txt
