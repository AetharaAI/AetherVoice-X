.PHONY: up down logs test smoke fmt

up:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

test:
	PYTHONPATH=services/worker-common:services/gateway:services/asr:services/tts pytest tests/unit

smoke:
	./scripts/smoke_test.sh

fmt:
	python -m compileall services
