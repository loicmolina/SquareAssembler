'''
Created on 6 mai 2018

@author: Loic
'''
import random
from random import randint
from Modele.Dictionnaire import Affectation

class tableau:
    
    
    
    def __init__(self):
        self.couleurs = Affectation()
        self.colonnes = 20
        self.lignes = 20  
        self.tableau = [[0 for x in range(self.colonnes)] for y in range(self.lignes)]
        
        
        for x in range(20):
            for y in range(20):                
                liste = self.couleurs.couleurs()   
                nbcouleur =  self.couleurs.select(liste, random.randint(0,liste.__len__()-1))
                self.tableau[x][y]=nbcouleur
        



    def resize(self,nb):
        self.colonnes = nb
        self.lignes = nb
        self.couleurs.setnbmax(nb)
        self.tableau = [[0 for x in range(self.colonnes)] for y in range(self.lignes)]
        
        for x in range(nb):
            for y in range(nb):                
                liste = self.couleurs.couleurs()        
                nbcouleur =  self.couleurs.select(liste, random.randint(0,liste.__len__()-1))
                self.tableau[x][y]=nbcouleur
                
        
    def find(self,x,y,valeur):
        listMove = []
        self.findrec(x,y,valeur,listMove)
        resultat = listMove.__len__() 
        if (resultat>=3):            
            self.clean(listMove)
            return resultat
        else:
            return 0
               
        
    def findrec(self,x,y,valeur,listMove):
        if (valeur > 0):
            listMove.insert(listMove.__len__(),[x,y])
                              
            if x>0 and self.tableau[x-1][y] == valeur and not [x-1,y] in listMove:
                self.findrec(x-1,y,valeur,listMove) 
            if x<self.lignes-1 and self.tableau[x+1][y] == valeur and not [x+1,y] in listMove:
                self.findrec(x+1,y,valeur,listMove) 
            if y>0 and self.tableau[x][y-1] == valeur and not [x,y-1] in listMove:
                self.findrec(x,y-1,valeur,listMove) 
            if y<self.colonnes-1 and self.tableau[x][y+1] == valeur and not [x,y+1] in listMove:
                self.findrec(x,y+1,valeur,listMove) 
        
            
    def clean(self,listMove):
        for i in range(listMove.__len__()):
            self.tableau[listMove[i][0]][listMove[i][1]]=0      
              
                  
    def chutevertical(self):
        for x in range(self.colonnes):
            for y in range(self.lignes-1,0,-1):
                if (self.tableau[x][y] == 0):
                    j = y-1
                    while j>0 and self.tableau[x][j]==0 : 
                        j = j-1                                                                   
                    if (self.tableau[x][j]!=0):
                            self.tableau[x][y]=self.tableau[x][j]
                            self.tableau[x][j]=0            
                            
                       
    def chutehorizontal(self):
        for i in range(self.colonnes):
            if self.tableau[i][self.colonnes-1]==0:
                x = i
                while x<self.colonnes-1 and self.tableau[x][self.colonnes-1]==0 :
                    x = x+1 
                if (self.tableau[x][self.colonnes-1] != 0):
                    for y in range(self.lignes):
                        self.tableau[i][y] = self.tableau[x][y]
                        self.tableau[x][y] = 0
                        
        
                    
                            
                            
    def continuer(self):
        restants = 0
        for x in range(self.colonnes):
            for y in range(self.lignes):
                if (self.tableau[x][y] != 0):
                    valeur = self.tableau[x][y]
                    troisalasuite = 0
                    if x>0 and self.tableau[x-1][y] == valeur:
                        troisalasuite = troisalasuite + 1      
                    if x<self.colonnes-1 and self.tableau[x+1][y] == valeur :
                        troisalasuite = troisalasuite + 1    
                    if y>0 and self.tableau[x][y-1] == valeur :
                        troisalasuite = troisalasuite + 1                            
                    if y<self.lignes-1 and self.tableau[x][y+1] == valeur :
                        troisalasuite = troisalasuite + 1    
                    if (troisalasuite>=2):
                        restants = restants + 1
        return restants
    
    def continuerjoueur(self,couleurs):
        restants = 0
        for x in range(self.colonnes):
            for y in range(self.lignes):
                if (self.tableau[x][y] in couleurs):
                    valeur = self.tableau[x][y]
                    troisalasuite = 0
                    if x>0 and self.tableau[x-1][y] == valeur:
                        troisalasuite = troisalasuite + 1      
                    if x<self.colonnes-1 and self.tableau[x+1][y] == valeur :
                        troisalasuite = troisalasuite + 1    
                    if y>0 and self.tableau[x][y-1] == valeur :
                        troisalasuite = troisalasuite + 1                            
                    if y<self.lignes-1 and self.tableau[x][y+1] == valeur :
                        troisalasuite = troisalasuite + 1    
                    if (troisalasuite>=2):
                        restants = restants + 1
        return restants
                