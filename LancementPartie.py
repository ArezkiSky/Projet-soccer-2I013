# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:48:43 2015

@author: 3200982
"""

#Test


from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, GAME_WIDTH, GAME_HEIGHT
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from TME2 import GoalStrategy
from TME1 import FonceurStrategy
from base_strategie import AllerVersPoint, Tirer, ComposeStrategy, PlacementDefenseur, Degagement


team1=SoccerTeam("team1")
team2=SoccerTeam("team2")
team1.add_player(SoccerPlayer("t1j1",FonceurStrategy()))
team1.add_player(SoccerPlayer("t1j4",ComposeStrategy(PlacementDefenseur(),Degagement())))
team1.add_player(SoccerPlayer("t1j3",GoalStrategy()))
team1.add_player(SoccerPlayer("t1j2",FonceurStrategy()))
team2.add_player(SoccerPlayer("t2j1",FonceurStrategy()))
team2.add_player(SoccerPlayer("t2j2",FonceurStrategy()))
team2.add_player(SoccerPlayer("t2j3",GoalStrategy()))
team2.add_player(SoccerPlayer("t2j4",ComposeStrategy(PlacementDefenseur(),Degagement())))

battle=SoccerBattle(team1,team2)
obs=PygletObserver()
obs.set_soccer_battle(battle)
pyglet.app.run()