import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import (ContainerGroup, Container, ContainerPort, Port, IpAddress,
                                                 ImageRegistryCredential, ResourceRequirements, ResourceRequests,
                                                 ContainerGroupNetworkProtocol, OperatingSystemTypes)

ACR_SERVER_SUFFIX = ".azurecr.io/"

class ContainerInstanceManager(object):
   """Manage container instances"""

   def __init__(self, azure_context):
      self.client          = azure_context.create_client(ContainerInstanceManagementClient)
      self.resource_client = azure_context.create_client(ResourceManagementClient)

   def with_resource_group(self, name, location, resource_group = None):
      if resource_group is not None:
         self.resource_group = resource_group
      else:
         self.resource_group = self.resource_client.resource_groups.create_or_update(name, { 'location': location })

      print("Resource Group: " + self.resource_group.name)
      return self

   def list_containers(self):
      """List all container groups in a resource group. """
      return self.client.container_groups.list_by_resource_group(self.resource_group.name)

   def delete(self, name, **kwargs):
      """Delete a container group. """
      return self.client.container_groups.delete(self.resource_group.name, name)

   def get(self, name):
      """Show details of a container group. """
      return self.client.container_groups.get(self.resource_group.name, name)

   def create(self, name,
               image,
               location = None,
               cpu = 1,
               memory = 1.5,
               port = 80,
               os_type = 'Linux',
               ip_address = None,
               command_line = None,
               environment_variables = None,
               registry_login_server = None,
               registry_username = None,
               registry_password = None, **kwargs):
      """"Create a container group. """

      container_resource_requirements = None

      if cpu is not None or memory is not None:
         container_resource_requests = ResourceRequests(memory_in_gb = memory, cpu = cpu)
         container_resource_requirements = ResourceRequirements(requests = container_resource_requests)

      image_registry_credentials = None

      if registry_login_server is not None:
         if registry_username is None:
            raise CLIError('Please specify a username.')
         if registry_password is None:
            raise CLIError('Please specify a registry_password.')

         image_registry_credentials = [ImageRegistryCredential(server = registry_login_server, username =registry_username, password = registry_password)]
      
      elif ACR_SERVER_SUFFIX in image:
         if registry_password is None:
            raise CLIError('Please specify registry_password')

         acr_server = image.split("/")[0] if image.split("/") else None
         acr_username = image.split(ACR_SERVER_SUFFIX)[0] if image.split(ACR_SERVER_SUFFIX) else None

         if acr_server is not None and acr_username is not None:
            image_registry_credentials = [ImageRegistryCredential(server=acr_server, username=acr_username, password=registry_password)]
         else:
            raise CLIError('Failed to parse ACR server or username from image name; please explicitly specify --registry-server and --registry-username.')

      command = None

      if command_line is not None:
         command = shlex.split(command_line)

      container = Container(name=name,
                           image=image,
                           resources=container_resource_requirements,
                           command=command,
                           ports=[ContainerPort(port=port)],
                           environment_variables=environment_variables)

      cgroup_ip_address = None

      if ip_address is not None and ip_address.lower() == 'public':
         cgroup_ip_address = IpAddress(ports=[Port(protocol=ContainerGroupNetworkProtocol.tcp, port=port)])

      cgroup_os_type = OperatingSystemTypes.linux if os_type.lower() == "linux" else OperatingSystemTypes.windows

      if location is None: location = self.resource_group.location

      cgroup = ContainerGroup(location=location,
                              containers=[container],
                              os_type=cgroup_os_type,
                              ip_address=cgroup_ip_address,
                              image_registry_credentials=image_registry_credentials)

      return self.client.container_groups.create_or_update(self.resource_group.name, name, cgroup)
