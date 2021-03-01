'''ScoreBox Baseball Manager'''

from typing import Dict


class BaseballManager:
    def __init__(self, home_team, visitor_team, home_color, visitor_color) -> None:
        self.home_team = home_team
        self.home_color = home_color
        self.visitor_team = visitor_team
        self.visitor_color = visitor_color

        # Game State
        self.home_score = 0
        self.visitor_score = 0

        self.inning = 1
        self.inninig_mode = 'top'

        self.base_1 = False
        self.base_2 = False
        self.base_3 = False

        self.strikes = 0
        self.balls = 0
        self.outs = 0

        print(self.export_game_state())
    
    def export_game_state(self) -> Dict:
        return {
            'home_team': self.home_team,
            'home_color': self.home_color,
            'home_score': self.home_score,
            'visitor_team': self.visitor_team,
            'visitor_color': self.visitor_color,
            'visitor_score': self.visitor_score,
            'inning': self.inning,
            'inning_mode': self.inninig_mode,
            'base_1': self.base_1,
            'base_2': self.base_2,
            'base_3': self.base_3,
            'strikes': self.strikes,
            'balls': self.balls,
            'outs': self.outs
        }
