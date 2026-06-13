from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal

AppMode = Literal['player', 'master']

class SourceDocument(BaseModel):
    content: str
    metadata: Dict[str, str] = Field(default_factory=dict)

class ChatResponse(BaseModel):
    answer: str = Field(description="Wygenerowana odpowiedź asystenta w Markdown.")
    sources: List[SourceDocument] = Field(description="Lista dokumentów użytych do wygenerowania odpowiedzi.")
    is_guardrail_triggered: bool = Field(default=False, description="Flaga informująca, czy zapytanie otarło się o blokadę bezpieczeństwa.")


class EntityStats(BaseModel):
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int

class CharacterSheet(BaseModel):
    name: str = Field(description="Imię postaci.")
    role_or_class: str = Field(description="Klasa (np. Paladyn) lub rola (np. Karczmarz).")
    race: str = Field(description="Rasa postaci.")
    stats: EntityStats = Field(description="Sześć głównych statystyk D&D.")
    background_story: str = Field(description="Krótka historia (lore) postaci powiązana ze światem.")
    equipment: List[str] = Field(default_factory=list, description="Lista ekwipunku.")
    special_traits: Optional[List[str]] = Field(default=None, description="Specjalne umiejętności lub sekrety (szczególnie dla NPC).")