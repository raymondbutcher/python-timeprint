app = $(shell python setup.py --name)
sdist := dist/$(shell python setup.py --fullname).tar.gz
src := $(wildcard *.py)

.PHONY: all
all: build

.PHONY: build
build: $(sdist)

$(sdist): $(src)
	python setup.py sdist

.PHONY: install
install: $(sdist)
	pip install $(sdist)

.PHONY: uninstall
uninstall:
	pip uninstall $(app)

.PHONY: clean
clean:
	rm -rf dist $(app).egg-info

.PHONY: test tests
test tests:
	python -m tests
