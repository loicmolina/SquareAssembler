'''
Created on 8 mai 2018

@author: Loic
'''

from Modele.Tableau import tableau
from Modele.Joueur import Joueur
from Modele.Dictionnaire import Affectation

class Jeu:
    def __init__(self,nbJoueurs,tempsMaxTour):
        self.tab = tableau()
        self.gameover = -1  
        self.joueur1 = Joueur("J1",1)
        self.joueur2 = Joueur("J2",2)
        self.nbjoueurs = nbJoueurs
        self.tempsTourMax = tempsMaxTour
        self.tempsTour = self.tempsTourMax
        self.joueurTour = self.joueur1 #Le joueur 1 commence
        self.joueurAdverse = self.joueur2
        self.couleurs = Affectation()
        self.joueurTour.restants = 100
        self.joueurAdverse.restants = 100
        self.taille = 600
        self.taillecase = 600/self.tab.lignes
    

    def joinTable(self,tablestr): 
        self.tab.settable(tablestr)
        self.gameover = 0
        

    def newTable(self,nb):  
        if (self.nbjoueurs == 1): 
            self.gameover = 0
        else:
            self.gameover = -1
        self.tab.resize(nb)
        self.taillecase = 600/self.tab.lignes
        self.joueurTour.restants = 100
        self.joueurAdverse.restants = 100
        self.joueur1.score = 0
        self.joueur2.score = 0        
        
        
    def setTime(self,tpsM):
        self.tempsTourMax = tpsM
        self.tempsTour = tpsM
        
    def tour(self,x,y):
        listeCases = self.tab.find(x,y,self.tab.tableau[x][y])
        if listeCases.__len__()>=3:            
            
            if self.nbjoueurs==2 and self.tab.tableau[x][y]>0 and self.joueurTour.couleurs.__len__() < self.tab.lignes/5 and self.tab.tableau[x][y] not in self.joueur1.couleurs and self.tab.tableau[x][y] not in self.joueur2.couleurs :
                self.joueurTour.couleurs.insert(self.joueurTour.couleurs.__len__(), self.tab.tableau[x][y])
            
            if self.nbjoueurs == 1 or self.tab.tableau[x][y] in self.joueurTour.couleurs:
                self.tempsTour = self.tempsTourMax
                self.tab.clean(listeCases)
                self.joueurTour.score = self.joueurTour.score + listeCases.__len__()              
                self.tab.chutevertical()
                self.tab.chutehorizontal()
                self.conditionsfin()     

                        
                
    def conditionsfin(self):
        if self.nbjoueurs==1:
            self.joueurTour.restants = self.tab.continuer()    
            if self.joueurTour.restants == 0:
                self.gameover = 1        
            
        if self.nbjoueurs == 2:
            self.joueurTour.restants = self.tab.continuerjoueur(self.joueurTour.couleurs)
            self.joueurAdverse.restants = self.tab.continuerjoueur(self.joueurAdverse.couleurs)
            #print("test de changement correct current : ",self.joueurTour.restants,self.joueurTour.couleurs.__len__(),"==",int(self.tab.lignes/5))
            #print("test de changement correct adverse : ",self.joueurAdverse.restants,self.joueurAdverse.couleurs.__len__(),"==",self.tab.lignes/5)

            if (self.joueurAdverse.restants == 0 and self.joueurAdverse.couleurs.__len__()==int(self.tab.lignes/5)):
                #print("l'adversaire ne peut plus jouer")
                if (self.joueurTour.restants == 0 and self.joueurTour.couleurs.__len__()==int(self.tab.lignes/5)):
                    #print("Vous non plus, fin de la partie")
                    self.gameover = 1
            else:
                self.changerjoueur()
                #print("au tour de ",self.joueurTour.nom," ses couleurs sont ",self.joueurTour.couleurs)
                #print("l'adversaire ",self.joueurAdverse.nom," ses couleurs sont ",self.joueurAdverse.couleurs)
        
            
                


    def changerjoueur(self):
        if self.joueurTour.nom == self.joueur1.nom:
            self.joueurTour = self.joueur2
            self.joueurAdverse = self.joueur1
        else:
            self.joueurTour = self.joueur1     
            self.joueurAdverse = self.joueur2   
    
