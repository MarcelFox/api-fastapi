install:
	pip install -r requirements.txt

run:
	fastapi run src/main.py

run\:dev:
	fastapi dev src/main.py

run\:uvi:
	uvicorn src.main:app --host 0.0.0.0

run\:uvi\:dev:
	uvicorn src.main:app --host 0.0.0.0 --reload

run\:docker:
	docker compose up --attach api