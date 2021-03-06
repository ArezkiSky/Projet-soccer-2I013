# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 18:27:33 2015

@author: 3200982
"""

#encoding=utf8

from soccersimulator import pyglet
from soccersimulator import Vector2D, SoccerBattle, SoccerPlayer, SoccerTeam, SoccerStrategy, SoccerAction, GAME_WIDTH, GAME_HEIGHT, BALL_RADIUS, PLAYER_RADIUS
from soccersimulator import PygletObserver,ConsoleListener,LogListener
import math

class Utilitaire :
        def __init__ (self, state, player, teamid) :
            self.state = state
            self.player = player
            self.teamid = teamid
            
# ID team Adverse     
       
        def adversaire(self) :
            if(self.teamid == 1) :
                return 2
            else : 
                return 1

# Mon joueur est à portée pour tirer la balle, "il a la balle"

        def aLaBalle(self) :
            return self.player.position.distance(self.state.ball.position)<=(PLAYER_RADIUS+BALL_RADIUS)
            
# Vecteur vers un point 

        def versUnPoint(self, direction) :
            return direction - self.player.position
# Vecteur en direction de la Balle
        
        def versLaBalle(self) :
           return self.state.ball.position-self.player.position
          
# Vecteur en direction des buts adverses

        def versLesButsAdverses(self) :
            return self.state.get_goal_center(self.adversaire()) - self.player.position
            
# Vecteur de la distance entre mes buts et le ballon
        
        def distanceBallonMesButs(self) :
            return self.state.ball.position - self.state.get_goal_center(self.teamid)

# Vecteur de la distance entre le ballon et le joueur adverse 

        def distanceBallonAdversaire(self) :
            return self.state.ball.position - self.player.adversaire().position
            
# Vecteur de la distance entre mon joueur et les buts adverses

        def distanceJoueurButAdverse(self) :
            return self.state.get_goal_center(adversaire()) - self.player.position
                                
# Mon joueur ne fait rien
        
        def rienDuTout(self) :
            return SoccerAction(Vector2D(0,0), Vector2D(0,0))
           
# Mon joueur bouge vers un endroit (sans tirer)           
           
        def bouger(self, acceleration) : 
            return SoccerAction(acceleration, Vector2D(0,0))
            
# Mon joueur tire vers un endroit (sans bouger)
            
        def tirer(self, shoot) :
            return SoccerAction(Vector2D(0,0), shoot)
            
# Mon joueur bouge et tire vers un endroit
        def bougertirer(self, acceleration, shoot) :
            return SoccerAction(acceleration, shoot)
            
# Mon joueur se place entre la balle est ses buts

        def entreBalleEtBut(self) :
            return self.state.ball.position + self.state.get_goal_center(self.teamid) - self.player.position - self.player.position
            
# Id du joueur le plus proche du joueur ami avec le ballon hormis le joueur avec le ballon

        def joueurLePlusProche(self) :
            if (self.teamid == 1) :
                res = [self.state.ball.position.distance(p.position) for p in self.state.team1.players if p!= self.player]
                m = min(res)
                return self.state.team1.players[res.index(m)]
            else :
                res = [self.state.ball.position.distance(p.position) for p in self.state.team2.players if p!= self.player]
                m=min(res)
                return self. state.team2.players[res.index(m)]
                
# Vecteur vers joueur le plus proche du joueur ami avec le ballon hormis le joueur avec le ballon
                
        def versJoueurLePlusProche(self) :
            return self.joueurLePlusProche().position - self.player.position
            

# Indique si mon équipe possède le ballon ou non

        def onALaBalle(self):
            x = 12345
            for p in self.state.team1 :
                    distanceDuBallon = self.state.ball.position - p.position
                    if(distanceDuBallon.norm < x):
                        x = distanceDuBallon.norm
            y = 12345
            for q in self.state.team2 :
                    distanceDuBallon2 = self.state.ball.position - q.position
                    if(distanceDuBallon.norm < x):
                        y = distanceDuBallon2.norm
            if(((x < y and self.team == 1) or (x > y and self.team == 2)) and y < GAME_WIDTH * 0.2):
                return True
            else:
                return False
            
        