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
    use_llm: bool = False
    anthropic_api_key: str = ""

    # Interest rate paid on the savings Space, as a decimal (0.03 = 3%).
    # TODO: agree a figure as a team and say where it came from in the pitch.
    savings_interest_rate: float = 0.0

    # Frontend dev server, for CORS
    frontend_origin: str = "http://localhost:5173"


settings = Settings()
