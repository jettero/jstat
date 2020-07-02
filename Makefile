
PY := $(shell which python3)

MAKE_AGAIN := make --no-print-directory

default:
	@+ $(MAKE_AGAIN) install-reqs
	@+ $(MAKE_AGAIN) version
	@+ $(MAKE_AGAIN) test

include mk/*.mk

test: install-reqs
	$(PY) -m pytest

clean:
	git clean -dfx
