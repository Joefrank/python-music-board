import mido
import time
from Configs.music_config import NoteDurationInTicks
from Models.GrandStaff import GrandStaff
from Models.MusicScore import MusicScore
from Models.Staff import Staff

class SoundPlayer:
    keys_played = []
    BPM = 120
    TICKS_PER_BEAT = 480
    SECONDS_PER_BEAT = 60 / BPM
    SECONDS_PER_TICK = SECONDS_PER_BEAT / TICKS_PER_BEAT
    
    def __init__(self):
        self.outport = mido.open_output()

    def play_key(self, key_code):
        self.keys_played.append(key_code)
        self.outport.send(mido.Message('note_on', note=key_code, velocity=127))
        time.sleep(0.2)
    
    """
        Playing note with specific duration is done with note_on and note_off then 
        putting the delay in between the two.
        note_key_code: is the number representing the note between 21 and 109 - 88 key on piano
        duration_ticks: is the duration of the note
        velocity: Controls loudness / brightness (0 - 127)
    """
    def play_note(self, note_key_code, duration_ticks, velocity=64):
        self.outport.send(mido.Message('note_on', note=note_key_code, velocity=velocity))
        time.sleep(duration_ticks * self.SECONDS_PER_TICK)
        self.outport.send(mido.Message('note_off', note=note_key_code, velocity=velocity))

    """
        Plays piano note with a delay to match timing/duration
    """
    def play_piano_note(self, note=60, duration=NoteDurationInTicks.QUARTER, velocity=64, channel=0):
        # Note ON
        note_on = mido.Message('note_on', note=note, velocity=velocity, channel=channel)
        self.outport.send(note_on)

        print(f"duration:{duration} - ticks:{self.SECONDS_PER_TICK}")
        # Wait for note duration
        time.sleep(duration * self.SECONDS_PER_TICK)

        # Note OFF
        note_off = mido.Message('note_off', note=note, velocity=0, channel=channel)
        self.outport.send(note_off)
        
    def play_note_crescendo(self, note_key_code, duration_ticks, cresendo_steps):
        for v in range(len(cresendo_steps)):  # 40, 60, 80, 100
            self.play_note(note_key_code, duration_ticks, velocity=v)

        
    