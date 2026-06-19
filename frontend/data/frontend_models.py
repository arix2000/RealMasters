from dataclasses import dataclass
from typing import Literal

OutputType = Literal['asking_question', 'character_creation']


@dataclass
class HistoryItem:
    session_id: str
    entryText: str
    is_character: bool = True
