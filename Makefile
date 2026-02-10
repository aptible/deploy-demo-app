
export COMPOSE_IGNORE_ORPHANS ?= true

default: help

## Show this help message
help:
	@echo "\n\033[1;34mAvailable targets:\033[0m\n"
	@awk 'BEGIN {FS = ":"; prev = ""} \
				/^## / {prev = substr($$0, 4); next} \
				/^[a-zA-Z_-]+:/ {if (prev != "") printf "  \033[1;36m%-20s\033[0m %s\n", $$1, prev; prev = ""} \
				{prev = ""}' $(MAKEFILE_LIST) | sort
	@echo

# Initialize the pg or redis data and configuration volume
init-storage:
	docker compose create --pull always --no-recreate --remove-orphans $(SVC)
	docker compose run --rm --remove-orphans --entrypoint 'test -e $(INIT_CHECK_FILE)' $(SVC) || \
	docker compose run --rm --remove-orphans $(SVC) --initialize

# Initialize the postgres container
init-pg:
	$(MAKE) init-storage SVC=pg INIT_CHECK_FILE=/var/db/postgresql.conf

# Initialize the redis containers
init-redis:
	$(MAKE) init-storage SVC=redis INIT_CHECK_FILE=/etc/redis/redis.extra.conf

## Delete all containers and volumes, then initialize containers and run migrations
init: clean build up
	$(MAKE) run CMD="python migrations.py"

# Ensure db, cache, and background are running
up: init-pg init-redis
	docker compose up -d pg redis background

## Run the application locally using docker compose
run-local:
	docker compose up

# Build the docker images
build:
	docker compose build --pull $(BUILD_ARGS)

## Open shell in a docker container
bash: build
	$(MAKE) run CMD=bash

CMD ?= bash
# Run command in a docker container, supports CMD=
run:
	docker compose run --rm --remove-orphans web $(CMD)

## Clean up docker compose resources
clean:
	docker compose down --remove-orphans --volumes
