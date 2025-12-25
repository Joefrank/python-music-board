import logging
import pygame

from Configs import screen_config
from Configs.music_config import BASS_CLEF, TREBLE_CLEF, VelicityLevels
from Models import MusicScore
from Models.DataModels.ApplicationState import ApplicationState
from Models.EventHandler import EventHandler
from Models.Menu.MenuColorConfig import MenuColorConfig
from Models.Menu.MenuData import MenuData
from Models.Menu.MenuItem import MenuItem
from Models.Menu.MenuItemState import MenuItemState
from Models.Menu.MenuItemStateStep import MenuItemStateStep
from Models.Position import Position
from Models.exceptions import MusicBoardApplicationError
from Services.Builders import MenuBuilder, MusicScoreBuilderDirector, StaffBuilderDirector
from Services.Renderer.ScoreNavigator import ScoreNavigator
from Services.Renderer.StaffRenderer import StaffRenderer
from Services.Renderer.ScreenRenderer import ScreenRenderer
from Configs.screen_config import Color, StaffConfig
from Services.Sound.PianoSoundPlayer import SoundPlayer

class MusicBoardApplication:

    def __init__(self):
        self.action_mode = None # Edit or Play(existing item)
        self.main_canvas = None
        self.state = ApplicationState()     
        self.staff_renderer = StaffRenderer(self.state)
        self.screen_renderer = ScreenRenderer(self.state)
        self.state.set_renderers(self.staff_renderer,self.screen_renderer)
        self.logger = logging.getLogger(__name__)        
        self.event_handler = EventHandler(self.state)
        self.staff_builder_director = StaffBuilderDirector()        
        self.score_builder_director = MusicScoreBuilderDirector.MusicScoreBuilderDirector()
        self.music_score = None
        self.menu_builder = MenuBuilder.MenuBuilder()
        self.state.set_score_navigator(ScoreNavigator(self.state))

    def initialize(self) -> None:
        """ Initializes everything to do with music-board application """
       #try:
        default_time_signature, default_key_signature, score_title, tempo, velocity =\
              "3x4", "F", "Praise to the Lord", 90, VelicityLevels.MF
        score_credits = [
            ["Anonymous, 1625", "Tr. by Theodore Baker, 1917 (1851-1934)"],
            ["KREMSER Irregular", "Netherland Folk Song, 1625","Arr. by Edward Kremser (1838-1914)"]
        ]
        window_width, window_height = screen_config.WindowConfig.WIDTH, screen_config.WindowConfig.HEIGHT
        self.state.screen_width = window_width
        self.state.screen_height = window_height
        
        # init the main window
        self.main_canvas = self.screen_renderer.init_screen(window_width, window_height, screen_config.WindowConfig.CAPTION,
                                                    screen_config.WindowConfig.BACKGROUND_COLOR)
        #self.state.set_main_screen(self.main_canvas)
        self.state.set_main_screen(self.main_canvas)
        
        # init the main menu
        gt_start_state = MenuItemState()
        gt_end_state = MenuItemState()
        pause_play_state = MenuItemState()
        reset_menu_item_state = MenuItemState()
        play_menu_item_state= MenuItemState()
        save_menu_item_state = MenuItemState()
        # items for play sub-menu
        gt_start_state.add_step(MenuItemStateStep("GoToStartNV", "<<", "Go to start", None, Color.WHITE, Color.BLACK, self.menu_reset_score_navigator, self.menu_show_tooltip))
        pause_step = MenuItemStateStep("PauseNV", "||", "Pause player", None, Color.WHITE, Color.BLACK, self.menu_pause_score_navigator, self.menu_show_tooltip)
        continue_step = MenuItemStateStep("ContinueNV", ">", "Continue playing", pause_step, Color.WHITE, Color.BLACK, self.menu_continue_score_navigator, self.menu_show_tooltip)
        pause_step.set_next_step(continue_step)
        pause_play_state.add_step(pause_step)
        pause_play_state.add_step(continue_step)
        gt_end_state.add_step(MenuItemStateStep("GoToEndNV", ">>", "Go to end", None, Color.WHITE, Color.BLACK, self.menu_score_navigator_end, self.menu_show_tooltip))
        # items for main menu
        reset_menu_step = MenuItemStateStep("ResetMM", "Reset", "Click to reset everything.", None, Color.BLUE, Color.WHITE, self.menu_reset_action, self.menu_show_tooltip)
        play_menu_step1 = MenuItemStateStep("PlayMM","Play", "Click to play the score.", None, Color.BLUE, Color.WHITE, self.menu_play_notes, self.menu_show_tooltip)
        play_menu_step2 = MenuItemStateStep("StopMM","Stop", "Click to stop playing the score.", play_menu_step1, Color.RED, Color.WHITE, self.menu_cancel_score, self.menu_show_tooltip)
        #play_menu_step3 = MenuItemStateStep("HoverMM","Play", "Click to stop playing the score.", play_menu_step2, Color.PINK, Color.WHITE, self.menu_play_notes, self.menu_show_tooltip)
        
        play_menu_step1.set_next_step(play_menu_step2)
        save_menu_step = MenuItemStateStep("SaveMM", "Save", "Click to save the score.", None, Color.BLUE, Color.WHITE, self.menu_save_score, self.menu_show_tooltip)
        
        reset_menu_item_state.add_step(reset_menu_step)
        play_menu_item_state.add_step(play_menu_step1)
        play_menu_item_state.add_step(play_menu_step2)
       # play_menu_item_state.add_step(play_menu_step3)
        save_menu_item_state.add_step(save_menu_step)

        main_menu_color_config = MenuColorConfig(Color.BLUE, Color.PINK, Color.RED, Color.WHITE)
        sub_menu_color_config = MenuColorConfig(Color.WHITE, Color.LIGHT_GRAY, Color.GREY, Color.WHITE)

        play_submenu_data = [MenuData(gt_start_state, sub_menu_color_config), 
                             MenuData(pause_play_state, sub_menu_color_config), 
                             MenuData(gt_end_state, sub_menu_color_config)]
        main_menu_data = [MenuData(reset_menu_item_state, main_menu_color_config), 
                          MenuData(play_menu_item_state, main_menu_color_config, play_submenu_data),
                      MenuData(save_menu_item_state, main_menu_color_config)]
        
        main_menu = self.menu_builder \
            .set_menu_position(Position(0,0)) \
                .build_items(main_menu_data) \
                    .set_item_positions() \
                        .register_items_listeners(self.state) \
                            .build()
        self.state.set_main_menu(main_menu)

        # init the first staff
        grand_staff = self.init_staffs(window_width, default_time_signature, default_key_signature, tempo, velocity) 
        # use first staff to create music score
        self.music_score = self.score_builder_director.build_score(grand_staff, score_title, score_credits, tempo) 
        self.state.set_music_score(self.music_score)
        

    def run(self) -> None:
        """Run the main application loop."""
       # try:
        self.logger.info("Starting main application loop")
        clock = pygame.time.Clock()

        while self.state.is_running:
            # Handle events
            self.event_handler.handle_events()
           
            # Handle all polling
            self.event_handler.handle_polling()
            
            # Render the screen/music score
            self.screen_renderer.render_frame()

            # Small delay to prevent excessive CPU usage
            #pygame.time.wait(1)
            
            #clock.tick(3160)
            #pygame.display.flip()
            #self.staff_renderer.render_music_score(self.main_canvas, self.music_score)
            pygame.time.wait(10)

        #except KeyboardInterrupt:
            #self.logger.info("Application interrupted by user")
        #except Exception as e:
           # self.logger.error(f"Unexpected error in main loop: {e}")
            #raise MusicBoardApplicationError(f"Main loop failed: {e}") from e
        #finally:
            #self.cleanup()

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
    def init_staffs(self, window_width, time_signature, key_signature, tempo, velocity):        
        # record this for subsequent operations
        grand_staff = self.staff_builder_director.build_grand_staff(window_width, StaffConfig, (TREBLE_CLEF, BASS_CLEF), 
                                                                    time_signature, key_signature, tempo, velocity)
        return grand_staff
    
    def menu_reset_action(self, menu_item:MenuItem):
        # check that there are no active menu otherwise alert.
        print('resetting all user actions')
        self.state.reset_all_actions(menu_item)

    

    def menu_save_score(self, menu_item:MenuItem):
        # check that there are no active menu otherwise alert.
        print('saving score')
        menu_item.deactivate_item()
   
    def menu_show_tooltip(self, menu_item:MenuItem):
        # show tooltip on status bar
        print(f"Tooltip: {menu_item.get_current_step().tooltip}")
    
        
    def menu_reset_score_navigator(self, menu_item:MenuItem):
        pass

    def menu_pause_score_navigator(self, menu_item:MenuItem):
        pass

    def menu_continue_score_navigator(self, menu_item:MenuItem):
        pass

    def menu_score_navigator_end(self, menu_item:MenuItem):
        pass

    """ Play all notes on the score from beginning to end. """
    def menu_play_notes(self, menu_item:MenuItem): 
        menu_item.set_active()  
        menu_item.go_to_step_by_id("StopMM")      
        self.state.score_navigator.activate(self.state.music_score, menu_item)  
        

    """ Cancel/stop playing score """
    def menu_cancel_score(self, menu_item:MenuItem):  
        menu_item.deactivate_item()
        menu_item.go_to_step_by_id("PlayMM")      
        self.state.score_navigator.cancel(menu_item)
        