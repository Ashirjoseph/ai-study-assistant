from __future__ import annotations

import json
from dataclasses import dataclass

from openai import OpenAI, OpenAIError

from app.config import settings

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        kwargs: dict = {"api_key": settings.LLM_API_KEY}
        if settings.LLM_BASE_URL:
            kwargs["base_url"] = settings.LLM_BASE_URL
        _client = OpenAI(**kwargs)
    return _client


@dataclass
class LLMResult:
    text: str
    tokens_used: int | None


def _call_llm(system_prompt: str, user_prompt: str, max_tokens: int) -> LLMResult:
    """Single chat-completion call. No history sent — each feature is stateless."""
    client = _get_client()
    try:
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except OpenAIError as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    text = response.choices[0].message.content or ""
    tokens_used = response.usage.total_tokens if response.usage else None
    return LLMResult(text=text.strip(), tokens_used=tokens_used)


ASK_SYSTEM_PROMPT = (
    "You are a concise study assistant. Explain the concept clearly and simply "
    "in under 150 words. No preamble."
)


def ask_question(question: str) -> LLMResult:
    return _call_llm(ASK_SYSTEM_PROMPT, question, max_tokens=settings.LLM_MAX_TOKENS)


SUMMARY_SYSTEM_PROMPT = (
    "Summarize the given study material in 3-5 concise bullet points. "
    "Return plain text only, one bullet per line starting with '- '. No preamble."
)

MCQ_SYSTEM_PROMPT = (
    "Generate multiple-choice questions from the study material. "
    'Return ONLY valid JSON of the form '
    '{"mcqs": [{"question": str, "options": [str, str, str, str], "answer_index": int}]}. '
    "answer_index is the 0-based index of the correct option. No extra text."
)

FLASHCARD_SYSTEM_PROMPT = (
    "Generate flashcards from the study material. "
    'Return ONLY valid JSON of the form '
    '{"flashcards": [{"front": str, "back": str}]}. No extra text.'
)


def _call_llm_json(system_prompt: str, user_prompt: str, max_tokens: int) -> tuple[dict, int | None]:
    """Single call using JSON response mode — avoids fragile text parsing."""
    client = _get_client()
    try:
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except OpenAIError as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    raw = response.choices[0].message.content or "{}"
    tokens_used = response.usage.total_tokens if response.usage else None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"LLM returned invalid JSON: {exc}") from exc
    return data, tokens_used


def generate_summary(text: str) -> LLMResult:
    return _call_llm(SUMMARY_SYSTEM_PROMPT, text, max_tokens=settings.LLM_MAX_TOKENS)


def generate_mcqs(text: str, num_questions: int) -> tuple[list[dict], int | None]:
    prompt = f"Number of questions: {num_questions}\n\nMaterial:\n{text}"
    data, tokens_used = _call_llm_json(MCQ_SYSTEM_PROMPT, prompt, max_tokens=settings.LLM_MAX_TOKENS)
    return data.get("mcqs", []), tokens_used


def generate_flashcards(text: str, num_cards: int) -> tuple[list[dict], int | None]:
    prompt = f"Number of flashcards: {num_cards}\n\nMaterial:\n{text}"
    data, tokens_used = _call_llm_json(FLASHCARD_SYSTEM_PROMPT, prompt, max_tokens=settings.LLM_MAX_TOKENS)
    return data.get("flashcards", []), tokens_used
