from dataclasses import dataclass
from enum import Enum, auto

class TrackingStatus(Enum):

    NOT_STARTED = auto()
    IDLE = auto()
    ACTIVE = auto()


@dataclass
class TrackingState:

    status: TrackingStatus = TrackingStatus.NOT_STARTED

    def start(self) -> None:
        self.status = TrackingStatus.ACTIVE

    def idle(self) -> None:
        self.status = TrackingStatus.IDLE

    def reset(self) -> None:
        self.status = TrackingStatus.NOT_STARTED