from dataclasses import dataclass
import queue
from Configs.screen_config import Color, ScoreNavigatorStatus
from Models.DataModels.ApplicationState import ApplicationState
from Models.GrandStaff import GrandStaff
from Models.Menu.MenuItem import MenuItem
from Models.Menu.StraightLine import StraightLine
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
        self.current_line:StraightLine = None
        self.current_staff = None
        self.current_staff_index:int = 0
        self.state = ScoreNavigatorStatus.INVACTIVE
        self.app_state = app_state
        self.sound_player = app_state.sound_player
        self.menu_item:MenuItem = None
        self.notes_to_play = []
        
    def activate(self, music_score, menu_item:MenuItem):       
       self.music_score = music_score       
       self.current_staff = self.music_score.staves_sequence[self.current_staff_index];
       self.start_position, self.end_position = self.current_staff.get_initial_navigator_line()
       self.current_line = StraightLine(self.start_position, self.end_position, thickness=2)
       self.state = ScoreNavigatorStatus.RUNNING 
       self.menu_item = menu_item
       self.notes_to_play =  music_score.get_all_notes_in_positional_order()    
       self.sound_player.start_processing_queue() 

    def cancel(self, menu_item:MenuItem):   
       self.start_position, self.end_position = None, None
       self.current_line = None
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
        #check that we haven't reached current staff note_right_offset
        if self.current_line.start_position.x >= self.current_staff.get_notes_offsets()[1]:
            # if there is no staff after this one
            if (self.current_staff_index + 1) >= len(self.music_score.staves_sequence):
                #otherwise stop: cancel navigation
                self.cancel(self.menu_item)
                return False
            else:
                self.current_staff_index += 1
                self.current_staff = self.music_score.staves_sequence[self.current_staff_index]
                self.start_position, self.end_position = self.current_staff.get_initial_navigator_line()
                self.current_line = StraightLine(self.start_position, self.end_position, thickness=2)
        
        self.current_line.translateTo(1,0)
        self.play_score_at_position(self.current_line.start_position)

    def stop(self, menu_item:MenuItem):
        self.state = ScoreNavigatorStatus.PAUSE
        menu_item.deactivate_item()
   
    def play_score_at_position(self, position:Position):
        for note in self.notes_to_play:
            if note.position.x == position.x:
                print(f"Playing note at position:{note.position} - key id:{note.key_id}")
                note_key_code = StaffUtils.get_key_code_from_keyid(note.key_id)
                #self.sound_player.play_note(note_key_code, note.duration[4])
                self.sound_player.add_note_to_queue(note_key_code, note.duration[4])

    def is_live(self):
        return self.is_paused() or self.is_running()
    
   
   
   
   