setup-dev-environment:
	pipenv install --dev

test:
	pytest . -vv

linting:
	black .

setup-container-environment:
	pipenv install --system --deploy

build-image:
	bash ./container/build-image.sh

create-container: build-image
	bash ./container/create-container.sh

start-container:
	bash ./container/start-container.sh

stop-container:
	bash ./container/stop-container.sh

clean-environment:
	bash ./container/clean.sh

run:
	python src/main.py

start-devcontainer:
	./scripts/start-devcontainer.sh

nvim-devcontainer: start-devcontainer
	./scripts/exec-in-devcontainer.sh nvim

bash-devcontainer: start-devcontainer
	./scripts/exec-in-devcontainer.sh bash

