PYTESTOPTS?=

.PHONY: all
all:
	poetry build

.PHONY: install
install:
	poetry install

.PHONY: run
run:
	FLASK_APP="manageritm.app:create_app()" \
	FLASK_ENV=development \
	poetry run flask run

.PHONY: test
test:
	poetry run pytest \
	    --verbose \
	    --tb=short \
	    ${PYTESTOPTS}

.PHONY: clean
clean:
	find . \( -name '*.pyc' -or -name '*.pyo' \) -print -delete
	find . -name '__pycache__' -print -delete
	rm -rf hars
