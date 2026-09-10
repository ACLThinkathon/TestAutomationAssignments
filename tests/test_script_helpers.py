import re
import base64
import json
import logging
import os
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def get_llm():
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("LLM_1_ENDPOINT"),
        api_key=os.getenv("LLM_1_API_KEY"),
        api_version=os.getenv("LLM_1_API_VERSION"),
        deployment_name=os.getenv("LLM_1_DEPLOYMENT_NAME"),
        temperature=1
    )

def encode_image(file_bytes: bytes) -> str:
    return base64.b64encode(file_bytes).decode("utf-8")

def _run_genai_validation(page, instruction):
    try:
        SYSTEM_PROMPT = """
        You are an AI UI validation assistant.
        You will receive two inputs:
        1. A UI screenshot (image)
        2. A natural language validation statement
        Your task is to:
        1. Analyze the screenshot
        2. Identify UI elements
        3. Validate the statement
        4. Return structured result
        Output Format:
        1. ELEMENT IDENTIFIED
        2. VALIDATION CHECKED
        3. RESULT (Pass / Fail / Cannot Determine)
        4. REASONING
        """
        logger.info(f"[GenAI] Running validation: {instruction}")

        image_bytes = page.screenshot(full_page=True)
        base64_image = encode_image(image_bytes)

        user_prompt = f"""Validation Template: {instruction}

        IMPORTANT: Only analyze the UI screenshot and validate it against the provided validation template.

        Return STRICT JSON:
        {{
        "validation_summary": [
            {{
            "validation_template": "",
            "result": "Pass or Fail",
            "reasoning": ""
            }}
        ]
        }}

        DO NOT add extra fields.
        DO NOT wrap in markdown.
        DO NOT add explanations outside JSON.
        """

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=[
                {"type": "text", "text": user_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ])
        ]
        llm = get_llm()
        ai_response = llm.invoke(messages)
        if not ai_response or not ai_response.content:
            logger.info("[GenAI] Empty response")
            return []
        raw_content = ai_response.content.strip()
        cleaned = re.sub(r'^```json\s*', '', raw_content)
        cleaned = re.sub(r'^```\s*', '', cleaned)
        cleaned = re.sub(r'\s*```$', '', cleaned).strip()
        try:
            parsed_json = json.loads(cleaned)
            validation_summary = parsed_json.get('validation_summary', [])
            logger.info(f"[GenAI RESULT]: {validation_summary}")
            return validation_summary
        except json.JSONDecodeError as e:
            logger.info(f"[GenAI] JSON parse error: {e}")
            return []
        except Exception as e:
            logger.info(f"[GenAI ERROR]: {e}")
            return []
    except Exception as e:
        logger.info(f"[GenAI ERROR]: {e}")
        return []
