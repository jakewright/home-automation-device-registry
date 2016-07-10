.PHONY: start
start:
	docker-compose up

.PHONY: test
test:
	docker-compose run --rm python python -m unittest
