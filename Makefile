setup-dev-environment:
	pipenv install --dev

test:
	pytest .

linting:
	black .
