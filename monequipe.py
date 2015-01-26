from soccersimulator import SoccerBattle, SoccerPlayer, SoccerTeam
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from soccersimulator import pyglet
from strats import RandomStrategy
from TME2 import GoalStrategy
from TME1 import FonceurStrategy


team1=SoccerTeam("team1")
team1.add_player(SoccerPlayer("t1j1",GoalStrategy()))

team2=SoccerTeam("team2")
team2.add_player(SoccerPlayer("t2j1",GoalStrategy()))
team2.add_player(SoccerPlayer("t2j2",FonceurStrategy()))


team3=SoccerTeam("team3")
team3.add_player(SoccerPlayer("t3j1",GoalStrategy()))
team3.add_player(SoccerPlayer("t3j2",FonceurStrategy()))
team3.add_player(SoccerPlayer("t3j3",FonceurStrategy()))
team3.add_player(SoccerPlayer("t3j4",FonceurStrategy()))


teams =[team1, team2, team3]
