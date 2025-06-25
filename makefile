
install:
	python3 -m venv .venv

activate:
	source .venv/bin/activate

update:
	pip install -r requirements.txt

run:
	python ollama_chat.py


up:
	docker compose up