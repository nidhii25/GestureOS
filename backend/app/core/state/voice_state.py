from dataclasses import dataclass


@dataclass
class VoiceState:
    is_active: bool = False
    language: str = "en"