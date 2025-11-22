run:
	python -B main.py

pretty:
	isort main.py src/
	black main.py src/