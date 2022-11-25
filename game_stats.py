import json


class GameStats():
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score_file = "highscore.json"
        with open(self.high_score_file) as f:
            self.high_score = json.load(f)

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def write_highscore(self):
        with open(self.high_score_file, 'w') as f:
            json.dump(self.high_score, f)
