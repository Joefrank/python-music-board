
"""Main entry point for the AI Music Board application."""

import sys
import logging

from Services.Builders import StaffBuilder
from Models.Line import Line
from Configs.screen_config import VERTICAL_POSITION_TOP

def main():
    """Main entry point."""
    #app = StaffBuilder(clef, time_signature, key_signature, staff_offset, staff_top_left, staff_width)  
    print(f'services test{VERTICAL_POSITION_TOP}')
    pass

if __name__ == "__main__":
    main()