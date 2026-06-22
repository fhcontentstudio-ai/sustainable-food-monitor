import json
from anthropic import Anthropic


MODEL = "claude-sonnet-4-6"

SEARCH_QUERIES = {
    "market_demand": "plant-based food retail sales data 2026",
    "investment": "alternative protein venture capital funding 2026",
    "policy_regulation": "state alternative protein labeling law 2026",
    "consumer_adoption": "plant-based food consumer survey 2026",
    "corporate_strategy": "plant-based company earnings strategy 2026",
    "macroeconomic_context": "USDA food price outlook 2026",
}


def find_candidates(missing_category: str) -> list[dict]:
    """Use Claude with web search to propose real candidate sources for a missing category."""

    client = Anthropic()
    query = SEARCH_QUERIES.get(missing_category, missing_category)

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            temperature=0,
            tools=[{"type": "web_search_20250305", "name": "web_search"}],
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Search for: {query}\n\n"
                        f"Find 3-5 credible, real articles or reports relevant to "
                        f"'{missing_category}' in the plant-based/alternative protein sector. "
                        f"Prioritize government data, trade press, and market reports over blogs. "
                        f"For each, return: title, url, and a 1-2 sentence description of what it covers. "
                        f"Return as a JSON list: "
                        f'[{{"title": "...", "url": "...", "description": "..."}}]'
                    ),
                }
            ],
        )
    except Exception as e:
        print(f"  [API ERROR] Exception calling Anthropic API: {type(e).__name__}: {e}")
        return []

    print(f"  [DEBUG] stop_reason: {response.stop_reason}")
    print(f"  [DEBUG] content block types: {[b.type for b in response.content]}")

    for i, block in enumerate(response.content):
        print(f"  [DEBUG] block[{i}] type={block.type}")
        if block.type == "text":
            print(f"  [DEBUG] block[{i}] text (first 500 chars): {block.text[:500]!r}")
        elif block.type == "tool_use":
            print(f"  [DEBUG] block[{i}] tool_use name={block.name} input={str(block.input)[:300]!r}")
        elif block.type == "tool_result":
            print(f"  [DEBUG] block[{i}] tool_result content={str(block.content)[:300]!r}")
        else:
            print(f"  [DEBUG] block[{i}] raw={str(block)[:300]!r}")

    text_blocks = [b.text for b in response.content if b.type == "text"]
    if not text_blocks:
        print("  [DEBUG] No text blocks found in response. Cannot parse candidates.")
        return []

    raw = "\n".join(text_blocks)
    print(f"  [DEBUG] Joined text for JSON parse (first 800 chars): {raw[:800]!r}")

    try:
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start == -1 or end == 0:
            print("  [DEBUG] No JSON list brackets found in joined text.")
            return []
        return json.loads(raw[start:end])
    except (json.JSONDecodeError, ValueError) as e:
        print(f"  [DEBUG] JSON parse error: {e}")
        print(f"  [DEBUG] Attempted to parse: {raw[start:end][:400]!r}")
        return []
