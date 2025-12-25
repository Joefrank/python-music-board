from Services.Builders.MusicScoreBuilder import MusicScoreBuilder

class MusicScoreBuilderDirector:
    
    def __init__(self):
        self.music_score = None
        self.music_score_builder = MusicScoreBuilder()
    
    def build_score(self, grand_staff, score_title, score_credits, tempo=80):
        self.music_score = self.music_score_builder \
            .init_score(grand_staff, score_title, score_credits, tempo) \
                .build_score_credit() \
                    .set_title_position() \
                        .build()
        
        return self.music_score