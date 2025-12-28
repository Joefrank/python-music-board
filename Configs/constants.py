
from dataclasses import dataclass


@dataclass
class SoundPlayerEventConstants:
    CHORD_START: str = "chord_start"
    CHORD_END: str = "chord_end"
    PENDING_CHORD_END: str = "pending_chord_end"
    BATCH_END: str = "batch_end"