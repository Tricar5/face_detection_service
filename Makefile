ifeq ($(shell test -e '.env' && echo -n yes),yes)
	include .env
endif

# Manually define main variables

ifndef APP_PORT
override APP_PORT = 8080
endif

ifndef APP_HOST
override APP_HOST = 127.0.0.1
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))
ifndef args
MESSAGE = "No such command (or you pass two or many targets to ). List of possible commands: make help"
else
MESSAGE = "Done"
endif

APPLICATION_NAME=detector
ROOT=`echo $(PWD)`

TEST = poetry run python3 -m pytest --verbosity=2 --showlocals --log-level=DEBUG
CODE = $(APPLICATION_NAME) tests
DOCKER_RUN = docker run -p 8000:8000 -it --env-file .env $(APPLICATION_NAME)

HELP_FUN = \
	%help; while(<>){push@{$$help{$$2//'options'}},[$$1,$$3] \
	if/^([\w-_]+)\s*:.*\#\#(?:@(\w+))?\s(.*)$$/}; \
    print"$$_:\n", map"  $$_->[0]".(" "x(20-length($$_->[0])))."$$_->[1]\n",\
    @{$$help{$$_}},"\n" for keys %help; \

# Commands
env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.example .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env


args := $(wordlist 2, 100, $(MAKECMDGOALS))

# Code style

fmt:
	poetry run python3 -m isort $(APPLICATION_NAME)
	poetry run python3 -m black $(APPLICATION_NAME)

lint:
	poetry run pylint ${APPLICATION_NAME}



# Docker

db:
	docker compose --env-file ./.env -f deploy/docker-compose.yml up db -d

open_db:  ##@Database Open database inside docker-image
	docker exec -it db psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

# Docker building

docker-build:
	docker compose --env-file ./.env -f deploy/docker-compose.yml build $(args)

docker-run:
	docker compose --env-file ./.env -f deploy/docker-compose.yml up -d --remove-orphans


# Application cmds

run:
	uvicorn ${APPLICATION_NAME}.__main__:app --reload --port 8080

celery:
	celery -A detector.tasks.app_worker worker

# Migrations

revision:
	cd ${APPLICATION_NAME}/db && alembic revision --autogenerate -m $(args)

migrate:
	cd ${APPLICATION_NAME}/db && alembic upgrade $(args)

migrate-downgrade:
	cd ${APPLICATION_NAME}/db && alembic downgrade -1

# Tests

test:  ##@Testing Test application with pytest
	make db && $(TEST)

test-cov:  ##@Testing Test application with pytest and create coverage report
	make db && $(TEST) --cov=$(APPLICATION_NAME) --cov-report html --cov-fail-under=70
