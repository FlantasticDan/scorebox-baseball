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
        self.inning_mode = 'top'

        self.base_1 = False
        self.base_2 = False
        self.base_3 = False

        self.strikes = 0
        self.balls = 0
        self.outs = 0
    
    def export_game_state(self) -> Dict:
        return {
            'home_team': self.home_team,
            'home_color': self.home_color,
            'home_score': self.home_score,
            'visitor_team': self.visitor_team,
            'visitor_color': self.visitor_color,
            'visitor_score': self.visitor_score,
            'inning': self.inning,
            'inning_mode': self.inning_mode,
            'base_1': self.base_1,
            'base_2': self.base_2,
            'base_3': self.base_3,
            'strikes': self.strikes,
            'balls': self.balls,
            'outs': self.outs
        }

    def adjust_score(self, team: str, score: int):
        if score < 0:
            score = 0
        if team == 'home':
            self.home_score = score
        else:
            self.visitor_score = score
    
    def strike(self, strikes: int):
        self.strikes = strikes
        if self.strikes >= 3:
            self.strikeout()

    def strikeout(self):
        self.out(self.outs + 1)
        self.reset_count()

    def out(self, outs: int):
        self.outs = outs
        if self.outs >= 3:
            self.three_outs()
    
    def three_outs(self):
        self.reset_outs()
        self.reset_count()
        self.clear_bases()
        self.advance_inning()

    def clear_bases(self):
        self.base_1 = False
        self.base_2 = False
        self.base_3 = False

    def advance_inning(self):
        if self.inning_mode == 'top':
            self.inning_mode = 'mid'
        elif self.inning_mode == 'bot':
            self.inning_mode = 'end'
    
    def ball(self, balls: int):
        self.balls = balls
        if self.balls >= 4:
            self.walk()
    
    def walk(self):
        self.reset_count()

        if not self.base_1:
            self.base_1 = True
        else:
            if not self.base_2:
                self.base_2 = True
            else:
                if not self.base_3:
                    self.base_3 = True
                else:
                    self.walkoff_run()
    
    def walkoff_run(self):
        if self.inning_mode == 'top':
            self.visitor_score += 1
        elif self.inning_mode == 'bot':
            self.home_score += 1
    
    def set_inning(self, inning: int):
        if inning < 1:
            inning = 1
        self.inning = inning
        if self.inning_mode == 'end':
            self.inning_mode ='top'
    
    def set_inning_mode(self, inning_mode: str):
        self.inning_mode = inning_mode
    
    def reset_count(self):
        self.strikes = 0
        self.balls = 0
    
    def reset_outs(self):
        self.outs = 0
    
    def set_base(self, base: int, state: bool):
        if base == 1:
            self.base_1 = state
        elif base == 2:
            self.base_2 = state
        elif base == 3:
            self.base_3 = state