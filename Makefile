.PHONY: backend, frontend

python=./fra-venv/bin/python
pip=./fra-venv/bin/pip

$(python):
	python3 -m venv ./fra-venv
	$(pip) install --requirement ./fra-back/requirements.txt


venv: ./fra-venv/bin/python

frontend:
	cd fra-front; PORT=3001 npm start

backend: venv
	FLASK_APP=./fra-back/app.py ./fra-venv/bin/python -m flask run --port=5001
