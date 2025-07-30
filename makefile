PROJECT_NAME=ai-lab
# try to import env from .makefile.env
ifneq (,$(wildcard .env))
	include .env
	export $(shell sed 's/=.*//' .env)
endif
DOCKER_COMPOSE_FILE?=compose.yml

help:
	echo "install"
	echo "activate"
	echo "update"
	echo "run"
	echo "up"

init:
	echo $(DOCKER_COMPOSE_FILE)
	if [ ! -f "./.env"                   ]; then cp ./utils/.env.example               ./.env; fi
	if [ ! -f "./utils/nginx.conf"       ]; then cp ./utils/nginx.conf.example         ./utils/nginx.conf; fi

build:
	export DOCKER_BUILDKIT=1 && \
	export COMPOSE_BAKE=true && \
	docker compose -p $(PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) build

run:
	docker compose up

install:
	python3 -m venv .venv

activate:
	. .venv/bin/activate

update:
	pip install -r requirements.txt

test:
	python test.py

makemigrations:
	docker compose -p $(PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec main python manage.py makemigrations
migrate:
	docker compose -p $(PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec main python manage.py migrate
test_data_dump:
	docker compose -p $(PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec main sh utils/test_data_dump.sh
test_data_reset:
	docker compose -p $(PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec main sh utils/test_data_reset.sh
create_superuser:
	docker compose -p $(PROJECT_NAME) -f $(DOCKER_COMPOSE_FILE) exec main python manage.py createsuperuser
