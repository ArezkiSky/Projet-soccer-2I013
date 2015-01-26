# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:27:50 2015

@author: 3200982
"""

from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction
from soccersimulator import PygletObserver,ConsoleListener,LogListener

class GoalStrategy(SoccerStrategy):
    def __init__(self):
        self.name="Goal"
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
        diff = state.ball.position - player.position
        if diff.norm > 5 :
            vitesse = state.ball.position + state.get_goal_center(teamid) - player.position - player.position 
            shoot= state.get_goal_center(self.idteamadverse(teamid)) - player.position
        else : 
            vitesse = state.ball.position - player.position
            shoot= state.get_goal_center(self.idteamadverse(teamid)) - player.position
        action = SoccerAction(vitesse,shoot)
        return action
    def copy(self):
        return GoalStrategy()
    def create_strategy(self):
        return GoalStrategy()
        
        

