import re

from langchain_core.prompts import PromptTemplate
from backend.models import AppMode
from backend.exceptions import GuardrailViolationError, PromptFormattingError


class PromptAndGuardrailManager:

    def __init__(self):
        self.MAX_QUERY_LENGTH = 1000
        self.forbidden_patterns = [
            re.compile(r"ignore\s*(all|previous)*\s*instructions", re.IGNORECASE),
            re.compile(r"zignoruj\s*(poprzednie)*\s*instrukcje", re.IGNORECASE),
            re.compile(r"jail[\s-]*break", re.IGNORECASE),
            re.compile(r"write\s*(a\s*)?code", re.IGNORECASE),
            re.compile(r"napisz\s*kod", re.IGNORECASE),
            re.compile(r"system prompt", re.IGNORECASE),
        ]

        self.chat_templates = {
            'player': PromptTemplate(
                input_variables=["context", "query"],
                template="""You are a helpful Player Assistant in a Dungeons and Dragons. Your task is to explain mechanics and remind the player about world lore.
                            Maintain a friendly, supportive, and immersive tone. 
                            Base your answers EXCLUSIVELY on the following context provided from the campaign notes. Do not make up rules outside of this context.
                            
                            <context>
                            {context}
                            </context>
                            
                            Player's query: {query}
                            Answer:"""
            ),
            'master': PromptTemplate(
                input_variables=["context", "query"],
                template="""You are an omniscient Game Master Advisor for Dungeons and Dragons. Your task is to help the GM run the session, create challenges, and recall hidden plotlines.
                            Use a professional, creative, and strategic tone.
                            Base your advice on the Game Master's secret notes below:
                            
                            <context>
                            {context}
                            </context>
                            
                            Game Master's query: {query}
                            Answer:"""
            )
        }

        self.entity_templates = {
            'player': PromptTemplate(
                input_variables=["requirements", "instruction"],
                template="""As an expert in RPG mechanics, {instruction} a playable character (PC) for a Player based on the following guidelines:
                            {requirements}
                            
                            Ensure the core stats are balanced, provide a coherent background story, and make sure the character is ready for an adventure."""
            ),
            'master': PromptTemplate(
                input_variables=["requirements", "instruction"],
                template="""As a Game Master Advisor, {instruction} a Non-Player Character (NPC) for the campaign based on the following guidelines:
                            {requirements}
                            
                            Focus on interesting motivations, dark secrets, and plot hooks. Treat the mechanical stats as a secondary element to support the narrative."""
            )
        }

    def check_guardrails(self, query: str) -> None:
        if len(query) > self.MAX_QUERY_LENGTH:
            raise GuardrailViolationError(
                attempt_type="PayloadTooLarge",
                blocked_query=query[:50] + "..."
            )

        for pattern in self.forbidden_patterns:
            if pattern.search(query):
                raise GuardrailViolationError(
                    attempt_type="RegexBlacklistMatch",
                    blocked_query=query
                )

        if not query.strip():
            raise GuardrailViolationError(
                attempt_type="EmptyQuery",
                blocked_query="[EMPTY]"
            )

    def build_chat_prompt(self, query: str, context: str, mode: AppMode) -> str:
        template = self.chat_templates.get(mode)
        if not template:
            raise PromptFormattingError(template_name=f"Chat_{mode}", missing_variable="TEMPLATE_NOT_FOUND")
        try:
            return template.format(context=context, query=query)
        except KeyError as e:
            raise PromptFormattingError(template_name=f"Chat_{mode}", missing_variable=str(e))

    def build_entity_prompt(self, requirements: str, mode: AppMode, is_modification: bool = False) -> str:
        template = self.entity_templates.get(mode)
        if not template:
            raise PromptFormattingError(template_name=f"Entity_{mode}", missing_variable="TEMPLATE_NOT_FOUND")

        instruction = "modify" if is_modification else "generate a new"

        try:
            return template.format(requirements=requirements, instruction=instruction)
        except KeyError as e:
            raise PromptFormattingError(template_name=f"Entity_{mode}", missing_variable=str(e))