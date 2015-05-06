from soccersimulator import SoccerBattle, SoccerPlayer, SoccerTeam
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from soccersimulator import pyglet
from base_strategie import *
from ToolBox import *



team1=SoccerTeam("Minute Maid Tropical")
team1.add_player(SoccerPlayer("t1j1",FonceurStrategy()))

team2=SoccerTeam("Minute Maid Orange")
team2.add_player(SoccerPlayer("t2j1",Goal2v2Strategy()))
team2.add_player(SoccerPlayer("t2j2",FonceurStrategy()))


team3=SoccerTeam("Minute Maid Pomme")
team3.add_player(SoccerPlayer("t1j1",FonceurStrategy()))
team3.add_player(SoccerPlayer("t1j4",DefenseurStrategy()))
team3.add_player(SoccerPlayer("t1j3",Goal2v2Strategy()))
team3.add_player(SoccerPlayer("t1j2",FonceurStrategy()))

teams =[team1, team2, team3]
