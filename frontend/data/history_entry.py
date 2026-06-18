from dataclasses import dataclass


@dataclass
class HistoryItem:
    entryText: str
    is_character: bool = True
