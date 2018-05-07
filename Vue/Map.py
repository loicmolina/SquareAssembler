'''
Created on 6 mai 2018

@author: Loic
'''
from tkinter import *
from Modele.Tableau import tableau
from Modele.Dictionnaire import Affectation
from _ctypes import alignment
from tkinter.constants import CENTER

                   
#Fonctions

def drawTable():  
    global canvasGame
    global tab  
    global couleurs  
    for i in range(tab.colonnes ):
        for j in range(tab.lignes ):            
            canvasGame.create_rectangle(1+i* taillecase, 1+j * taillecase,2+ (i+1)* taillecase,2+ (j+1) * taillecase , fill = couleurs.couleur(tab.tableau[i][j]))


def newTable(nb,popup):   
    global taille     
    global taillecase
    canvasGame.delete("all")
    tab.resize(nb) 
    taillecase =  taille/nb
    drawTable()
    scoring.config(text=tab.score)
    popup.destroy()
    

def cliqueGauche(event):    
    x = int(event.x/taillecase)
    y = int(event.y/taillecase)  
    tour(x, y)  
   
    
def tour(x,y):
    global scoring
    tab.find(x,y,tab.tableau[x][y])
    
    tab.chutevertical()
    tab.chutehorizontal()
    drawTable()
    
    restant = tab.continuer()
    scoring.config(text=tab.score)
    if restant == 0:
        fin()
        
        
def fin():
    popup = Toplevel()
    popup.title("")
    popup.geometry("200x50+200+200")
    labelFin=Label(popup, text="Partie Terminée")
    labelFin.pack()
    popup.mainloop()

        
def selectionsize():    
    popup = Toplevel()
    popup.title("Nouveau")
    popup.geometry("40x40+200+200")
    bouton10=Button(popup, text="10 Cases", command= lambda:newTable(10,popup))
    bouton10.pack(side =LEFT)
    bouton20=Button(popup, text="20 Cases", command= lambda:newTable(20,popup))
    bouton20.pack(side =RIGHT)
    popup.mainloop()
    

#Instanciations

fenetre = Tk()
fenetre.title("Square Assembler")
fenetre.geometry("800x600+200+200")

tab = tableau()
taille = 600
taillecase = taille / tab.lignes

couleurs = Affectation()

canvasScore = Canvas(fenetre,width = 200, height = tab.lignes * taillecase, background = "white")
canvasGame = Canvas(fenetre,width = tab.colonnes * taillecase, height = tab.lignes * taillecase, background = "white")

canvasScore.pack(side=LEFT)
canvasGame.pack(side=RIGHT)
            

#Créations des menus

scoring = Label(canvasScore,text=tab.score,font=("Impact",30))
scoring.pack(anchor=CENTER)

menubar = Menu(fenetre)
fenetre.config(menu = menubar)

menufichier = Menu(menubar,tearoff = 0)
menuanonymat = Menu(menubar,tearoff = 0)

menubar.add_cascade(label="Jeu", menu=menufichier)

menufichier.add_command(label="Nouveau", command = selectionsize)
menufichier.add_command(label="Quitter", command=fenetre.destroy )

menubar.add_cascade(label="Numeros d'anonymat", menu=menuanonymat)
menuanonymat.add_command(label="Molina Loïc")
menuanonymat.add_command(label="Mattei Zav")


canvasGame.bind("<Button-1>", cliqueGauche)


#Création du tableau

    
drawTable()       

fenetre.mainloop()



