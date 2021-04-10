import boto3
import json
import glob
import logging
import os
from datetime import date
from collections import OrderedDict

# Date
today = date.today()
date = today.strftime("%Y-%m-%d")

# Setup logging
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)


# Empty ./findings/ folder
def clean_findings_folder():
    finds = glob.glob('./findings/*')
    for find in finds:
        os.remove(find)


# Get IAM Policies based on Scope
def get_policies():
    scope = "Local"
    client = boto3.client('iam')
    try:
        r = client.list_policies(
            Scope=scope,
            MaxItems=1000
        )
    except Exception as e:
        logging.error(e)
    policies = r["Policies"]
    count_policy = 0
    for policy in policies:
        count_policy += 1
        PolicyName = policy["PolicyName"]
        DefaultVersionId = policy["DefaultVersionId"]
        Arn = policy["Arn"]
        logging.info("GetPolicy: %s", PolicyName)
        try:
            r = client.get_policy_version(
                PolicyArn=Arn,
                VersionId=DefaultVersionId
            )
        except Exception as e:
            logging.error(e)

        doc = json.dumps(r['PolicyVersion']['Document'], indent=4, sort_keys=True)
        path_output = "./policies/" + PolicyName + ".json"
        writer = open(path_output, "w")
        writer.write(str(doc))
        writer.close()
    logging.info("Policies Count: %s", count_policy)


# Validate with AA for each Policy
def validate_policies():
    to_analyze = 5000
    analyzed_count = error = fail = sec_warning = suggestion = warning = 0
    error_list = []
    fail_list = []
    sec_warning_list = []
    suggestion_list = []
    warning_list = []
    policy_path = './policies'
    files = [f for f in glob.glob(policy_path + "**/*", recursive=True)]
    for f in files[:to_analyze]:
        policy_name = f.replace("./policies/", "")
        analyzed_count += 1
        with open(f) as policy:
            logging.info("Validation of: %s", f)
            policy = policy.read()
            policy = json.loads(policy)
            doc = json.dumps(policy)

            # Access Analyzer - Policy Validation
            client = boto3.client('accessanalyzer')
            try:
                r = client.validate_policy(
                    policyDocument=str(doc),
                    policyType='IDENTITY_POLICY'
                )
            except Exception as e:
                fail += 1
                fail_list.append(policy_name)
                # Distinct list
                fail_list = list(OrderedDict.fromkeys(fail_list))
                # Write errors to a log file
                error_output = open("./findings/fails.txt", "w")
                error_output.write(str(f) + '\n')
                error_output.write(str(e))
                error_output.close()

            # Extract findings from response
            findings = r['findings']
            # More readable output (json)
            readable_findings = json.dumps(findings, indent=4, sort_keys=True)
            if readable_findings != "[]":
                logging.info("==> Issue detected!")
            else:
                logging.info("==> No issue detected")

            # Export to findings (if not empty) folder with a json file per AWS Managed Policy
            if len(findings) > 0:
                file_name = f.split("/")
                file_name = file_name[2]

                results = "./findings/" + file_name + ".json"
                finding_output = open(results, "a")
                finding_output.write(readable_findings)
                finding_output.close()

            # Count for stats
            for finding in findings:
                # Possible Types: 'ERROR'|'SECURITY_WARNING'|'SUGGESTION'|'WARNING'
                if finding['findingType'] == 'ERROR':
                    error += 1
                    error_list.append(policy_name)
                    # Distinct on list
                    error_list = list(OrderedDict.fromkeys(error_list))
                if finding['findingType'] == 'SECURITY_WARNING':
                    sec_warning += 1
                    sec_warning_list.append(policy_name)
                    # Distinct on list
                    sec_warning_list = list(OrderedDict.fromkeys(sec_warning_list))
                if finding['findingType'] == 'SUGGESTION':
                    suggestion += 1
                    suggestion_list.append(policy_name)
                    # Distinct on list
                    suggestion_list = list(OrderedDict.fromkeys(suggestion_list))
                if finding['findingType'] == 'WARNING':
                    warning += 1
                    warning_list.append(policy_name)
                    # Distinct on list
                    warning_list = list(OrderedDict.fromkeys(warning_list))

    return analyzed_count, error, fail, sec_warning, suggestion, warning, \
        error_list, fail_list, sec_warning_list, suggestion_list, warning_list


# Create README.md report
def output_writer(analyzed_count, error, fail, sec_warning, suggestion, warning,
    error_list, fail_list, sec_warning_list, suggestion_list, warning_list):

    stats_output = open("./findings/README.md", "a")
    stats_output.write("## AWS Access Analyzer - Findings - " + str(date) + "\n\n")
    stats_output.write("- Policies analyzed: `" + str(analyzed_count) + "`\n")
    stats_output.write("- Errors: `" + str(error) + "`\n")
    for i in error_list:
        stats_output.write("  - [`" + str(i) + "`](./" + str(i) + ".json)\n")
    stats_output.write("- Sec_Warnings: `" + str(sec_warning) + "`\n")
    for i in sec_warning_list:
        stats_output.write("  - [`" + str(i) + "`](./" + str(i) + ".json)\n")
    stats_output.write("- Suggestions: `" + str(suggestion) + "`\n")
    for i in suggestion_list:
        stats_output.write("  - [`" + str(i) + "`](./" + str(i) + ".json)\n")
    stats_output.write("- Warnings: `" + str(warning) + "`\n")
    for i in warning_list:
        stats_output.write("  - [`" + str(i) + "`](./" + str(i) + ".json)\n")
    stats_output.write("- Fails: `" + str(fail) + "`\n")
    for i in fail_list:
        stats_output.write("  - [`" + str(i) + "`](./" + str(i) + ".json)\n")
    stats_output.close()



def stats(analyzed_count, error, fail, sec_warning, suggestion, warning):
    logging.info("======== stats =======")
    logging.info("policies analyzed: %s", analyzed_count)
    logging.info("errors: %s", error)
    logging.info("sec_warnings: %s", sec_warning)
    logging.info("suggestions: %s", suggestion)
    logging.info("warnings: %s", warning)
    logging.info("fail: %s", fail)
    logging.info("======================")

def main(event, context):
    get_policies()
    clean_findings_folder()
    analyzed_count, error, fail, sec_warning, suggestion, warning, \
        error_list, fail_list, sec_warning_list, suggestion_list, warning_list = validate_policies()
    output_writer(analyzed_count, error, fail, sec_warning, suggestion, warning,
        error_list, fail_list, sec_warning_list, suggestion_list, warning_list)
    stats(analyzed_count, error, fail, sec_warning, suggestion, warning)


if __name__ == '__main__':
    main(0, 0)
