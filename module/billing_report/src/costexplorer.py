import boto3
import json


class CostExplorer:
    def __init__(self, role_ssm_name):
        #self.ssm_secret = role_ssm_name
        # self.ssm_accounts = accounts_ssm_name

        self.roles = role_ssm_name


        # self.roles = self.retrieve_secrets(self.ssm_secret)
        # self.accounts = self.retrieve_secrets(self.ssm_accounts)

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

    def create_service(self,service):
        creds = self.assume_billing_role(self.roles)
        return self.new_client(service, creds[0], creds[1], creds[2])

    def list_child_accounts(self):
        return self.create_org_service("organizaions").list_accounts_for_parent(
            ParentId='371988484697',
            MaxResults=999)
