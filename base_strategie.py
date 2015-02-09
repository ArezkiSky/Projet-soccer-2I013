from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, GAME_WIDTH, GAME_HEIGHT
from soccersimulator import PygletObserver,ConsoleListener,LogListener
import math


class AllerVersPoint(SoccerStrategy) :
    def __init__ (self, direction) :
        self.direction = direction
        self.nom = "AllerVersPointStrat"
    def compute_strategy (self, state, player, teamid) :
        
        acceleration = self.direction - player.position
        shoot = Vector2D(0,0)
        action = SoccerAction(acceleration,shoot)
        
        return action
        
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def copy(self):
        return AllerVersPoint(self.direction)
    def create_strategy(self):
        return AllerVersPoint(self.direction)
        

        
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
        
     def start_battle(self,state):
        pass
     def finish_battle(self,won):
        pass
     def copy(self):
        return Tirer()
     def create_strategy(self):
        return Tirer()
        

        
        
class ComposeStrategy(SoccerStrategy) :
    def __init__(self,acceleration,shoot) :
        self.acceleration = acceleration
        self.shoot = shoot
    
    def compute_strategy(self, state, player, teamid):
        return SoccerAction(self.acceleration.compute_strategy(state, player, teamid).acceleration, self.shoot.compute_strategy(state, player, teamid).shoot)
        
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def copy(self):
        return ComposeStrategy(self.acceleration, self.shoot)
    def create_strategy(self):
        return ComposeStrategy()    
        



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
        
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def copy(self):
        return PlacementDefenseur()
    def create_strategy(self):
        return PlacementDefenseur()
            
            
            
class Degagement(SoccerStrategy) :
    def __init__(self) :
         SoccerStrategy.__init__(self, "degagement")
         
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
        
    def start_battle(self,state):
        pass
    def finish_battle(self,won):
        pass
    def copy(self):
        return PlacementDefenseur()
    def create_strategy(self):
        return PlacementDefenseur()
                       
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            