
from dataclasses import dataclass


@dataclass
class SoundPlayerEventConstants:
    CHORD_START: str = "chord_start"
    CHORD_END: str = "chord_end"