from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, GAME_WIDTH, GAME_HEIGHT
from soccersimulator import PygletObserver,ConsoleListener,LogListener
import math

# Le joueur fonce vers un point donné

class AllerVersPoint(SoccerStrategy) :
    def __init__ (self, direction) :
        self.direction = direction
        self.nom = "AllerVersPointStrat"
    def compute_strategy (self, state, player, teamid) :
        acceleration = self.direction - player.position
        shoot = Vector2D(0,0)
        action = SoccerAction(acceleration,shoot)
        return action
        
# Le joueur fonce vers le ballon

class AllerVersBallon(SoccerStrategy):
    def __init__(self):
        self.name="AllerVersBallonStrat"
    def compute_strategy(self,state,player,teamid):
        shoot = Vector2D(0,0)
        acceleration = state.ball.position-player.position
        return SoccerAction(acceleration,shoot)
        
# Le joueur Tire vers les buts     

class Tirer(SoccerStrategy) :
    def __init__ (self) :
        SoccerStrategy.__init__(self,"TirerStrat")   
    def idteamadverse(self,teamid) :
        if(teamid == 1) :
            return 2
        else : 
            return 1
    def compute_strategy (self, state, player, teamid) :
        acceleration = Vector2D(0,0)
        shoot =  state.get_goal_center(self.idteamadverse(teamid)) - player.position
        action = SoccerAction(acceleration,shoot)  
        return action
        
# Composition de deux stratègies, l'une basée sur le placement, l'autre sur le tir

class ComposeStrategy(SoccerStrategy) :
    def __init__(self,acceleration,shoot) :
        self.acceleration = acceleration
        self.shoot = shoot   
    def compute_strategy(self, state, player, teamid):
        return SoccerAction(self.acceleration.compute_strategy(state, player, teamid).acceleration, self.shoot.compute_strategy(state, player, teamid).shoot)
        
# Stratégie de placement en tant que defenseur

class PlacementDefenseur(SoccerStrategy) :
    def __init__(self) :
        SoccerStrategy.__init__(self,"PlacementDefenseurStrat")
    def compute_strategy (self, state, player, teamid) :
        diff = state.ball.position - state.get_goal_center(teamid)      
        if diff.norm > 60 :
            acceleration = state.ball.position + state.get_goal_center(teamid) - player.position - player.position 
            shoot= Vector2D(0,0)
        else :
                acceleration = state.ball.position - player.position
                shoot= Vector2D(0,0)                    
        action = SoccerAction(acceleration,shoot)
        return action    
        
# Stratégie de tir vers le but + un angle défini pour dégager le ballon

class Degagement(SoccerStrategy) :
    def __init__(self) :
         SoccerStrategy.__init__(self, "DegagementStrat")   
    def idteamadverse(self,teamid) :
        if(teamid == 1) :
            return 2
        else : 
            return 1
    def compute_strategy (self, state, player, teamid) :
        acceleration = Vector2D(0,0)
        shoot = state.get_goal_center(self.idteamadverse(teamid)) - player.position 
        shoot = Vector2D(GAME_WIDTH/2 * math.cos(GAME_WIDTH/2), GAME_HEIGHT/2 * math.sin(GAME_HEIGHT/2))        
        action = SoccerAction(acceleration,shoot)
        return action
        
# Stratégie de fonceur : combinaison AllerVersBallon + Tirer

class FonceurStrategy(SoccerStrategy):
    def __init__(self):
        self.fonceurstrategy = ComposeStrategy(AllerVersBallon(), Tirer())
    def compute_strategy(self,state,player,teamid):
        return self.fonceurstrategy.compute_strategy(state,player,teamid)
        
# Stratégie de défenseur : combinaison PlacementDefenseur + Degager

class DefenseurStrategy(SoccerStrategy):
    def __init__(self):
        self.defenseurstrategy = ComposeStrategy(PlacementDefenseur(), Degagement())
    def compute_strategy(self,state,player,teamid):
        return self.defenseurstrategy.compute_strategy(state,player,teamid)

# Stratégie de placement de goal :

class PlacementGoal(SoccerStrategy):
    def __init__(self):
        self.name="PlacementGoalStrat"
    def idteamadverse(self,teamid) :
        if(teamid == 1) :
            return 2
        else : 
            return 1                 
    def compute_strategy (self, state, player, teamid) :
        diff = state.ball.position - state.get_goal_center(teamid)      
        if diff.norm > 5 :
            acceleration = state.ball.position + state.get_goal_center(teamid) - player.position - player.position 
            shoot= Vector2D(0,0)
        else :
                acceleration = state.ball.position - player.position
                shoot= Vector2D(0,0)                    
        action = SoccerAction(acceleration,shoot)
        return action

# Stratégie de gardien de but qui dégage : Combinaison PlacementGoal + Degagement

class GoalStrategy(SoccerStrategy):
    def __init__(self):
        self.gardienstrategy = ComposeStrategy(PlacementGoal(), Degagement())
    def compute_strategy(self,state,player,teamid):
        return self.gardienstrategy.compute_strategy(state,player,teamid)   
