
activate:
	source .venv/bin/activate

install:
	pip install -r requirements.txt

run:
	python ollama_chat.py