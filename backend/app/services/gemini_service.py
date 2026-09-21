import json
import re
from functools import lru_cache
from typing import Any

import google.generativeai as genai
from loguru import logger

from app.config import get_settings

settings = get_settings()


# Current Gemini models.
PREFERRED_MODELS = (
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
)


# Models to try if the selected model is unavailable
# or has reached its quota.
QUOTA_FALLBACK_MODELS = (
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
)


def _normalize_model_name(name: str) -> str:
    """Remove the models/ prefix if present."""
    return name.removeprefix("models/").strip()


def _is_quota_error(exc: Exception) -> bool:
    """Check whether an exception is a quota/rate-limit error."""
    msg = str(exc).lower()

    return (
        "429" in msg
        or "quota" in msg
        or "rate" in msg
        or "resource_exhausted" in msg
    )


@lru_cache(maxsize=1)
def _discover_available_models() -> tuple[str, ...]:
    """
    Discover models available to the configured Gemini API key.

    Only models supporting generateContent are returned.
    """
    available: list[str] = []

    try:
        for model in genai.list_models():
            methods = (
                getattr(
                    model,
                    "supported_generation_methods",
                    None,
                )
                or []
            )

            if "generateContent" not in methods:
                continue

            short_name = _normalize_model_name(model.name)

            if short_name and short_name not in available:
                available.append(short_name)

    except Exception as exc:
        logger.warning(
            f"Could not list Gemini models: {exc}"
        )

    return tuple(available)


def _pick_model(requested: str) -> str:
    """
    Select a Gemini model.

    Priority:
    1. Requested model if available
    2. Preferred current models
    3. Any available Flash-Lite model
    4. Any available Flash model
    5. Configured model as fallback
    """

    available = _discover_available_models()

    requested = _normalize_model_name(requested)

    if available:

        if requested and requested in available:
            logger.info(
                f"Using requested Gemini model: {requested}"
            )
            return requested

        for preferred in PREFERRED_MODELS:
            if preferred in available:
                logger.info(
                    f"Using Gemini model: {preferred}"
                )
                return preferred

        for name in available:
            lower_name = name.lower()

            if (
                "flash" in lower_name
                and "lite" in lower_name
            ):
                logger.info(
                    f"Using discovered Gemini model: {name}"
                )
                return name

        for name in available:
            if "flash" in name.lower():
                logger.info(
                    f"Using discovered Gemini model: {name}"
                )
                return name

        logger.info(
            f"Using discovered Gemini model: {available[0]}"
        )

        return available[0]

    if requested:
        return requested

    return "gemini-3.1-flash-lite"


class GeminiService:

    def __init__(self) -> None:

        if settings.gemini_api_key:
            genai.configure(
                api_key=settings.gemini_api_key
            )

        self._resolved_model: str | None = None

        # Models that have already returned quota errors
        # during the current server session.
        self._quota_blocked: set[str] = set()


    @property
    def model_name(self) -> str:

        if not self._resolved_model:
            self._resolved_model = _pick_model(
                settings.gemini_model
            )

        return self._resolved_model


    def _models_to_try(self) -> list[str]:
        """
        Build the list of models to try.

        The selected model is tried first, followed by
        the configured fallback models.
        """

        primary = self.model_name

        candidates = [primary]

        for model_name in QUOTA_FALLBACK_MODELS:

            if (
                model_name not in candidates
                and model_name not in self._quota_blocked
            ):
                candidates.append(model_name)

        available = set(
            _discover_available_models()
        )

        if available:
            candidates = [
                model_name
                for model_name in candidates
                if model_name in available
            ]

        return candidates or [primary]


    def _call_model(
        self,
        model_name: str,
        prompt: str,
        temperature: float,
    ) -> str:
        """Send a prompt to Gemini."""

        logger.info(
            f"Calling Gemini model: {model_name}"
        )

        model = genai.GenerativeModel(
            model_name
        )

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 4096,
            },
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty response"
            )

        return response.text


    def generate(
        self,
        prompt: str,
        temperature: float = 0.3,
    ) -> str:
        """
        Generate a text response from Gemini.

        If a model reaches its quota, immediately move
        to the next available model instead of waiting
        for Google's retry period.
        """

        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Add it to backend/.env and restart the server."
            )

        last_error: Exception | None = None

        for model_name in self._models_to_try():

            try:

                text = self._call_model(
                    model_name,
                    prompt,
                    temperature,
                )

                self._resolved_model = model_name

                return text

            except Exception as exc:

                last_error = exc

                if _is_quota_error(exc):

                    self._quota_blocked.add(
                        model_name
                    )

                    logger.warning(
                        f"Quota/rate limit reached on "
                        f"{model_name}. "
                        f"Trying the next model."
                    )

                    # IMPORTANT:
                    # Do NOT wait 60 seconds.
                    # Immediately try the next model.
                    continue

                logger.warning(
                    f"Gemini model {model_name} "
                    f"failed: {exc}"
                )

                # Try the next available model.
                continue


        available = _discover_available_models()

        if available:
            hint = ", ".join(
                available[:8]
            )
        else:
            hint = (
                "gemini-3.1-flash-lite, "
                "gemini-3.5-flash-lite, "
                "gemini-3.5-flash"
            )

        raise ValueError(
            "Gemini request failed. "
            f"Last error: {last_error}. "
            f"Available models: {hint}"
        ) from last_error


    def generate_json(
        self,
        prompt: str,
    ) -> dict[str, Any]:
        """Generate and parse a JSON response."""

        text = self.generate(
            prompt
            + "\n\nRespond with valid JSON only, "
            "with no markdown code fences."
        )

        cleaned = text.strip()

        # Remove markdown JSON fences.
        cleaned = re.sub(
            r"^```json\s*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError:

            # Try to locate the outermost JSON object.
            start = cleaned.find("{")
            end = cleaned.rfind("}")

            if (
                start != -1
                and end != -1
                and end > start
            ):

                json_text = cleaned[
                    start:end + 1
                ]

                try:
                    return json.loads(
                        json_text
                    )

                except json.JSONDecodeError:
                    pass

            raise ValueError(
                "Failed to parse Gemini JSON response"
            ) from None


gemini_service = GeminiService()