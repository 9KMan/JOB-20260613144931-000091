"""Response Synthesis Agent — generates natural-language answers from structured data."""
from __future__ import annotations

from typing import Any


async def synthesize_response(
    question: str,
    data: dict[str, Any],
    output_format: str = "detailed",
) -> str:
    """Generate a natural-language response from structured query results.

    In PoC, returns a formatted string. In production, this calls an LLM.
    """
    collection = data.get("collection", "dataset")
    records = data.get("records", [])
    total = data.get("total", len(records))

    if output_format == "json":
        import json
        return json.dumps({"question": question, "data": data}, indent=2)

    lines = [f"Based on the {collection} data:\n"]

    if records:
        lines.append(f"Found {total} record(s):\n")
        for rec in records[:10]:
            lines.append(f"  • {rec.get('name', 'N/A')} (id: {rec.get('id', 'N/A')})")
        if total > 10:
            lines.append(f"\n  ... and {total - 10} more records.")
    else:
        lines.append("No records found matching your query.")

    if data.get("note"):
        lines.append(f"\n⚠️ {data['note']}")

    return "\n".join(lines)
