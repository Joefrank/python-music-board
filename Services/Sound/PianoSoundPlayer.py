import queue
import threading
import mido
import time
from Configs.music_config import NoteDurationInTicks
from Models.Chord import Chord
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
        self.note_queue = queue.Queue()
        self.chord_queue = queue.Queue()

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
        try:
            self.outport.send(mido.Message('note_on', note=note_key_code, velocity=velocity))
            time.sleep(duration_ticks * self.SECONDS_PER_TICK)
            self.outport.send(mido.Message('note_off', note=note_key_code, velocity=velocity))
        except IOError:
            print("Could not open MIDI output. Available ports:")
            print(mido.get_output_names())

    """
        Plays piano note with a delay to match timing/duration
    """
    def play_piano_note(self, note=60, duration=NoteDurationInTicks.QUARTER, velocity=64, channel=0):
        # Note ON
        note_on = mido.Message('note_on', note=note, velocity=velocity, channel=channel)
        self.outport.send(note_on)
        # Wait for note duration
        time.sleep(duration * self.SECONDS_PER_TICK)

        # Note OFF
        note_off = mido.Message('note_off', note=note, velocity=0, channel=channel)
        self.outport.send(note_off)
        
    def play_note_crescendo(self, note_key_code, duration_ticks, cresendo_steps):
        for v in range(len(cresendo_steps)):  # 40, 60, 80, 100
            self.play_note(note_key_code, duration_ticks, velocity=v)

    def midi_worker(self, port_name='Microsoft GS Wavetable Synth'):
        # try:
        #     outport = mido.open_output(port_name)
        # except IOError:
        #     print("Could not open MIDI output. Available ports:")
        #     print(mido.get_output_names())
        #     return

        while True:
            chord = self.chord_queue.get()   # blocks until a note is available
            self.play_chord(chord)                
            self.chord_queue.task_done()

    def play_chord(self, chord: Chord):
        note_details = chord.get_playable_notes()
        for note in note_details:                
            duration = note[1] * self.SECONDS_PER_TICK
            print(f"processing note: {note[0]} - duration:{duration}")
            # Play note
            self.outport.send(mido.Message('note_on', note=note[0], velocity=90))            
       
        time.sleep(duration)

        for note in note_details:
            self.outport.send(mido.Message('note_off', note=note[0]))

    def start_processing_queue(self):
        # Start MIDI thread
        threading.Thread(target=self.midi_worker, daemon=True).start()

    def add_note_to_queue(self, note, length):
        self.note_queue.put((note, length))

    def add_chord_to_queue(self, chord: Chord):       
        self.chord_queue.put(chord)

        
    