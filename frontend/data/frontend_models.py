from dataclasses import dataclass
from typing import Literal

OutputType = Literal['asking_question', 'character_creation']


@dataclass
class HistoryItem:
    entryText: str
    is_character: bool = True
