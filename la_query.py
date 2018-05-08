import adal
import requests
import azure
import json
from msrestazure.azure_active_directory import AdalAuthentication
from azure.mgmt.resource import ResourceManagementClient
from msrestazure.azure_cloud import AZURE_US_GOV_CLOUD


# ---------------------------------------------------
# Replace these
TENANT_ID = '{your tenant id}'
CLIENT = '{your client id}'
KEY = '{your client key}'
SUB_ID = '{your subscription id}'
resource_group_name = '{your resource group name}'
workspace_name = '{your workspace name}'
# ----------------------------------------------------

LOGIN_ENDPOINT = AZURE_US_GOV_CLOUD.endpoints.active_directory
RESOURCE = AZURE_US_GOV_CLOUD.endpoints.active_directory_resource_id

context = adal.AuthenticationContext(LOGIN_ENDPOINT + '/' + TENANT_ID)
token = context.acquire_token_with_client_credentials(RESOURCE, CLIENT, KEY)

headers = {
    'Authorization': "Bearer {0}".format(token['accessToken']),
    'Content-Type': 'application/json'
}

query = { 
    "query": "Heartbeat | where TimeGenerated > ago(1h) | summarize max(TimeGenerated) by Computer" 
}

url = "{arm}/subscriptions/{sub_id}/resourceGroups/{rg_name}/providers/Microsoft.OperationalInsights/workspaces/{workspace_name}/api/query?api-version=2017-01-01-preview".format(
    arm=AZURE_US_GOV_CLOUD.endpoints.resource_manager ,sub_id=SUB_ID, rg_name=resource_group_name, workspace_name=workspace_name)

s = requests.post(url, data=json.dumps(query), headers=headers) 
r = requests.get(url, headers=headers)
print ("status code of post: {}".format(s.status_code))
print ("status code of get: {}".format(r.status_code)) 

print json.dumps(s.json(), indent=4)
