from azureml.core import Workspace
from azureml.core import Environment
from azureml.core.authentication import InteractiveLoginAuthentication
interactive_auth = InteractiveLoginAuthentication(tenant_id="ac5c5e7c-0141-491a-a5dd-d3608633ce62")

#ws = Workspace.from_config(auth=interactive_auth)
ws = Workspace.from_config()
#ws = Workspace(subscription_id = "01644559-ad8e-40d4-9bf2-6c5e3213a8bf",
#                      resource_group = "rgAzureNotebooks", 
#                      workspace_name="wsAzureNoteBooks"
#                      ,auth=interactive_auth
#                      )
print("Found workspace {} at location {}".format(ws.name, ws.location))
envs = Environment.list(workspace=ws)

for env in envs:
    if env.startswith("AzureML"):
        print("Name",env)
        print("packages", envs[env].python.conda_dependencies.serialize_to_string())