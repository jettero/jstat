
PY := $(shell which python3)

imake := make --no-print-directory

default:
	@+ $(imake) install-reqs
	@+ $(imake) version
	@+ $(imake) test

include mk/*.mk

test: install-reqs
	$(PY) -m pytest

clean:
	git clean -dfx
