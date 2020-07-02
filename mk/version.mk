version: jstat/__version__.py

# probably we can do better than .git/HEAD
jstat/__version__.py: setup.py .git/HEAD mk/version.mk
	./setup.py --version
