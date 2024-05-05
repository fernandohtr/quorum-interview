style:
	black . && pylint . && isort .

migrations:
	./src/manage.py makemigrations

migrate:
	./src/manage.py migrate
