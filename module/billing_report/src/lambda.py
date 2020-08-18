from costexplorer import CostExplorer
from datetime import datetime, timedelta
import boto3
from pprint import pprint

roles =[{"arn": "823349916773 ","role": "ChainRole"},{"arn":"371988484697", "role":"ReadOnly"}]


ce = CostExplorer(roles)
pprint(ce.list_child_accounts())
