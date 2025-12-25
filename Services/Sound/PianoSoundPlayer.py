import queue
import threading
import mido
import time
from Configs.constants import SoundPlayerEventConstants
from Configs.music_config import NoteDurationInTicks
from Models.Chord import Chord
from Models.GrandStaff import GrandStaff
from Models.MusicScore import MusicScore
from Models.Staff import Staff
from Services.Utils.MusicUtils import MusicUtils

class SoundPlayer:
    keys_played = []
    
    def __init__(self):
        self.outport = mido.open_output()
        self.note_queue = queue.Queue()
        self.chord_queue = queue.Queue()
        self.play_lock = threading.Lock()
        self.feedback_queue = queue.Queue()

        self.midi_thread = threading.Thread(
            target=self.midi_worker,
            daemon=True
        )
        self.midi_thread.start()

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
    def play_note(self, note_key_code, duration_ticks, velocity=60, tempo=80):
        try:
            self.outport.send(mido.Message('note_on', note=note_key_code, velocity=velocity))
            duration = MusicUtils.get_note_duration(duration_ticks, tempo)
            time.sleep(duration)
            self.outport.send(mido.Message('note_off', note=note_key_code, velocity=velocity))
        except IOError:
            print("Could not open MIDI output. Available ports:")
            print(mido.get_output_names())

    """
        Plays piano note with a delay to match timing/duration
    """
    def play_piano_note(self, velocity, tempo, note=60, duration_in_ticks=NoteDurationInTicks.QUARTER, channel=0):
        # Note ON
        note_on = mido.Message('note_on', note=note, velocity=velocity, channel=channel)
        self.outport.send(note_on)
        
        # Wait for note duration
        duration_in_seconds = MusicUtils.get_note_duration(duration_in_ticks, tempo)
        time.sleep(duration_in_seconds)

        # Note OFF
        note_off = mido.Message('note_off', note=note, velocity=0, channel=channel)
        self.outport.send(note_off)
        
    def play_note_crescendo(self, note_key_code, duration_ticks, cresendo_steps, tempo):
        for velocity in range(len(cresendo_steps)):  # [40, 60, 80, 100]
            self.play_note(note_key_code, duration_ticks, velocity, tempo)

    def midi_worker(self, port_name='Microsoft GS Wavetable Synth'):
         try:              
              while True:
                chord = self.chord_queue.get()  # blocks until a chord is available   
                with self.play_lock:  
                    self.feedback_queue.put((SoundPlayerEventConstants.CHORD_START, chord))           
                    self.play_chord(chord)  
                    self.feedback_queue.put((SoundPlayerEventConstants.CHORD_END, chord))                 
                self.chord_queue.task_done()             

         except IOError:
             print("Could not play chord:")
             print(mido.get_output_names())
             return
         finally: # clean up
            if self.outport:
                # Safety: turn off any stuck notes
                for note in range(128):
                    self.outport.send(mido.Message('note_off', note=note, velocity=0))

                self.outport.close()

    def play_chord(self, chord: Chord):
        note_details = chord.get_playable_notes()
        #print("------------------------------------starting --------------------")
        for note in note_details:                
            duration = 1 #MusicUtils.get_note_duration(note[1], note[3])
            print(f"Playing chord note: {note[0]} - Duration (s): {duration}")          
            # Play note
            self.outport.send(mido.Message('note_on', note=note[0], velocity=note[2]))            
        
        time.sleep(duration)

        #print("------------------------------------TErminating --------------------")
        for note in note_details:
            self.outport.send(mido.Message('note_off', note=note[0]))

    def start_processing_queue(self):
        print("------------------------------------ processing queue --------------------")
        # Start MIDI thread
        #threading.Thread(target=self.midi_worker, daemon=True).start()

    def add_note_to_queue(self, note, length):
        self.note_queue.put((note, length))

    def add_chord_to_queue(self, chord: Chord):       
        self.chord_queue.put(chord)

   