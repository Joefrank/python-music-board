from Services.Builders import *
from Services.Builders import MusicScoreBuilder

class MusicScoreBuilderDirector:
    
    def __init__(self):
        self.music_score = None
        self.music_score_builder = MusicScoreBuilder.MusicScoreBuilder()
    
    def build_score(self, grand_staff, score_title, score_credits):
        self.music_score = self.music_score_builder \
            .init_score(grand_staff, score_title, score_credits) \
                .build_score_credit() \
                    .set_title_position() \
                        .build()
        
        return self.music_score