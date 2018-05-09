'''
Created on 6 mai 2018

@author: Loic
'''
from tkinter import *
from Modele.Jeu import Jeu

                   
#Fonctions

def drawTable():  
    global canvasGame
    for i in range(jeu.tab.colonnes ):
        for j in range(jeu.tab.lignes ):            
            canvasGame.create_rectangle(1+i* jeu.taillecase, 1+j * jeu.taillecase,2+ (i+1)* jeu.taillecase,2+ (j+1) * jeu.taillecase , fill = jeu.couleurs.couleur(jeu.tab.tableau[i][j]))


def start(nbCases,nbJoueurs,popup):  
    if ((nbCases == 10 or nbCases == 20) and (nbJoueurs == 1 or nbJoueurs == 2)):
        global jeu
        jeu = Jeu(nbJoueurs)    
        jeu.newTable(nbCases)  
        
        labelplayer1.config(text = '>'+jeu.joueur1.nom)
        labelplayer2.config(text = jeu.joueur2.nom)
        
        scoring1.config(text = jeu.joueur1.score)
        scoring2.config(text = jeu.joueur2.score)
        
        
        canvasGame.delete("all")
        popup.destroy()
        drawTable()
    

def cliqueGauche(event):   
    x = int(event.x/jeu.taillecase)
    y = int(event.y/jeu.taillecase)  
    jeu.tour(x, y)   
    drawTable() 
    updatescores()      
    if jeu.gameover == 1 :
        fin()
            

def updatescores():
    global scoring1
    scoring1.config(text = jeu.joueur1.score) 
    if jeu.joueurTour == jeu.joueur1:
        labelplayer1.config(text = '>'+jeu.joueur1.nom)
        labelplayer2.config(text = jeu.joueur2.nom)
    else:
        labelplayer2.config(text = '>'+jeu.joueur2.nom)
        labelplayer1.config(text = jeu.joueur1.nom)
     
    if(jeu.nbjoueurs == 2):
        global scoring2
        scoring2.config(text = jeu.joueur2.score)  

        
def fin():
    popup = Toplevel()
    popup.title("")
    popup.config(bg="red")
    popup.geometry("200x50+400+400")
    labelFin=Label(popup, bg="red",fg="black",font=("Impact",15),text="Partie Terminée")
    labelFin.pack()
    popup.mainloop()

        
def selectionsize():    
    popup = Toplevel()
    popup.title("Nouveau")
    popup.geometry("350x270+200+200")
    
    texte = Label(popup,text="Choix des détails de la partie")
    texte.grid(row=0,column = 1,pady=10)
    
    varTaille = StringVar()
    varJoueurs = StringVar()
    
    bouton10=Radiobutton(popup,indicatoron=0, variable = varTaille,value = 10 ,text="10 Cases")
    bouton10.grid(row=1,column = 0,pady=10,ipadx=20,ipady=20)
    bouton20=Radiobutton(popup,indicatoron=0, variable = varTaille,value = 20 , text="20 Cases")
    bouton20.grid(row=1,column = 2,pady=10,ipadx=20,ipady=20)
    
    
    
    bouton1p=Radiobutton(popup,indicatoron=0, variable = varJoueurs ,value = 1 , text="1 Joueur ")
    bouton1p.grid(row=2,column = 0,pady=10,ipadx=20,ipady=20)
    bouton2p=Radiobutton(popup,indicatoron=0, variable = varJoueurs ,value = 2, text="2 Joueurs")
    bouton2p.grid(row=2,column = 2,pady=10,ipadx=20,ipady=20)
    
     
    valider=Button(popup, text="Valider", command= lambda:start(int(varTaille.get()),int(varJoueurs.get()),popup))
    valider.grid(row=3,column = 1,pady=10,ipadx=25,ipady=15)
    popup.mainloop()
    

#Instanciations
    #fenetre
fenetre = Tk()
fenetre.title("Square Assembler")
fenetre.resizable(False, False)
fenetre.geometry("800x600+200+200")

    #Modele   
jeu = Jeu(2)
taille = 600
taillecase = taille / jeu.tab.lignes

    
    #Canvas
canvasScore = Canvas(fenetre,width = 180, height = jeu.tab.lignes * taillecase, bg = "black")
canvasGame = Canvas(fenetre,width = jeu.tab.colonnes * taillecase, height = jeu.tab.lignes * taillecase, bg = "black")

canvasGame.bind("<Button-1>", cliqueGauche)

canvasScore.place(anchor=CENTER)
canvasScore.config(highlightbackground="Black")

canvasScore.pack(ipadx=10,side=LEFT)
canvasGame.pack(side=RIGHT)

    #variable de fin
restants = 100

#Créations des menus

titre = Label(canvasScore,text="SQUARE\n\nASSEMBLER",font=("Impact",26,"bold"),bg="black",fg="white")
titre.pack(side=TOP,ipady = 120)

labelplayer1 = Label(canvasScore,text=jeu.joueur1.nom,font=("Impact",20),bg="black",fg="white")
scoring1 = Label(canvasScore,text=jeu.joueur1.score,font=("Impact",20),bg="black",fg="white")

if(jeu.nbjoueurs == 2):
    labelplayer1.pack(side=LEFT,ipady = 90)
    scoring1.pack(side=LEFT,ipady = 90)
    
    labelplayer2 = Label(canvasScore,text=jeu.joueur2.nom,font=("Impact",20),bg="black",fg="white")
    scoring2 = Label(canvasScore,text=jeu.joueur2.score,font=("Impact",20),bg="black",fg="white")

    scoring2.pack(side=RIGHT,ipady = 90)
    labelplayer2.pack(side=RIGHT,ipady = 90)
else:
    scoring1.pack(side=BOTTOM,ipady = 80)
    


menubar = Menu(fenetre)
fenetre.config(menu = menubar)

menufichier = Menu(menubar,tearoff = 0)
menuanonymat = Menu(menubar,tearoff = 0)

menubar.add_cascade(label="Jeu", menu=menufichier)

menufichier.add_command(label="Nouveau", command = selectionsize)
menufichier.add_command(label="Quitter", command=fenetre.destroy )

menubar.add_cascade(label="Numeros d'anonymat", menu=menuanonymat)
menuanonymat.add_cascade(label="17820046")
menuanonymat.add_cascade(label="17820047")


#Affichage de la fenêtre
      

fenetre.mainloop()
