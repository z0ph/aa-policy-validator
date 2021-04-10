# :white_check_mark: Access Analyzer - Batch Policy Validator

This script will analyze using [AWS Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html) all your account customer IAM Policies.

## Usage

> ProTip :bulb: : Use AWS CloudShell to run this directly on your AWS Account

        $ pip install aa-policy-valitor

Change path to your preferred folder.

        $ mkdir policy-validator
        $ cd policy-validator
        $ aa-policy-validator
## Results

Results will be written into a `findings` folder with a `README.md` file.

![findings screenshot](./assets/screenshot.png)
