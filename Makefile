setup-dev-environment:
	pipenv install --dev

test:
	pytest . -vv

linting:
	black .

setup-run-environment:
	pipenv install

run:
	python src/main.py
