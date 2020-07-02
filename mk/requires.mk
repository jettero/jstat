
requirements.txt: grok-requires.py mk/requires.mk
	./$< > $@

install-reqs: requirements.txt
	pip install --upgrade pip
	pip install --upgrade -r $<
