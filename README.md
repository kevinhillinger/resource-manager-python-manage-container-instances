---
services: azure-containerinstance
platforms: python
author: kehilli
---

# Manage Azure Container Instances 

This sample shows how to use the Python SDK to create, retreive, and delete Azure Container Instances, 
using Managed Service Identity (MSI) authentication.

**Outline**

- [Running the sample](#run)
- [What is example.py doing?](#example)
    - [Create a MSI authentication instance](#create-credentials)
    - [Get the subscription ID of that token](#subscription_id)
    - [List resource groups](#list-groups)

<a id="run"></a>
## Running the example

### Setting up your environment
You need to have the following installed on the development environment you will be running the sample from.

1. Install [Python](https://www.python.org/downloads/)

2. Initialize a virtual environment (optional)

   > TIP: using [virtual environnements](https://docs.python.org/3/tutorial/venv.html) is recommended, but not required. To initialize a virtual environment, run the following, replacing `<myvirtualenv> with the name you would like:

    ```
    pip install virtualenv
    virtualenv <myvirtualenv>
    cd <myvirtualenv>
    source bin/activate
    ```

3. Clone the repository.

    ```
    git clone https://github.com/Azure-Samples/resource-manager-python-manage-container-instances.git
    ```

4. Install the dependencies using pip.

    ```
    cd resource-manager-python-manage-container-instances
    pip install -r src/requirements.txt
    ```
### Running the sample

Run the sample by opening a terminal window and executing the following command:

```
python src/example.py
```

<a id="example"></a>
## What is example.py doing?

The sample creates a MSI Authentication credentials class. Then it uses this credentials to
extract the current subscription ID. Finally it uses this credentials and subscription ID
to list all the available Resource Groups.

Note that listing Resource Group is just an example, there is no actual limit of what you can do with this 
credentials (creating a KeyVault account, managing the Network of your VMs, etc.). The limit
will be defined by the roles and policy assigned to the MSI token at the time of the creation of the VM.

<a id="create-credentials"></a>
### Create a MSI authentication instance

```python
from msrestazure.azure_active_directory import MSIAuthentication

credentials = MSIAuthentication()
```

<a id="subscription_id"></a>
### Get the subscription ID of that token

```python
from azure.mgmt.resource import SubscriptionClient

subscription_client = SubscriptionClient(credentials)
subscription = next(subscription_client.subscriptions.list())
subscription_id = subscription.subscription_id
```

<a id="list-groups"></a>
### List resource groups

List the resource groups in your subscription.

```python
from azure.mgmt.resource import ResourceManagementClient

resource_client = ResourceManagementClient(credentials, subscription_id)
for item in resource_client.resource_groups.list():
    print(resource_group.name)
```
