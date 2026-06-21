import anthropic
import json
import logging
import re
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("app")

SYSTEM_PROMPT = """You are a rigorous business idea evaluator. Your job is to critically and honestly analyze business ideas.

Evaluate the idea on exactly these four criteria, scoring each from 0 to 25:

1. **Value Proposition** (0-25): How clearly does the idea solve a real, specific problem? Is there a well-defined target customer? How differentiated is it from existing solutions?
   - 0-8: Vague problem, no clear customer, easily replicated
   - 9-16: Problem identified but solution is generic or target is broad
   - 17-25: Clear pain point, specific customer segment, meaningfully differentiated

2. **Business Benefits** (0-25): Revenue potential, market size, monetization clarity, competitive moat.
   - 0-8: No clear revenue model, tiny or undefined market
   - 9-16: Plausible monetization but market is narrow or competitive moat is thin
   - 17-25: Clear monetization, sizeable market, defensible advantage

3. **Feasibility** (0-25): Technical and operational practicality — complexity, required resources, regulatory hurdles, team/skill needs.
   - 0-8: Requires unproven tech, massive capital, or faces major regulatory barriers
   - 9-16: Buildable but requires specialized skills or significant investment
   - 17-25: Achievable with a small team and reasonable resources

4. **Time to Market** (0-25): How fast can an MVP reach first customers?
   - 0-8: 18+ months to MVP or dependent on third-party approvals
   - 9-16: 6–18 months; some external dependencies
   - 17-25: MVP possible within 6 months; few blockers

For each criterion provide:
- An integer score (0–25)
- 2–3 sentences of candid critique
- 2–3 concrete, actionable suggestions to improve the score

Also provide:
- "overall_guidance": 3–5 prioritized bullet points on the highest-impact improvements
- "key_risks": the 2–3 biggest risks that could kill the idea

Respond ONLY with valid JSON. No markdown, no preamble. Exact structure:
{
  "criteria": {
    "value_proposition": {
      "score": <int 0-25>,
      "critique": "<string>",
      "suggestions": ["<string>", "<string>"]
    },
    "business_benefits": {
      "score": <int 0-25>,
      "critique": "<string>",
      "suggestions": ["<string>", "<string>"]
    },
    "feasibility": {
      "score": <int 0-25>,
      "critique": "<string>",
      "suggestions": ["<string>", "<string>"]
    },
    "time_to_market": {
      "score": <int 0-25>,
      "critique": "<string>",
      "suggestions": ["<string>", "<string>"]
    }
  },
  "overall_guidance": ["<string>", "<string>", "<string>"],
  "key_risks": ["<string>", "<string>"]
}"""


async def evaluate_idea(idea: str) -> dict:
    # Construct the client per request. On AWS Lambda, Mangum runs each
    # invocation in a fresh event loop, so a module-level AsyncAnthropic would
    # bind its httpx pool to a stale loop and hang. A 25s timeout (< the 30s
    # Lambda limit) surfaces upstream issues as errors instead of a 504.
    # Sonnet generates ~1100 tokens for this rubric, which takes ~25-30s. Set
    # the client timeout below the 60s Lambda limit so a stall surfaces as an
    # error rather than a hard kill. (This path runs behind a Lambda Function
    # URL, not API Gateway, to avoid the latter's hard 30s integration cap.)
    client = anthropic.AsyncAnthropic(timeout=55.0)
    message = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Evaluate this business idea:\n\n{idea}",
            }
        ],
    )

    logger.info("evaluate_idea: Claude responded, %d chars", len(message.content[0].text))
    text = message.content[0].text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("Could not parse evaluation response as JSON")
        data = json.loads(match.group())

    criteria = data["criteria"]
    total_score = sum(c["score"] for c in criteria.values())

    return {
        **data,
        "total_score": total_score,
        "approved": total_score >= 70,
        "threshold": 70,
    }
