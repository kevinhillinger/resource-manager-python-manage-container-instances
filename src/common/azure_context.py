from azure.common.credentials import ServicePrincipalCredentials

class AzureContext(object):
   """Azure Security Context"""
   
   def __init__(self, subscription_id, client_id, client_secret, tenant):
      self.credentials = ServicePrincipalCredentials(
         client_id = client_id,
         secret = client_secret,
         tenant = tenant
      )
      self.subscription_id = subscription_id

   def create_client(self, client_type): 
      return client_type(self.credentials, self.subscription_id)