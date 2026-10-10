from openai import AzureOpenAI
from app.config import settings

def openai_client():

  azure_openai_api_key = settings.azure_openai_api_key
  azure_openai_endpoint = settings.azure_openai_endpoint

  client = AzureOpenAI(
    api_version="2024-12-01-preview",
    api_key=azure_openai_api_key,
    azure_endpoint=azure_openai_endpoint,
  )

  return client