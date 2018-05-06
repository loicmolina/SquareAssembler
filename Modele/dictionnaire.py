'''
Created on 6 mai 2018

@author: Loic
'''

class affectation:
    def __init__(self):
        self.valeurs = {}
        self.valeurs[0]="white"
        self.valeurs[1]="red"
        self.valeurs[2]="blue"
        self.valeurs[3]="green"
        self.valeurs[4]="yellow"
        self.valeurs[5]="purple"
        self.valeurs[6]="cyan"
        self.valeurs[7]="pink"
        self.valeurs[8]="orange"        
        
        self.nbmax = {}
        self.nbmax[1]=50
        self.nbmax[2]=50
        self.nbmax[3]=50
        self.nbmax[4]=50
        self.nbmax[5]=50
        self.nbmax[6]=50
        self.nbmax[7]=50
        self.nbmax[8]=50
        
        
    def couleur(self, i): 
        return self.valeurs[i] 
    
        
    def couleurs(self): 
        liste = []
        for i in range(1,9):
            if self.nbmax[i] > 0:
                liste.append(i)
        return liste
                
                
    def select(self, liste, i):
        self.nbmax[liste[i]] = self.nbmax[liste[i]] -1
        return liste[i]
    
    
    def setnbmax(self,nbcases):
        if nbcases == 20:   
            self.nbmax[1]=50
            self.nbmax[2]=50
            self.nbmax[3]=50
            self.nbmax[4]=50
            self.nbmax[5]=50
            self.nbmax[6]=50
            self.nbmax[7]=50
            self.nbmax[8]=50
        else:            
            self.nbmax[1]=25
            self.nbmax[2]=25
            self.nbmax[3]=25
            self.nbmax[4]=25
            self.nbmax[5]=0
            self.nbmax[6]=0
            self.nbmax[7]=0
            self.nbmax[8]=0
            
