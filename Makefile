migrate:
	python src/manage.py migrate $(if $m, api $m,)

makemigrations:
	python src/manage.py makemigrations
	sudo chown -R ${USER} src/app/migrations/

createsuperuser:
	python src/manage.py createsuperuser

collectstatic:
	python src/manage.py collectstatic --no-input

command:
	python src/manage.py ${c}

shell:
	python src/manage.py shell

debug:
	python src/manage.py debug

piplock:
	pipenv install
	sudo chown -R ${USER} Pipfile.lock

lint:
	isort .
	flake8 --config setup.cfg
	black --config pyproject.toml .

check_lint:
	isort --check --diff .
	flake8 --config setup.cfg
	black --check --config pyproject.toml .

local_start_app:
	python src/manage.py runserver 0.0.0.0:8000

local_start_bot:
	python src/manage.py start_bot

start_app:
	docker-compose up -d app --build

stop_app:
	docker-compose stop app

start_bot:
	docker-compose up -d bot --build

stop_bot:
	docker-compose stop bot