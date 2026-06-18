from langchain_google_genai import ChatGoogleGenerativeAI
from backend.models import CharacterSheet
from backend.exceptions import UpstreamAPIError, StructuredParsingError


class LLMClient:

    def __init__(self, api_key: str, model_name: str = "gemini-3.1-flash-lite"):
        try:
            self.chat_llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.7,
                convert_system_message_to_human=True
            )

            self.entity_llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=0.3
            ).with_structured_output(CharacterSheet)

        except Exception as e:
            print(e)
            raise UpstreamAPIError(provider="Google", status_code=500)

    def generate_chat_response(self, prompt_text: str) -> str:
        try:
            response = self.chat_llm.invoke(prompt_text)
            content = response.content

            if isinstance(content, list):
                text_parts = []
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        text_parts.append(part.get("text", ""))
                    elif isinstance(part, str):
                        text_parts.append(part)
                return "".join(text_parts)

            return str(content)

        except Exception as e:
            print(e)
            raise UpstreamAPIError(provider="Google (Chat)", status_code=502)

    def generate_structured_entity(self, prompt_text: str) -> CharacterSheet:
        try:
            structured_response: CharacterSheet = self.entity_llm.invoke(prompt_text)
            return structured_response

        except Exception as e:
            raise StructuredParsingError(
                target_model="CharacterSheet",
                raw_output=str(e)
            )