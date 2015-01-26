# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:48:43 2015

@author: 3200982
"""

#Test


from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from TME2 import GoalStrategy
from TME1 import FonceurStrategy

team1=SoccerTeam("team1")
team2=SoccerTeam("team2")
team1.add_player(SoccerPlayer("t1j1",GoalStrategy()))
team2.add_player(SoccerPlayer("t2j1",GoalStrategy()))
team1.add_player(SoccerPlayer("t1j2",FonceurStrategy()))
team2.add_player(SoccerPlayer("t2j2",FonceurStrategy()))
battle=SoccerBattle(team1,team2)
obs=PygletObserver()
obs.set_soccer_battle(battle)
pyglet.app.run()