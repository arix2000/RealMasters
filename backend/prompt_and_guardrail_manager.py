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
                input_variables=["context", "chat_history", "query"],
                template="""You are a helpful Player Assistant in a Dungeons and Dragons. Your task is to explain mechanics and remind the player about world lore.
                            Maintain a friendly, supportive, and immersive tone. 
                            Base your answers EXCLUSIVELY on the following context provided from the campaign notes. Do not make up rules outside of this context.
                            
                            <context>
                            {context}
                            </context>
                            
                            <chat_history>
                            {chat_history}
                            </chat_history>
                            
                            Continue the conversation naturally. Do NOT greet or introduce yourself again if there is prior chat history above.
                            
                            Player's query: {query}
                            Answer:"""
            ),
            'master': PromptTemplate(
                input_variables=["context", "chat_history", "query"],
                template="""You are an omniscient Game Master Advisor for Dungeons and Dragons. Your task is to help the GM run the session, create challenges, and recall hidden plotlines.
                            Use a professional, creative, and strategic tone.
                            Base your advice on the Game Master's secret notes below:
                            
                            <context>
                            {context}
                            </context>
                            
                            <chat_history>
                            {chat_history}
                            </chat_history>
                            
                            Continue the conversation naturally. Do NOT greet or introduce yourself again if there is prior chat history above.
                            
                            Game Master's query: {query}
                            Answer:"""
            )
        }

        self.entity_templates = {
            'player': PromptTemplate(
                input_variables=["requirements", "instruction"],
                template="""As an expert in RPG mechanics, {instruction} a playable character (PC) for a Player based on the following guidelines:
                            {requirements}
                            
                            IMPORTANT REQUIREMENTS:
                            - The "background_story" field MUST be a rich, detailed narrative of AT LEAST 3 full paragraphs (minimum 200 words). Include the character's origin, formative life events, key relationships, motivations, fears, and how they came to be an adventurer. Make the story vivid, emotional, and deeply tied to a fantasy world.
                            - Each "special_traits" entry MUST follow the format "Trait Name: detailed description" where the description is at least 2 sentences long explaining the mechanical and narrative implications of the trait.
                            - Provide at least 5 items in "equipment", each with a short flavor description (e.g. "Miecz Płomieni - wykuty w ogniu starożytnej kuźni, lśni czerwonym blaskiem").
                            - Ensure the core stats are balanced and make sense for the chosen class and race."""
            ),
            'master': PromptTemplate(
                input_variables=["requirements", "instruction"],
                template="""As a Game Master Advisor, {instruction} a Non-Player Character (NPC) for the campaign based on the following guidelines:
                            {requirements}
                            
                            IMPORTANT REQUIREMENTS:
                            - The "background_story" field MUST be a rich, detailed narrative of AT LEAST 3 full paragraphs (minimum 200 words). Include the NPC's origin, hidden agenda, past betrayals or alliances, their role in the world, and secrets the players may uncover. Make the story layered and full of plot hooks.
                            - Each "special_traits" entry MUST follow the format "Trait Name: detailed description" where the description is at least 2 sentences long explaining both the narrative role and any mechanical effects.
                            - Provide at least 5 items in "equipment", each with a short flavor description hinting at the NPC's personality or history.
                            - Focus on interesting motivations, dark secrets, and plot hooks. Treat the mechanical stats as a secondary element to support the narrative."""
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

    def build_chat_prompt(self, query: str, context: str, mode: AppMode, chat_history: str = "") -> str:
        template = self.chat_templates.get(mode)
        if not template:
            raise PromptFormattingError(template_name=f"Chat_{mode}", missing_variable="TEMPLATE_NOT_FOUND")
        try:
            return template.format(context=context, query=query, chat_history=chat_history)
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