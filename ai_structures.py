import json
import re
from groq import Groq

client = Groq(api_key='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')

def get_presentation_structure(topic):
    prompt = f"""Create a presentation structure for: "{topic}"
Return ONLY a JSON object with this EXACT structure:
{{
  "title": "Main Presentation Title",
  "subtitle": "Brief subtitle or tagline",
  "topic": "main topic category",
  "slides": [
    {{
      "title": "Definition of [subject]",
      "definition": "Concise definition here",
      "characteristics": ["Characteristic 1", "Characteristic 2"],
      "type": "definition"
    }},
    {{
      "title": "Key Use Cases",
      "use_cases": [
        {{"title": "Use Case 1", "description": "Desc 1"}},
        {{"title": "Use Case 2", "description": "Desc 2"}}
      ],
      "type": "use_cases"
    }},
    {{
      "title": "Real-World Examples",
      "examples": [
        {{"title": "Example 1", "description": "Example description"}},
        {{"title": "Example 2", "description": "Example description"}}
      ],
      "type": "examples"
    }},
    {{
      "title": "Benefits & Challenges",
      "benefits": ["Benefit 1", "Benefit 2", "Benefit 3"],
      "challenges": ["Challenge 1", "Challenge 2", "Challenge 3"],
      "type": "benefits_challenges"
    }},
    {{
      "title": "Detailed Topic Slide",
      "description": "Comprehensive info here.",
      "points": ["Point 1", "Point 2", "Point 3"],
      "type": "content"
    }},
    {{
      "title": "Conclusion",
      "conclusion": "Main conclusion statement.",
      "takeaways": ["Key takeaway 1", "Key takeaway 2", "Key takeaway 3"],
      "type": "conclusion"
    }}
  ]
}}
Requirements:
- Use a mix of these slide types: definition, use_cases, examples, benefits_challenges, content, conclusion.
- Each slide type should have appropriate fields.
- No explanation, just JSON."""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000
    )
    response = completion.choices[0].message.content
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        return json.loads(json_str)
    return {
        "title": f"Introduction to {topic.title()}",
        "subtitle": "A comprehensive overview",
        "topic": topic,
        "slides": [
            {
                "title": f"Definition of {topic.title()}",
                "definition": f"{topic.title()} is an important subject.",
                "characteristics": [
                    "Characteristic 1",
                    "Characteristic 2"
                ],
                "type": "definition"
            },
        ]
}
