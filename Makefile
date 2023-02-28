setup-dev-environment:
	pipenv install --dev

test:
	pytest . -vv

linting:
	black .

setup-container-environment:
	pipenv install --system --deploy

build-image:
	./container/build-image.sh

create-container: build-image
	./container/create-container.sh

start-container:
	./container/start-container.sh

stop-container:
	./container/stop-container.sh

clean-environment:
	./container/clean.sh

run:
	python src/main.py
