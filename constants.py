# Constants
MAX_ATTEMPTS = 3
LOGGER_NAME = 'app-logger'
JENKINS_ASSUMED_ROLE_ARN = \
    "arn:aws:iam::{ACCOUNT}:role/mra-jenkins-deploy-role-" \
    "{ACCOUNT_ENV}-{REGION}"
JENKINS_SESSION_ID = "MRA-Jenkins-Deploy"
S3_LAMBDA_REPO = "mra-lambda-repo-us-east-1"
ENV_TO_ACCOUNT_MAP = {
    'sbx':  {'account_env': 'sbx',  'account_id': '731179564832'},
    'tst':  {'account_env': 'nprd', 'account_id': '938540043867'},
    'dev':  {'account_env': 'nprd', 'account_id': '938540043867'},
    # 'dev': {'account_env': 'nprod', 'account_id': '165339645591'},
    'dev2': {'account_env': 'nprd', 'account_id': '938540043867'},
    'dev3': {'account_env': 'nprd', 'account_id': '938540043867'},
    'qa':   {'account_env': 'nprd', 'account_id': '938540043867'},
    'qa2':  {'account_env': 'nprd', 'account_id': '938540043867'},
    'qa3':  {'account_env': 'nprd', 'account_id': '938540043867'},
    'perf': {'account_env': 'nprd', 'account_id': '938540043867'},
    'uat':  {'account_env': 'nprd', 'account_id': '938540043867'},
    'prd':  {'account_env': 'prd',  'account_id': '827773453376'}
}
WEBSITE_BUCKET = "{APP}-{ENV}-website-{REGION}"
ZIPFILE_NAME = "temp.zip"
