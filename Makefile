style:
	black . && pylint . && isort .

migrations:
	./src/manage.py makemigrations

migrate:
	./src/manage.py migrate

requirements:
	poetry export -f requirements.txt --without-hashes --without-urls --with dev -o requirements.txt

populate:
	./src/manage.py csvpopulate

up:
	./src/manage.py runserver

test:
	@pytest
