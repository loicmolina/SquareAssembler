'''
Created on 6 mai 2018

@author: Loic
'''
from tkinter import *
from Modele.Tableau import tableau
from Modele.dictionnaire import affectation

'''
    Instanciations
'''

taillecase = 30
tab = tableau()
couleurs = affectation()

fenetre= Tk()

'''
    Fonctions

'''


def drawTable():    
    for i in range(tab.colonnes ):
        for j in range(tab.lignes ):
            canvas.create_rectangle(i* taillecase, j * taillecase, (i+1)* taillecase, (j+1) * taillecase, fill = couleurs.couleur(tab.tableau[i][j]))

def newTable():
    tab.randomize()
    drawTable()

'''
    Ajout du menu
'''


menubar = Menu(fenetre)
fenetre.config(menu = menubar)

menufichier = Menu(menubar,tearoff = 0)
menubar.add_cascade(label="Jeu", menu=menufichier)
menufichier.add_command(label="Nouveau",command= newTable)
menufichier.add_command(label="Quitter", command=fenetre.destroy )


menuanonymat = Menu(menubar,tearoff = 0)
menubar.add_cascade(label="Numeros d'anonymat", menu=menuanonymat)
menuanonymat.add_command(label="Molina Loïc")
menuanonymat.add_command(label="Mattei Zav")

'''
    Création du tableau
'''



canvas = Canvas(fenetre,width = tab.colonnes * taillecase, height = tab.lignes * taillecase, background = "white")

drawTable()       

canvas.pack()
fenetre.mainloop()
