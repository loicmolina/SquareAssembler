'''
Created on 6 mai 2018

@author: Loic
'''
from Modele.Tableau import tableau
tab = tableau()
tab.randomize()

for i in range(20):
    print("")
    for j in range(20):
        print(tab.tableau[i][j],end='')
        
   