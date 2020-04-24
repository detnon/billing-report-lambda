from costexplorer import CostExplorer
from datetime import datetime, timedelta
import boto3
from pprint import pprint


def lambda_handler(event, context):
    time_start = datetime.today() - timedelta(31)
    time_start_del = time_start.strftime("%Y-%m-%d")
    time_end = datetime.today().strftime("%Y-%m-%d")

    ce = CostExplorer(
        "CostExplorerAccounts", "CostExplorerArn", time_start_del, time_end
    )
    pprint(ce.build_results())
