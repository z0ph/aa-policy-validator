.DEFAULT_GOAL := help

help:
	@echo "install - get started with batch policy validator"
	@echo "run - run local validation of your AWS Account IAM Policies"

venv: clean-venv
	virtualenv --python=python3 venv

clean-venv:
	rm -rf venv

install: venv
	venv/bin/pip install -U aa-policy-validator

run:
	venv/bin/python3 -m aa-policy-validator