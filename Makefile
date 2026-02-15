.PHONY: up down build test lint

up:
	docker compose up --build -d

down:
	docker compose down -v

build:
	docker compose build

test:
	docker compose run --rm backend pytest

lint:
	docker compose run --rm backend ruff check app
