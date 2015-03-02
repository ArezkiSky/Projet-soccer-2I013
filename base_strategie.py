# -*- coding: utf-8 -*-
from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, GAME_WIDTH, GAME_HEIGHT, BALL_RADIUS, PLAYER_RADIUS
from soccersimulator import PygletObserver,ConsoleListener,LogListener
from ToolBox import *
import math

# Le joueur fonce vers un point donné
class StrategieAvecUtilitaire(SoccerStrategy) :
    def compute_strategy (self, state, player, teamid) :
        u = Utilitaire(state, player, teamid)
        return self.compute_strategy_utilitaire(u)
        
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

class Degagement(SoccerStrategy):
    def __init__(self):
        self.name="DegagementStrat"
    def compute_strategy_utilitaire (self, u) :
        shoot = Vector2D.create_polar(u.player.angle + 3.5, 100)
        return u.tirer(shoot)

# Le joueur tire autour de l'adversaire en face de lui

class Contournement(StrategieAvecUtilitaire) :
    def __init__(self) :
        SoccerStrategy.__init__(self, "ContournerStrat")
    def compute_strategy_utilitaire (self, u) :
        shoot = Vector2D.create_polar(u.versLesButsAdverses.angle + 45,1)
        return u.tirer(shoot)
            
        
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
        if u.distanceBallonMesButs().norm > 45 :
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
        position = Vector2D(milieuter.x*0.1 + u.state.ball.position.x*0.9, milieuter.y*0.1 + u.state.ball.position.y*0.9)
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
        if u.distanceBallonMesButs().norm > 5 :
            return u.bouger(u.entreBalleEtBut())
        return u.bouger(u.versLaBalle())
            
# Stratégie de fonceur : combinaison AllerVersBallon + Tirer

class FonceurStrategy(StrategieAvecUtilitaire):
    def __init__(self):
        self.fonceurstrategy = ComposeStrategy(AllerVersBallon(), Tirer())
    def compute_strategy_utilitaire (self, u) :
        return self.fonceurstrategy.compute_strategy_utilitaire(u)

# Stratégie de défenseur 2v2 : combinaison PlacementDefenseur + Passe

class DefenseurStrategy(StrategieAvecUtilitaire):
    def __init__(self):
        self.defenseurstrategy = ComposeStrategy(PlacementDefenseur(), Degagement())
    def compute_strategy_utilitaire (self, u) :
        return self.defenseurstrategy.compute_strategy_utilitaire(u)


# Stratégie de gardien de but 1v1 qui intercepte et fonce au but : Combinaison GoalStrategy + FonceurStrategy

class Goal1v1Strategy(StrategieAvecUtilitaire):
    def __init__(self):
        self.name="Goal1v1Strat"             
    def compute_strategy_utilitaire (self, u) :
        
        if u.versLaBalle().norm > 10 :
            return u.bouger(u.entreBalleEtBut())
        else : 
            return SoccerAction(u.versLaBalle(), u.versLesButsAdverses())  

# Strtégie de dribleur : Combinaison AllerVersBallon + Drible(contournement)

class DribleStrategy(StrategieAvecUtilitaire):
    def __init__(self):
        self.dribleStrategy = ComposeStrategy(AllerVersBallon(), Contournement())
        self.fonceurstrategy = ComposeStrategy(AllerVersBallon(), Tirer())
    def compute_strategy_utilitaire (self, u) :
        if(u.aLaBalle) :
            return self.fonceurstrategy.compute_strategy_utilitaire(u)
        return self.dribleStrategy.compute_strategy_utilitaire(u)
