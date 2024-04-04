migrate:
	docker-compose run --rm app python src/manage.py migrate $(if $m, api $m,)

makemigrations:
	docker-compose run --rm app python src/manage.py makemigrations
	docker-compose run app bash -c "sudo chown -R ${USER} src/app/migrations/"

createsuperuser:
	docker-compose run --rm app python src/manage.py createsuperuser

collectstatic:
	docker-compose run --rm app python src/manage.py collectstatic --no-input

command:
	python src/manage.py ${c}

shell:
	docker-compose run --rm app python src/manage.py shell

debug:
	docker-compose run --rm app python src/manage.py debug

piplock:
	pipenv install
	sudo chown -R ${USER} Pipfile.lock

lint:
	docker-compose run app bash -c "isort ."
	docker-compose run app bash -c "flake8 --config setup.cfg"
	docker-compose run app bash -c "black --config pyproject.toml ."

check_lint:
	isort --check --diff .
	flake8 --config setup.cfg
	black --check --config pyproject.toml .

test:
	docker-compose run --rm app bash -c "cd src/tests && python -m pytest"

push:
	docker-compose push

pull:
	docker-compose pull

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

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build