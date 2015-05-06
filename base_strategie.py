# -*- coding: utf-8 -*-
from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, GAME_WIDTH, GAME_HEIGHT, BALL_RADIUS, PLAYER_RADIUS
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from ToolBox import *
from math import pi


class StrategieAvecUtilitaire(SoccerStrategy) :
    def compute_strategy (self, state, player, teamid) :
        u = Utilitaire(state, player, teamid)
        return self.compute_strategy_utilitaire(u)
        
# Le joueur fonce vers un point donné

        
class AllerVersPoint(StrategieAvecUtilitaire) :
    def __init__ (self, direction) :
        self.direction = direction
        self.nom = "AllerVersPointStrat"
    def compute_strategy_utilitaire (self, u) :
        return u.bouger(u.versUnPoint())
        
# Le joueur fonce vers le ballon

class AllerVersBallon(StrategieAvecUtilitaire):
    def __init__(self):
        self.name="AllerVersBallonStrat"
    def compute_strategy_utilitaire (self, u) :
        return u.bouger(u.versLaBalle())
        
# Le joueur Tire vers les buts     

class Tirer(StrategieAvecUtilitaire) :
    def __init__ (self) :
        SoccerStrategy.__init__(self,"TirerStrat")   
    def compute_strategy_utilitaire (self, u) :
        if u.aLaBalle():
            return u.tirer(u.versLesButsAdverses())
        return u.rienDuTout()
        
# Le joueur Dégage le ballon avec un angle prédéfini

class Degagement(StrategieAvecUtilitaire):
    def __init__(self):
        self.name="DegagementStrat"
    def compute_strategy_utilitaire (self, u) :
       shoot = Vector2D(0,0) 
       if u.aLaBalle() :        
            if u.state.ball.speed.y < 0 :
                shoot = Vector2D.create_polar(u.versButsAdversesBallon().angle - pi/4.0, 100.0)
            else : 
                shoot = Vector2D.create_polar(u.versButsAdversesBallon().angle + pi/4.0, 100.0)
       return u.tirer(shoot)

# Le joueur tire autour de l'adversaire en face de lui


# Composition de deux stratègies, l'une basée sur le placement, l'autre sur le tir

class ComposeStrategy(StrategieAvecUtilitaire) :
    def __init__(self,acceleration,shoot) :
        self.acceleration = acceleration
        self.shoot = shoot   
    def compute_strategy_utilitaire (self, u) :
        return SoccerAction(self.acceleration.compute_strategy_utilitaire(u).acceleration, self.shoot.compute_strategy_utilitaire(u).shoot)
        
# Stratégie de placement en tant que defenseur

class PlacementDefenseur(StrategieAvecUtilitaire) :
    def __init__(self) :
        SoccerStrategy.__init__(self,"PlacementDefenseurStrat")
    def compute_strategy_utilitaire (self, u) :     
        if u.distanceBallonMesButs() > 40 :
            acceleration = u.entreBalleEtBut()
        else :
                acceleration = u.versLaBalle()                  
        
        return u.bouger(acceleration)   

# Stratégie de temporisation : attend l'acte du joueur a 9/10eme de la distance entre ses buts et le milieu du terrain

class Temporisation(StrategieAvecUtilitaire) :
    def __init__(self) :
        slef.name="TemporisationStrat"
    def compute_strategy_utilitaire (self, u) :
        milieuter = u.state.get_goal_center(u.teamid)        
        position = Vector2D(milieuter.x*0.1 + u.state.ball.position.x*0.9, milieuter.y*0.1 + u.state.ball.speed.y*0.9)
        return u.bouger(position)

# Stratégie de passe vers le joueur allié le plus proche

class Passe(StrategieAvecUtilitaire) :
    def __init__(self) :
         SoccerStrategy.__init__(self, "PasseStrat")   
    def compute_strategy_utilitaire (self, u) :
        joueurLePlusProche = u.versJoueurLePlusProche()
        if u.state.get_goal_center(u.adversaire())-u.player.position > u.state.get_goal_center(u.adversaire()) - u.joueurLePlusProche().position:
            if (u.aLaBalle()) :
                shoot = u.versJoueurLePlusProche()
                return u.tirer(shoot)
            return u.tirer(u.versLesButsAdverses())
        return u.rienDuTout()

# Stratégie de placement de goal :

class PlacementGoal(StrategieAvecUtilitaire):
    def __init__(self):
        self.name="PlacementGoalStrat"             
    def compute_strategy_utilitaire (self, u) :
        if u.distanceBallonMesButs() > 20 :
            return u.bouger(u.entreBalleEtBut())
        return u.bouger(u.versLaBalle())
            
# Stratégie de fonceur : combinaison AllerVersBallon + Tirer

class FonceurStrategy(StrategieAvecUtilitaire):
    def __init__(self):
        self.fonceurstrategy = ComposeStrategy(AllerVersBallon(), Tirer())
    def compute_strategy_utilitaire (self, u) :
        return self.fonceurstrategy.compute_strategy_utilitaire(u)

# Stratégie de défenseur 2v2 : combinaison PlacementDefenseur + passe

class DefenseurStrategy(StrategieAvecUtilitaire):
    def __init__(self):
        self.defenseurstrategy = ComposeStrategy(PlacementDefenseur(), Degagement())
    def compute_strategy_utilitaire (self, u) :
        return self.defenseurstrategy.compute_strategy_utilitaire(u)

# Stratégie de goal 2v2 : combinaison PlacementGoal + Passe

class Goal2v2Strategy(StrategieAvecUtilitaire):
    def __init__(self) :
        self.name = "goal2v2strategy"
        self.goal2v2strategy = ComposeStrategy(PlacementGoal(), Degagement())
    def compute_strategy_utilitaire (self, u) :
        return self.goal2v2strategy.compute_strategy_utilitaire(u)
       
class TirCote (StrategieAvecUtilitaire):
    def __init__(self):
        self.name="TirCoteStrat"   
    def compute_strategy_utilitaire(self,u):
        if u.aLaBalle():
            if u.state.ball.speed.y < 0 :
                return u.tirer(Vector2D(u.versLesButsAdverses().x, u.versLesButsAdverses().y - 9))
            else :
                return u.tirer(Vector2D(u.versLesButsAdverses().x, u.versLesButsAdverses().y + 9))
        else :
            return u.rienDuTout()
       
        
        
class ButeurStrategy (StrategieAvecUtilitaire) :
    def __init__(self):
        self.buteurStrategy = ComposeStrategy(AllerVersBallon(), TirCote())
    def compute_strategy_utilitaire(self, u) :
            return self.buteurStrategy.compute_strategy_utilitaire(u)
            
            
class DefenseurTMEsolo (StrategieAvecUtilitaire) :
    def __init__(self, adversaire): 
        SoccerStrategy.__init__(self, "DefenseurTMEsolo")
    def compute_strategy_utilitaire (self, u) :     
        if u.quiABalle() == adversaire.teamid:
            acceleration = u.versLaBalle()    
        else :
            acceleration = u.entreBalleEtBut()          
        
        return u.bouger(acceleration)       
        
        
        
class FonceurIceMud(StrategieAvecUtilitaire) :
    def __init__(self) :
        SoccerStrategy.__init__(self, "FonceurIceMud")
        
    def compute_strategy_utilitaire(self, u) :
        for z in u.state.danger_zones :
            if u.posBalle() > z.bottom_left and u.posBalle() < z.bottom_left+ u.z.diagonal and z.type == "ice" :
                return u.bouger(u.state.danger_zones[z].bottom_left, Vector2D(0,0))
            else :
                u.posBalle() > z.bottom_left and u.posBalle() < z.bottom_left+ z.diagonal and z.type == "mud":
                return u.bougertirer(u.versLaBalle(), u.versLesButsAdverses())       
                
            
         
class PlacementDefenseurIceMud(StrategieAvecUtilitaire) :
    def __init__(self) :
        SoccerStrategy.__init__(self, "PlacementDefenseurIceMud")
        
    def compute_strategy_utilitaire(self, u) :
         if u.distanceBallonMesButs() > 20 :
            return u.bouger(u.entreBalleEtBut())
        else :            
            for z in u.state.danger_zones :
                if u.posBalle() z.bottom_left and u.posBalle() < z.bottom_left+ z.diagonal and z.type == "ice" :
                    return u.bouger(u.state.danger_zones[z].bottom_left)
                else :
                    if u.posBalle() > z.bottom_left and u.posBalle() < z.bottom_left+ z.diagonal and z.type == "mud":
                        return u.bouger(u.versLaBalle())    
                    else :
                        return u.bouger(u.versLaBalle())

class DegagementIceMud(StrategieAvecUtilitaire) :
      def __init__(self) :
          SoccerStrategy.__init__(self, "DegagementIceMud")
          
      def compute_strategy_utilitaire(self, u) :
          shoot = Vector2D(0,0) 
          for z in u.state.danger_zones :
              if u.aLaBalle() :        
                    if u.state.ball.speed.y > z.bottom_left and u.posBalle() < z.bottom_left+ z.diagonal and z.type == "ice" :
                        shoot = Vector2D.create_polar(u.versButsAdversesBallon().angle - pi/4.0, 100.0)
                    else : 
                        shoot = Vector2D.create_polar(u.versButsAdversesBallon().angle + pi/4.0, 100.0)
               return u.tirer(shoot) 
                
          
        
    
    
                        
class DefenseurIceMud(StrategieAvecUtilitaire) :
    def __init__(self):
        self.defenseuricemudstrategy = ComposeStrategy(PlacementDefenseurIceMud(), DegagementIceMud())
    def compute_strategy_utilitaire (self, u) :
        return self.defenseurstrategy.compute_strategy_utilitaire(u)
        
        
        
        
        