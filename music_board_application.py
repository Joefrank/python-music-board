import logging
import pygame

from Configs import screen_config
from Configs.music_config import BASS_CLEF, TREBLE_CLEF
from Models import MusicScore
from Models.DataModels.ApplicationState import ApplicationState
from Models.EventHandler import EventHandler
from Models.exceptions import MusicBoardApplicationError
from Services.Builders import MusicScoreBuilderDirector, StaffBuilderDirector
from Services.Renderer.StaffRenderer import StaffRenderer
from Services.Renderer.ScreenRenderer import ScreenRenderer
from Configs.screen_config import StaffConfig
from Services.Sound.PianoSoundPlayer import SoundPlayer

class MusicBoardApplication:

    def __init__(self):
        self.action_mode = None # Edit or Play(existing item)
        self.main_canvas = None
        self.state = ApplicationState()     
        self.staff_renderer = StaffRenderer(self.state)
        self.screen_renderer = ScreenRenderer(self.state)
        self.logger = logging.getLogger(__name__)        
        self.event_handler = EventHandler(self.state)
        self.staff_builder_director = StaffBuilderDirector()        
        self.score_builder_director = MusicScoreBuilderDirector.MusicScoreBuilderDirector()
        self.music_score = None

    def initialize(self) -> None:
        """ Initializes everything to do with music-board application """
       #try:
        default_time_signature, default_key_signature, score_title = "3x4", "Gb", "We Gather Together"
        score_credits = [
            ["Anonymous, 1625", "Tr. by Theodore Baker, 1917 (1851-1934)"],
            ["KREMSER Irregular", "Netherland Folk Song, 1625","Arr. by Edward Kremser (1838-1914)"]
        ]
        window_width, window_height = screen_config.WindowConfig.WIDTH, screen_config.WindowConfig.HEIGHT
        # init the main window
        self.main_canvas = self.screen_renderer.init_screen(window_width, window_height, screen_config.WindowConfig.CAPTION,
                                                    screen_config.WindowConfig.BACKGROUND_COLOR)
        # init the first staff
        grand_staff = self.init_staffs(window_width, default_time_signature, default_key_signature) 
        # use first staff to create music score
        self.music_score = self.score_builder_director.build_score(grand_staff, score_title, score_credits) 
       
        

    def run(self) -> None:
        """Run the main application loop."""
        try:
            self.logger.info("Starting main application loop")
            clock = pygame.time.Clock()

            while self.state.is_running:
                # Handle events
                self.event_handler.handle_events()

                # Process music logic
                #self.controller.process_note_placement()

                # Render frame
                self.screen_renderer.render_frame(self.main_canvas, self.music_score)

                # Small delay to prevent excessive CPU usage
                #pygame.time.wait(1)
                
                #clock.tick(3160)
                #pygame.display.flip()
                #self.staff_renderer.render_music_score(self.main_canvas, self.music_score)
                pygame.time.wait(200)

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

    """ We initialize the app with only one grand staff."""
    def init_staffs(self, window_width, time_signature, key_signature):        
        # record this for subsequent operations
        grand_staff = self.staff_builder_director.build_grand_staff(window_width, StaffConfig, (TREBLE_CLEF, BASS_CLEF), 
                                                                    time_signature, key_signature)
        return grand_staff
    
   
        
    
        
        