import boto3
import json


class CostExplorer:
    def __init__(self, accounts_ssm_name, role_ssm_name, start, end):
        self.ssm_secret = role_ssm_name
        self.ssm_accounts = accounts_ssm_name
        self.roles = self.retrieve_secrets(self.ssm_secret)
        self.accounts = self.retrieve_secrets(self.ssm_accounts)
        self.start_date = start
        self.end_date = end

    def assume_billing_role(self, roles):
        client = boto3.client("sts")
        for role in self.roles:
            creds = self.assume_role(role["arn"], role["role"], client)
            client = self.new_client("sts", creds[0], creds[1], creds[2])
        return creds

    def assume_role(self, arn, role, client):
        client_name = client.assume_role(
            RoleArn=f"arn:aws:iam::{arn}:role/{role}", RoleSessionName=role
        )
        return self.get_credential_list(client_name)

    def get_credential_list(self, client_name):
        return [i for i in client_name["Credentials"].values()]

    def new_client(
        self, service, aws_access_key_id, aws_secret_access_key, aws_session_token
    ):
        return boto3.client(
            service,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
        )

    def retrieve_secrets(self, secret_name):
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name="eu-west-2")
        secrets = client.get_secret_value(SecretId=secret_name)
        return json.loads(secrets["SecretString"])

    def create_cost_explorer_service(self):
        creds = self.assume_billing_role(self.roles)
        return self.new_client("ce", creds[0], creds[1], creds[2])

    def build_results(self):
        cost_results = []
        for account in self.accounts:
            cost = {}
            response = self.create_cost_explorer_service().get_cost_and_usage(
                TimePeriod={"Start": self.start_date, "End": self.end_date},
                Granularity="MONTHLY",
                Metrics=["UnblendedCost"],
                Filter={
                    "Dimensions": {
                        "Key": "LINKED_ACCOUNT",
                        "Values": [account["AccountID"]],
                    }
                },
            )
            cost.update({account["AccountName"]: response["ResultsByTime"]})
            cost_results.append(cost)
        return cost_results
