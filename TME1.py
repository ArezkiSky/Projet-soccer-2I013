# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 17:19:58 2015

@author: 3200982
"""

from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction
from soccersimulator import PygletObserver,ConsoleListener,LogListener

class RandomStrategy(SoccerStrategy):
    def __init__(self):
        self.name="Random"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def compute_strategy(self,state,player,teamid):
        shoot=Vector2D.create_random(-1,1)
        acceleration=Vector2D.create_random(-1,1)
        action = SoccerAction(acceleration,shoot)
        return action
    def copy(self):
        return RandomStrategy()
    def create_strategy(self):
        return RandomStrategy()




class FonceurStrategy(SoccerStrategy):
    def __init__(self):
        self.name="Fonceur"
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def idteamadverse(self,teamid) :
        if(teamid == 1) :
            return 2
        else : 
            return 1
                    
    def compute_strategy(self,state,player,teamid):
        acceleration=state.ball.position - player.position
        shoot= state.get_goal_center(self.idteamadverse(teamid)) - player.position
        action = SoccerAction(acceleration,shoot)
        return action
    def copy(self):
        return FonceurStrategy()
    def create_strategy(self):
        return FonceurStrategy()





