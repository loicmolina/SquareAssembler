'''
Created on 6 mai 2018

@author: Loic
'''
import random
from random import randint

class tableau:
    
    def __init__(self):
        self.colonnes = 20
        self.lignes = 20
        self.tableau = [[random.randint(1,7) for x in range(self.colonnes)] for y in range(self.lignes)]

        
    def randomize(self):
        self.tableau = [[random.randint(1,7) for x in range(self.colonnes)] for y in range(self.lignes)]
