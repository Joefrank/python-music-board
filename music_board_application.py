import logging
import pygame

from Configs import screen_config
from Configs.music_config import TREBLE_CLEF
from Models.DataModels.ApplicationState import ApplicationState
from Models.EventHandler import EventHandler
from Models.exceptions import MusicBoardApplicationError
from Services.Builders import StaffBuilderDirector
from Services.Renderer.StaffRenderer import StaffRenderer
from Services.Renderer.ScreenRenderer import ScreenRenderer
from Configs.screen_config import StaffConfig

class MusicBoardApplication:

    def __init__(self):
        self.action_mode = None # Edit or Play(existing item)
        self.main_canvas = None
        self.first_staff_position = None
        self.staff_renderer = StaffRenderer()
        self.screen_renderer = ScreenRenderer()
        self.logger = logging.getLogger(__name__)
        self.state = ApplicationState()
        self.event_handler = EventHandler(self.state)

    def initialize(self) -> None:
        """ Initializes everything to do with music-board application """
        try:
            default_time_signature, default_key_signature = "3x4", "Ab"
            window_width, window_height = screen_config.WindowConfig.WIDTH, screen_config.WindowConfig.HEIGHT
            # init the main window
            self.main_canvas = self.screen_renderer.init_screen(window_width, window_height, screen_config.WindowConfig.CAPTION,
                                                       screen_config.WindowConfig.BACKGROUND_COLOR)
            # init the first staff
            first_staff = self.init_staffs(window_width, default_time_signature, default_key_signature)
            self.staff_renderer.render_staff(first_staff, self.main_canvas)

        except Exception as e:
            self.logger.error(f"Failed to initialize application: {e}")

    def run(self) -> None:
        """Run the main application loop."""
        try:
            self.logger.info("Starting main application loop")

            while self.state.is_running:
                # Handle events
                self.event_handler.handle_events()

                # Process music logic
                #self.controller.process_note_placement()

                # Render frame
                #self.renderer.render_frame()

                # Small delay to prevent excessive CPU usage
                pygame.time.wait(1)
                pygame.display.flip()

        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
        except Exception as e:
            self.logger.error(f"Unexpected error in main loop: {e}")
            raise MusicBoardApplicationError(f"Main loop failed: {e}") from e
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up application resources."""
        try:
            self.logger.info("Cleaning up application resources")

            #if self.controller:
                #self.controller.cleanup()

            pygame.quit()
            self.logger.info("Application cleanup completed")

        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

    def init_staffs(self, window_width, time_signature, key_signature):
        staff_builder_director = StaffBuilderDirector()
        # work out first staff position and with
        staff_with, staff_original_position = StaffBuilderDirector.calculate_first_staff_position(window_width,
                                                                                      StaffConfig.STAFF_WIDTH_PERCENT,
                                                                                      StaffConfig.STAFF_ORIGINAL_Y_OFFSET)
        # record this for subsequent operations
        self.first_staff_position = staff_original_position

        # build the staff.
        current_staff = staff_builder_director.build_staff(TREBLE_CLEF, time_signature, key_signature,
                                                           staff_original_position,
                                                           StaffConfig.STAFF_ALLOWED_MARGIN, staff_with,
                                                           StaffConfig.STAFF_LINE_GAP,
                                                           StaffConfig.STAFF_LINE_THICKNESS,
                                                           StaffConfig.STAFF_SPACING,
                                                           StaffConfig.STAFF_NO_LINES,
                                                           StaffConfig.STAFF_NO_INTERVALS)

        return current_staff