import json
import os
from app.models.model import QuestionDifficulty
from fastapi import HTTPException
from openai import OpenAI
from typing import List, Dict, Any
from app.core.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)
# client = OpenAI(
#     base_url="http://localhost:11434/v1",
#     api_key="ollama"  # 占位即可，不会校验
# )

def generate_question_with_ai(difficulty: QuestionDifficulty) -> Dict[str, Any]:
    system_prompt = """
        You are a professional coding challenge generator.

You will receive a difficulty level: easy, medium, or hard.

Rules:
- easy: basic syntax, simple control flow, basic data types
- medium: data structures, loops, functions, moderate logic
- hard: recursion, algorithms, optimization, edge cases

Output MUST be a valid JSON object and NOTHING else.

JSON schema (strict):
{
  "question_description": string,
  "question_content": string,
  "options": [
    {
      "option_index": number,
      "option_text": string
    }
  ],
  "correct_option_index": number,
  "explanation": string
}

Constraints:
- options MUST contain exactly 4 items
- option_index MUST be 0, 1, 2, 3
- correct_option_index MUST be one of the option_index values
- Only ONE option is correct
- Do NOT include markdown
- Do NOT include additional fields

    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            # model="deepseek-r1:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate a {difficulty.value} difficulty coding challenge."}
            ],
            response_format={
                "type": "json_object"
            },
            temperature=0.7
        )
        print(f"response: *******************{response}*******************")
        content = response.choices[0].message.content
        question_data = json.loads(content)
        required_fields = ["question_description",  "question_content", "options", "correct_option_index", "explanation"]
        for field in required_fields:
            if field not in question_data:
                raise HTTPException(status_code=500, detail=f"Missing required field: {field}")
        return question_data
    except Exception as e:
        print(f"Error generating question: {e}")
        return {
            "question_description": "Basic Python Question",
            "question_content": "What is the output of the following code?",
            "options": [
                {"option_text": "A", "option_index": 0}, 
                {"option_text": "B", "option_index": 1}, 
                {"option_text": "C", "option_index": 2}, 
                {"option_text": "D", "option_index": 3}
                ],
            "correct_option_index": 0,
            "explanation": "This is a basic Python question"
        }
