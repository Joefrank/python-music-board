from Configs.screen_config import StaffConfig
from Models.Position import Position
from Configs.music_config import NoteDurationInTicks, valid_note_durations, note_modifiers
from Services.Utils.StaffUtils import StaffUtils

class Note:

    """
        duration: how long is the note for
        position: position on the staff item
        order: order on the staff item
        extended: if note duration is extended
        key: the related music note/key name that is for this object
        key_id: the exact piano music key to be played for this note
        beam_width: if this note has another key it is connected with.
    """
    def __init__(self, staff_item, duration, position, order, extended, key, key_id, beam_with=None):
        self.staff_item = staff_item
        self.duration:tuple = duration # in beats
        self.position:Position = position # position to center rest around
        self.order:int = order
        self.extended:bool = extended
        self.staccato:bool = None
        self.key:str = key
        self.key_id:str = key_id
        self.key_value:int = StaffUtils.get_key_code_from_keyid(key_id)
        self.beam_with:Note = beam_with # this is when we link to another note
        self.connected_note:Note = None
        self.stem_inverted = False
        self.color = None

    """
        staff_item: line/interval containing this note
    """
    def set_parent(self, staff_item):
        self.staff_item = staff_item

    def implement_unary_modifier(self, modifier):
        modifier_keys = modifier[0]
        if not any(item in modifier_keys for item in note_modifiers):
            return

        modifier_key = modifier_keys[0]
        match modifier_key:
            case 's' | 'S':                 
                 self.staccato = True
            case 'x' | 'X':
                 self.extended = True            
            case 'd' | 'D':
                 self.staff_item.delete_note(self)           
            case 'i' | 'I':
                 self.stem_inverted = not self.stem_inverted

    def implement_binary_modifier(self, modifier, linked_note):
        if modifier not in note_modifiers:
            return
        match modifier:           
            case 'b' | 'B':
                 self.beam_with = linked_note          
            case 'c' | 'C':
                 self.connected_note = linked_note 

    def is_near_position(self, position: Position) -> bool:
         proximity_threshold = StaffConfig.NOTE_PROXIMITY_THRESHOLD // 2
         return ((self.position.x - proximity_threshold <= position.x <= self.position.x + proximity_threshold)
             and (self.position.y - proximity_threshold <= position.y <= self.position.y + proximity_threshold))

    def get_distance_to(self, position:Position):
        return (self.position.x - position.x)**2 + (self.position.y - position.y)**2
    
    def get_exact_duration(self):
        duration = self.duration[4] * 1.5 if self.extended else self.duration[4] 
        exact_duration = duration       
        rest_duration = 0

        if self.staccato: # staccato is 1/4 of one tick
            exact_duration = NoteDurationInTicks.QUARTER * 0.25
            rest_duration = (duration - exact_duration) if duration > NoteDurationInTicks.QUARTER else 0
              
        return exact_duration, rest_duration
    
    def __str__(self):
        return f"Note {self.key_id} - Position:{self.position} - Order: {self.order} - Extended:{self.extended}" + \
            f" Stackato:{self.staccato} - Duration: {self.duration}"