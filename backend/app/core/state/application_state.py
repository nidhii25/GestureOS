from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApplicationState:
    is_running: bool = True
    version: str = "1.0.0"
    started_at: datetime = datetime.now()