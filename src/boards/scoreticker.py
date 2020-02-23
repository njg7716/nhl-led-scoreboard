"""
    Shows list of games.
    TODO:
        Make sliding animation.
"""
from time import sleep
from utils import center_obj
from data.scoreboard import Scoreboard
from renderer.scoreboard import ScoreboardRenderer

class Scoreticker:
    def __init__(self, data, matrix):
        self.data = data
        self.rotation_rate = self.data.config.scoreticker_rotation_rate
        self.matrix = matrix
        self.spacing = 3 # Number of pixel between each dot + 1

    def render(self):
        self.index = 0
        self.games = self.data.games
        self.num_games = len(self.games)
        try:
            while True:
                self.matrix.clear()
                if self.index >= (len(self.games)):
                    return

                ScoreboardRenderer(self.data, self.matrix, Scoreboard(self.games[self.index], self.data.teams_info, self.data.config)).render()
                self.show_indicator()
                self.matrix.render()

                if self.data.network_issues:
                    self.matrix.network_issue_indicator()

                sleep(self.rotation_rate)
                self.index += 1

        except IndexError:
            print("NHL OFF DAY today")
            return

    def show_indicator(self):
        """
            TODO: This function need to be coded a better way. but it works :D

            Carousel indicator.
        """
        # Tell if there is a lot of games (12+)
        self.many_games = False

        # if there is more then 11 games, reduce the spacing of each dots
        if self.num_games > 10:
            self.many_games = True
            self.spacing = 2

        # Measure the width of the indicator and then center it on the screen
        indicator_length = (self.num_games * self.spacing) - (self.spacing - 1)
        align = center_obj(self.matrix.width, indicator_length)

        # Move back the indicator by 1 pixel if the number of games is even.
        if self.num_games%2 == 0 and self.many_games == False:
            align -= 1

        # Render the indicator
        for i in range(self.num_games):
            dot_position = ((self.spacing * i) - 1) + 1
            if i == self.index:
                self.matrix.set_pixel(((align + dot_position), 30), (255, 50, 50))
            else:
                self.matrix.set_pixel(((align + dot_position), 30), (70, 70, 70))