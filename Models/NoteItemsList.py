from typing import List, Optional
from Models import Interval
from Models.Line import Line

class NoteItemsList:   
    def __init__(self, line_notes, interval_notes):
        self.line_notes: Optional[List[Line]] = line_notes 
        self.interval_notes: Optional[List[Interval]] = interval_notes 
   