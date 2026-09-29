PYTHON ?= .venv/bin/python

.PHONY: setup prepare features train evaluate pipeline test api ui mlflow docker up down

setup:
	python3.12 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements.txt

prepare:
	$(PYTHON) scripts/prepare_data.py

features:
	$(PYTHON) scripts/build_features.py

train:
	$(PYTHON) scripts/train.py

evaluate:
	$(PYTHON) scripts/evaluate.py

pipeline: prepare features train evaluate

test:
	PYTHONPATH=. $(PYTHON) -m pytest -q

api:
	$(PYTHON) -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

ui:
	$(PYTHON) -m streamlit run app/streamlit/app.py --server.port 8501

mlflow:
	$(PYTHON) -m mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 5000

docker:
	docker build -t airlinesense-mlops:production .

up:
	docker compose up --build -d

down:
	docker compose down
