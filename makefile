
help:
	echo "install"
	echo "activate"
	echo "update"
	echo "run"
	echo "up"

install:
	python3 -m venv .venv

activate:
	. .venv/bin/activate

update:
	pip install -r requirements.txt

run:
	python ollama_chat.py

test:
	python test.py

up:
	docker compose up
