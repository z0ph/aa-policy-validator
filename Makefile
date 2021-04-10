.DEFAULT_GOAL := help

help:
	@echo "install - get started with batch policy validator"
	@echo "run - run local validation of your AWS Account IAM Policies"

venv: clean-venv
	virtualenv --python=python3 venv

clean-venv:
	rm -rf venv

install: venv
	venv/bin/pip install -U -r requirements.txt
	mkdir -p aa-policy-validator/findings
	mkdir -p aa-policy-validator/policies

run:
	venv/bin/python3 aa-policy-validator/validate-batch.py