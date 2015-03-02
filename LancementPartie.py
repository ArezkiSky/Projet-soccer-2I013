# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:48:43 2015

@author: 3200982
"""

#Test


from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, GAME_WIDTH, GAME_HEIGHT
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from base_strategie import *


team1=SoccerTeam("team1")
team2=SoccerTeam("team2")
team1.add_player(SoccerPlayer("t1j1",Goal1v1Strategy()))
team1.add_player(SoccerPlayer("t1j2",DefenseurStrategy()))
team2.add_player(SoccerPlayer("t2j1",FonceurStrategy()))
team2.add_player(SoccerPlayer("t2j2",DribleStrategy()))




battle=SoccerBattle(team1,team2)
obs=PygletObserver()
obs.set_soccer_battle(battle)
pyglet.app.run()