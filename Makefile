PROJECT=manageritm
PYTESTOPTS?=
PYTHON_VERSION?=3.9.11

.PHONY: pyenv
pyenv:
	pyenv install ${PYTHON_VERSION} --skip-existing
	pyenv virtualenv-delete ${PROJECT} || true
	pyenv virtualenv ${PYTHON_VERSION} ${PROJECT}
	pyenv local ${PROJECT}
	pip install poetry
	sed -i '/export VIRTUAL_ENV=/d' .envrc || true
	echo "export VIRTUAL_ENV=\$$$\(pyenv prefix)" >> .envrc
	direnv allow || true
	poetry install

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

.PHONY: server
server:
	poetry run gunicorn --bind localhost:8000 --workers 1 --log-level debug "manageritm.app:main()"

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
