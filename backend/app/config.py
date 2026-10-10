"""Settings, read from environment variables or backend/.env.

Shared file: set up by Person 3, anyone can add a setting (tell the team).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Mock Engine Core
    engine_url: str = "http://localhost:8001"

    # ONS Beta API
    ons_base_url: str = "https://api.beta.ons.gov.uk/v1"
    ons_dataset: str = "cpih01"
    ons_geography: str = "K02000001"  # UK
    offline: bool = False  # True = never call ONS, read the cache only

    # LLM fallback for categorising unknown merchants
    use_llm: bool = True

    # Azure OpenAI (used by app/services/openai.py)
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = ""  # the model deployment name in Azure
    
    # Easy Saver standard rate (AER), excluding the first-year bonus.
    # Source: starlingbank.com/savings, checked 2026-10-10
    savings_interest_rate: float = 0.025

    # Frontend dev server, for CORS
    frontend_origin: str = "http://localhost:5173"


settings = Settings()
