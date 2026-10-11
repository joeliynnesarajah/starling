import json
import logging
from pathlib import Path

from app.config import settings

LOGGER = logging.getLogger(__name__)

CACHE_FILE = Path(__file__).resolve().parent / "llm_cache.json" #Where saved AI answer are stored

# The only answers we accept
DIVISIONS = {
    "01": "Food and non-alcoholic drinks",
    "02": "Alcohol and tobacco",
    "03": "Clothing and footwear",
    "04": "Housing, water, electricity, gas",
    "05": "Furniture and household goods",
    "06": "Health",
    "07": "Transport",
    "08": "Communication (phone, internet)",
    "09": "Recreation and culture",
    "10": "Education",
    "11": "Restaurants, cafes and hotels",
    "12": "Other (insurance, personal care, etc.)",
}


def _llm_enabled() -> bool: #Checks the AI is switched on and has a key
    # Only run if the team switched it on and the Azure key is set
    enabled = bool(
        getattr(settings, "use_llm", False)
        and getattr(settings, "azure_openai_api_key", None)
    )
    LOGGER.info("LLM enabled: %s", enabled)
    return enabled


def _load_cache() -> dict:
    # Read saved answers from earlier runs (empty if no file yet)
    try:
        return json.loads(CACHE_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, indent=2, sort_keys=True))


def _ask_llm(merchants: list[str]) -> dict:
    # Send ALL the shop names in ONE request and get JSON back( OpenAI in one message)
    from app.services.openai import openai_client  # the team's Azure setup

    client = openai_client()
    category_list = "\n".join(f"{code}: {name}" for code, name in DIVISIONS.items())

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You classify UK merchant names into spending categories by the TYPE of business. "
                    f"Categories:\n{category_list}\n\n"
                    "Reply with ONLY a JSON object mapping each merchant name exactly as given "
                    "to a category code, or null if you can't tell. No other text."
                ),
            },
            {
                "role": "user",
                "content": "Merchants:\n" + "\n".join(merchants),
            },
        ],
        max_tokens=1024,
        temperature=0,
        model=settings.azure_openai_deployment,
    )

    text = response.choices[0].message.content
    LOGGER.info(text)
    # Take just the {...} part, in case the model adds extra words
    return json.loads(text[text.find("{"): text.rfind("}") + 1])


def classify_merchants(merchants: list[str]) -> dict[str, str | None]:
    """{merchant name: division code or None}."""
    # Switched off, or no key: answer "don't know" for everything
    if not _llm_enabled():
        return {m: None for m in merchants}

    cache = _load_cache()
    new_names = [m for m in merchants if m not in cache]

    # Only ask about shops we haven't asked about before
    if new_names:
        try:
            answers = _ask_llm(new_names)
        except Exception as e:
            LOGGER.exception(f"LLM categorisation failed: {e}")
            answers = None  # don't crash, but don't cache the failure
        if answers is not None:
            for name in new_names:
                code = answers.get(name)
                cache[name] = code if code in DIVISIONS else None
            _save_cache(cache)

    return {m: cache.get(m) for m in merchants} 
   