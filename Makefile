build:
	docker-compose build device-registry

start:
	docker-compose up

test:
	docker-compose run --rm device-registry python -m unittest
