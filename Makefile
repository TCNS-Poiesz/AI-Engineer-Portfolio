
.PHONY: setup notebook dashboard api

setup:
	python -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt

notebook:
	. .venv/bin/activate && jupyter lab

dashboard:
	. .venv/bin/activate && streamlit run dashboard/app.py

api:
	. .venv/bin/activate && uvicorn api.main:app --reload
