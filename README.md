# :white_check_mark: Access Analyzer - Batch Policy Validator

This script will analyze using [AWS Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html) all your account customer IAM Policies.

## Requirements

- Python3

## Usage

        $ make install
        $ make run
## Results

Results will be written into a `findings` folder with a [`README.md`](./findings/README.md) file.
