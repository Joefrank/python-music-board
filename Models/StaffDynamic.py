class StaffDynamic:
    start_step = None # StaffStep where dynamic starts
    end_step = None # StaffStep where dynamic ends
    dynamic_type = None

    def __init__(self, start_step, end_step, dynamic_type):
        self.start_step = start_step
        self.end_step = end_step
        self.dynamic_type = dynamic_type
        