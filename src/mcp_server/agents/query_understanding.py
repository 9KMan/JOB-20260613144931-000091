"""Query Understanding Agent — parses natural-language input into structured query plans."""
from __future__ import annotations

import json
from typing import Any


async def understand_query(question: str) -> dict[str, Any]:
    """Parse a natural-language question into a structured query plan.

    This is a rule-based parser for the PoC. In production, this would call
    an LLM (Claude/GPT) to classify intent and extract entities.

    Returns a dict with:
      - intent: lookup | aggregation | comparison | summary | search_similar
      - entities: extracted field names, table names, date ranges
      - filters: extracted WHERE conditions
      - output_format: concise | detailed | table | json
    """
    question_lower = question.lower()

    # Intent classification
    if any(kw in question_lower for kw in ["how many", "count", "total", "sum"]):
        intent = "aggregation"
    elif any(kw in question_lower for kw in ["similar", "like", "related to"]):
        intent = "search_similar"
    elif any(kw in question_lower for kw in ["list", "show me", "what are"]):
        intent = "lookup"
    elif any(kw in question_lower for kw in ["compare", "difference between"]):
        intent = "comparison"
    else:
        intent = "lookup"

    # Output format
    if "table" in question_lower or "breakdown" in question_lower:
        output_format = "table"
    elif "json" in question_lower:
        output_format = "json"
    elif "summary" in question_lower or "brief" in question_lower:
        output_format = "concise"
    else:
        output_format = "detailed"

    # Extract collection name (first capitalized word that isn't a question word)
    stop_words = {"what", "which", "how", "when", "where", "who", "show", "list", "the", "a", "an"}
    words = question.split()
    collection = "dataset"  # default
    for word in words:
        cleaned = word.strip(",?.:").lower().capitalize()
        if cleaned.lower() not in stop_words and len(cleaned) > 2:
            collection = cleaned.lower()
            break

    return {
        "intent": intent,
        "collection": collection,
        "question": question,
        "output_format": output_format,
        "filters": {},
        "date_range": None,
    }
