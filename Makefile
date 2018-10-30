# ex: set ts=8 noet:

venv: requirements.txt
	python3 -m venv venv
	./venv/bin/pip install -U pip
	./venv/bin/pip install -Ur requirements.txt
	
