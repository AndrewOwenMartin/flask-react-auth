.PHONY: backend, frontend

python=fra-venv/bin/python
pip=./fra-venv/bin/pip

$(python):
	python3 -m venv ./fra-venv
	$(pip) install --requirement ./fra-back/requirements.txt


venv: ./fra-venv/bin/python

frontend:
	cd fra-front; PORT=3001 npm start

# OATHLIB_INSECURE_TRANSPORT=1 allows use of insecure http to test OAUTH
# OAUTHLIB_RELAX_TOKEN_SCOPE does something similar, that only affects local testing
backend: venv
	cd fra-back; \
	OAUTHLIB_RELAX_TOKEN_SCOPE=1 \
	OAUTHLIB_INSECURE_TRANSPORT=1 \
	FLASK_DEBUG=1 \
	FLASK_APP=./fra_back/app.py \
	../${python} -m flask run --port=5001

readme: venv
	$(python) -m grip
