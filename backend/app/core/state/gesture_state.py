from dataclasses import dataclass


@dataclass
class GestureState:
    current_gesture: str | None = None
    previous_gesture: str | None = None
    confidence: float = 0.0
    last_action: str | None = None