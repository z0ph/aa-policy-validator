# :white_check_mark: Access Analyzer - Batch Policy Validator

This script will analyze using [AWS Access Analyzer - Policy Validation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html) all your account customer managed IAM policies.

## Usage

> ProTip :bulb: : Use AWS CloudShell to run this directly on your AWS Account

### Install

        $ pip3 install aa-policy-valitor
### Run
        $ python3 -m aa-policy-validator
## Results

Results will be written into `/tmp/findings` folder with a `README.md` file inside.

![findings screenshot](./assets/screenshot.png)
