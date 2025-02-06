install:
	pip install -r requirements.txt

run:
	fastapi run

run\:dev:
	fastapi dev

run\:uvi:
	uvicorn main:app --host 0.0.0.0

run\:uvi\:dev:
	uvicorn main:app --host 0.0.0.0 --reload