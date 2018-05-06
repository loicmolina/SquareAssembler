'''
Created on 6 mai 2018

@author: Loic
'''

class affectation:
    def __init__(self):
        self.valeurs = {}
        self.valeurs[1]="red"
        self.valeurs[2]="blue"
        self.valeurs[3]="green"
        self.valeurs[4]="yellow"
        self.valeurs[5]="purple"
        self.valeurs[6]="cyan"
        self.valeurs[7]="pink"
        
    def couleur(self,i):   
        return self.valeurs[i]