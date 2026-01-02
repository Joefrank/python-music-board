from dataclasses import dataclass
import queue
from Configs.screen_config import Color, ScoreNavigatorStatus
from Models.DataModels.ApplicationState import ApplicationState
from Models.GrandStaff import GrandStaff
from Models.Menu.MenuItem import MenuItem
from Models.StraightLine import StraightLine
from Models.MusicScore import MusicScore
from Models.Position import Position
from Models.Staff import Staff
from Services.Sound.PianoSoundPlayer import SoundPlayer
from Services.Utils.StaffUtils import StaffUtils


class ScoreNavigator:

    def __init__(self, app_state:ApplicationState):    
        self.start_position:Position = None
        self.end_position:Position = None
        self.music_score:MusicScore = None
        self.current_staff = None
        self.current_staff_index:int = 0
        self.state = ScoreNavigatorStatus.INVACTIVE
        self.app_state = app_state
        self.sound_player = app_state.sound_player
        self.menu_item:MenuItem = None
        self.chords_to_play = []

    """Activate the score navigation. And goes through each staff in the score to play it."""  
    def activate(self, music_score, menu_item:MenuItem): 
       self.current_staff_index = 0      
       self.music_score = music_score 
       self.set_current_staff_for_navigation()
       self.state = ScoreNavigatorStatus.RUNNING 
       self.menu_item = menu_item       
       self.chords_to_play = self.current_staff.get_chords()
       self.play_score()  # Play chords at initial position 

    def set_current_staff_for_navigation(self):
        if self.current_staff_index < len(self.music_score.staves_sequence):            
            self.current_staff = self.music_score.staves_sequence[self.current_staff_index]
            self.current_staff_index += 1
    
    def cancel(self, menu_item:MenuItem):   
       self.start_position, self.end_position = None, None
       self.state = ScoreNavigatorStatus.INVACTIVE
       menu_item.deactivate_item()   
       self.app_state.raise_screen_update_event()       

    def is_paused(self):
        return self.state == ScoreNavigatorStatus.PAUSE

    def is_running(self):
        return self.state == ScoreNavigatorStatus.RUNNING
    
    def is_inactive(self):
        return self.state == ScoreNavigatorStatus.INVACTIVE

    def deactivate(self):
        self.state = ScoreNavigatorStatus.INVACTIVE

    def move_next(self) -> bool:      
        # if there is no staff after this one
        if (self.current_staff_index + 1) >= len(self.music_score.staves_sequence):
            # otherwise stop: cancel navigation
            self.cancel(self.menu_item)
            return False
        else:
            self.current_staff_index += 1
            self.current_staff = self.music_score.staves_sequence[self.current_staff_index]
          
        self.play_score()       
        

    def stop(self, menu_item:MenuItem):
        self.state = ScoreNavigatorStatus.PAUSE
        menu_item.deactivate_item()
   
    def play_score_at_position(self, position:Position):
        # notes to play should be for one staff at a time
        # notes should be put in chords if they share same x position
        for note in self.notes_to_play:
            if note.position.x == position.x:
                note_key_code = StaffUtils.get_key_code_from_keyid(note.key_id)
                self.sound_player.add_note_to_queue(note_key_code, note.duration[4])


    def play_score(self):
        if len(self.chords_to_play) == 0:
            return 
        self.sound_player.add_chords_to_queue(self.chords_to_play)
      
    def is_live(self):
        return self.is_paused() or self.is_running()
    
   
   
   
   