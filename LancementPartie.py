# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 18:48:43 2015

@author: 3200982
"""

#Test


from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, GAME_WIDTH, GAME_HEIGHT, InteractStrategy, TreeStrategy
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from base_strategie import *


team1=SoccerTeam("team1")
team2=SoccerTeam("team2")
team2.add_player(SoccerPlayer("t2j1",DefenseurTMEsolo("t1j1")))

list_key_player1=['a','z','e']
list_strat_player1=[Goal2v2Strategy(),FonceurStrategy(), ButeurStrategy()]
inter_strat_player1=InteractStrategy(list_key_player1,list_strat_player1,"joueur1")

team1.add_player(SoccerPlayer("t1j1",inter_strat_player1,))


battle=SoccerBattle(team1,team2)
obs=PygletObserver()
obs.set_soccer_battle(battle)
pyglet.app.run()