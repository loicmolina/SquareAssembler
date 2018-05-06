'''
Created on 6 mai 2018

@author: Loic
'''
import random
from random import randint
from Modele.dictionnaire import affectation

class tableau:
    
    
    
    def __init__(self):
        self.couleurs = affectation()
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
        
            
        
    def find(self,x,y,valeur,profondeur):
        if (valeur > 0):
            print(x,y)
            if self.tableau[x][y] == valeur and profondeur>0:
                self.tableau[x][y] = 0        
           
                if self.tableau[x-1][y] == valeur:
                    self.find(x-1,y,valeur,profondeur+1) 
            if x<self.lignes-1 :
                if self.tableau[x+1][y] == valeur:
                    self.find(x+1,y,valeur,profondeur+1) 
            if y>0 :
                if self.tableau[x][y-1] == valeur:
                    self.find(x,y-1,valeur,profondeur+1) 
            if y<self.colonnes-1 :
                if self.tableau[x][y+1] == valeur:
                    self.find(x,y+1,valeur,profondeur+1)  
            
                  
                  
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
        for y in range(self.lignes):
                for x in range(self.colonnes):
                    if (self.tableau[x][y] == 0 and x<self.colonnes-1):
                        j = x+1
                        while j<self.colonnes-1 and self.tableau[j][y]==0 :                             
                            print(j,y)
                            j = j+1                                                                   
                        if (self.tableau[j][y]!=0):
                                self.tableau[x][y]=self.tableau[j][y]
                                self.tableau[j][y]=0                         