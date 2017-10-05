from haikunator import Haikunator
from common import AzureContext
from management import ContainerInstanceManager

# TODO: document this

haikunator = Haikunator()

def create_manager():
   """ Creates the sample container instance manager (found in ./management).

      remarks: 
      see README for information on obtaining the service principal attributes
      client id, secret, etc. 
   """
   azure_context = AzureContext(
      subscription_id = '<SUBSCRIPTION ID>',
      client_id = '<CLIENT ID>',
      client_secret = '<CLIENT SECRET>',
      tenant = '<TENANT ID (AZURE ACTIVE DIRECTORY)>'
   )
   resource_group_name = 'container-instances-wispydawn7754' #'container-instances-' + haikunator.haikunate(delimiter='')
   return ContainerInstanceManager(azure_context).with_resource_group(
         name = resource_group_name,
         location = 'eastus'
      )

def main():
   """Azure Container instance example."""

   # 1. Create the custom manager
   # 2. Define and create the ACI
   # 3. Get the newly created instance
   # 4. Clean up all the resources

   manager = create_manager()

   name = "myapline"

   manager.create(name = "myapline", image = "alpine:latest", cpu = 1, memory = 1)
   instance = manager.get(name)

   manager.delete(name)

if __name__ == "__main__":
    main()
