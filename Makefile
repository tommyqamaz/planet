APP_PORT := 1818
DOCKER_TAG := latest
DOCKER_IMAGE := planet
DVC_REMOTE_NAME := kekus

DEPLOY_HOST := demo_host

.PHONY: run
run:
	poetry run python -m uvicorn app:app --host='0.0.0.0' --port=$(APP_PORT)

.PHONY: download_weights
download_weights:
	poetry run dvc pull

.PHONY: run_unit_tests
run_unit_tests:
	PYTHONPATH=. poetry run pytest tests/unit/

.PHONY: run_integration_tests
run_integration_tests:
	PYTHONPATH=. poetry run pytest tests/integration/

.PHONY: run_all_tests
run_all_tests:
	make download_weights
	make run_unit_tests
	make run_integration_tests

.PHONY: lint
lint:
	@poetry run flake8 .

.PHONY: install
install:
	pip install poetry && poetry --version && poetry config virtualenvs.in-project true && poetry install -vv --no-root


.PHONY: test-coverage
test-coverage:
	PYTHONPATH=. poetry run pytest --cov-report html --cov-report term-missing --cov=src/ tests/

.PHONY: install_c_libs
install_c_libs:
	apt-get update && apt-get install -y --no-install-recommends gcc ffmpeg libsm6 libxext6

.PHONY: init_dvc
init_dvc:
	dvc init --no-scm
	dvc remote add --default $(DVC_REMOTE_NAME) ssh://91.206.15.25/home/$(USERNAME)/dvc_files
	dvc remote modify $(DVC_REMOTE_NAME) user $(USERNAME)
	dvc config cache.type hardlink,symlink

.PHONY: build
build:
	docker build -f Dockerfile . --force-rm=true -t $(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: docker-run
docker-run:
	docker run -it --expose 1818 --name planet_service planet

.PHONY: deploy
deploy:
	ansible-playbook -i deploy/ansible/inventory.ini  deploy/ansible/deploy.yml \
		-e host=$(DEPLOY_HOST) \
		-e docker_image=$(DOCKER_IMAGE) \
		-e docker_tag=$(DOCKER_TAG) \
		-e docker_registry_user=$(CI_REGISTRY_USER) \
		-e docker_registry_password=$(CI_REGISTRY_PASSWORD) \
		-e docker_registry=$(CI_REGISTRY) \


.PHONY: destroy
destroy:
	ansible-playbook -i deploy/ansible/inventory.ini deploy/ansible/destroy.yml \
		-e host=$(DEPLOY_HOST)
