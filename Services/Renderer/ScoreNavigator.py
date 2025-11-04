from Configs.screen_config import Color
from Models.DataModels.ApplicationState import ApplicationState
from Models.GrandStaff import GrandStaff
from Models.Menu.StraightLine import StraightLine
from Models.MusicScore import MusicScore
from Models.Position import Position
from Models.Staff import Staff


class ScoreNavigator:

    def __init__(self):    
        self.start_position:Position = None
        self.end_position:Position = None
        self.active:bool = False
        self.music_score:MusicScore = None
        self.current_line:StraightLine = None

    def activate(self, music_score):
       self.music_score = music_score       
       self.start_position, self.end_position = self.music_score.staves_sequence[0].get_initial_navigator_line()
       self.current_line = StraightLine(self.start_position, self.end_position, thickness=2)
       self.active = True

    def is_active(self):
        return self.active

    def deactivate(self):
        self.activate = False

    def move_next(self):
        self.current_line.translateTo(1,0)

    # def navigate_score(self, music_score, from_step:int = 0):
    #     print(f"Playing score from step:{from_step}")
    #     for staff in music_score.staves_sequence:
    #         if  isinstance(staff, GrandStaff):
    #             self.navigate_grand_staff_notes(staff)
    #         elif isinstance(staff, Staff):
    #             self.navigate_staff_notes(staff)                 

    # def navigate_grand_staff_notes(self, grand_staff):
    #     top_left = grand_staff.get_top_left()
    #     bottom_left = grand_staff.get_bottom_left()
    #     print(f"drawing line from {top_left} to {bottom_left}")
    #     self.state.staff_renderer.draw_line_from_point(top_left, bottom_left, color=Color.RED, thickness = 2)

    #def navigate_staff_notes(self, staff):
        #pass
   
   