
BR := $(shell git symbolic-ref HEAD | sed -e 's,.*/,,')

rebase:
	git pull --rebase git@github.com:jettero/jstat.git $(BR)
