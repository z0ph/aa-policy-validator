# :white_check_mark: Access Analyzer - Batch Policy Validator

This script will analyze using [AWS Access Analyzer - Policy Validation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html) all your account customer managed IAM policies.

## Usage

> ProTip :bulb: : Use AWS CloudShell to run this directly on your AWS Account

### Install

        $ python3 -m pip install aa-policy-validator --user
### Run
        $ python3 -m aa-policy-validator

### Update

        $ python3 -m pip install aa-policy-validator -U --user --no-cache-dir
## Results

Results will be written into `/tmp/findings` folder with a `README.md` file inside.

![findings screenshot](./assets/screenshot.png)
