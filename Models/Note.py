from Models.Position import Position
from Configs.music_config import valid_note_durations, note_modifiers
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
                 self.stem_inverted = True

    def implement_binary_modifier(self, modifier, linked_note):
        if modifier not in note_modifiers:
            return
        match modifier:           
            case 'b' | 'B':
                 self.beam_with = linked_note          
            case 'c' | 'C':
                 self.connected_note = linked_note
            
    def is_near_position(self, position: Position) -> bool:
         return ((self.position.x - 40 <= position.x <= self.position.x + 40)
             and (self.position.y - 40 <= position.y <= self.position.y + 40))


    def __str__(self):
        return f"Note {self.key_id} - Position:{self.position} - Order: {self.order} - Extended:{self.extended}" + \
            f" Stackato:{self.staccato} - Duration: {self.duration}"