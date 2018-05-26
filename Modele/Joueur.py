'''
Created on 8 mai 2018

@author: Loic
'''
class Joueur:
    def __init__(self,nomJoueur):
        self.nom = nomJoueur
        self.score = 0
        self.restants = 100
        self.couleurs = []
        
    def ajoutCouleur(self,valeur):
        self.couleurs.insert(self.couleurs.__len__(), valeur)
        
    def setScore(self,scr):
        self.score = scr