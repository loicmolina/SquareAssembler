'''
Created on 6 mai 2018

@author: Loic
'''
from tkinter import *
from Modele.Jeu import Jeu
import time


#Fonctions

def drawTable():  
    global canvasGame
    for i in range(jeu.tab.colonnes ):
        for j in range(jeu.tab.lignes ):            
            canvasGame.create_rectangle(1+i* jeu.taillecase, 1+j * jeu.taillecase,2+ (i+1)* jeu.taillecase,2+ (j+1) * jeu.taillecase , fill = jeu.couleurs.couleur(jeu.tab.tableau[i][j]))


def drawColors():
    global canvasScore
    for i in range(jeu.joueur1.couleurs.__len__()):
        canvasScore.create_rectangle(10,450+i*20+1,50,450+(i+1)*20, fill =jeu.couleurs.couleur(jeu.joueur1.couleurs[i])) 
    
    for i in range(jeu.joueur2.couleurs.__len__()):
        canvasScore.create_rectangle(145,450+i*20+1,185,450+(i+1)*20, fill =jeu.couleurs.couleur(jeu.joueur2.couleurs[i])) 
        

def start(nbCases,nbJoueurs,popup):  
    
    if (nbCases != "" and nbJoueurs != ""):
        global jeu
        global canvasScore
        global nbpartie        
        
        jeu = Jeu(int(nbJoueurs))   
        jeu.newTable(int(nbCases))
        nbpartie = nbpartie +1
        
        canvasScore.delete("all")
        
        if (jeu.nbjoueurs==2):
            labelplayer1.config(text = '>'+jeu.joueur1.nom+'-',fg="white")
            labelplayer2.config(text = jeu.joueur2.nom+'-',fg="white")
            
            scoring1.config(text = jeu.joueur1.score,fg="white")
            scoring2.config(text = jeu.joueur2.score,fg="white")            
            
            labeltimeleft.config(fg="white")

            horloge(nbpartie)
        else:
            labelplayer1.config(text = '>'+jeu.joueur1.nom+'-',fg="white")
            labelplayer2.config(fg= "black")
            
            labeltimeleft.config(fg="black")
            
            scoring1.config(text = jeu.joueur1.score,fg="white")
            scoring2.config(fg= "black")
        
        
        canvasGame.delete("all")
        popup.destroy()
        updatescoreboard()
        drawTable()
        
        

def cliqueGauche(event):   
    if (jeu.gameover == 0):
        x = int(event.x/jeu.taillecase)
        y = int(event.y/jeu.taillecase)  
        jeu.tour(x, y)   
        drawTable() 
        updatescoreboard() 
        drawColors()     
        if jeu.gameover == 1 :
            fin()
            


def updatescoreboard():
    global scoring1
    global scoring2
    global labelplayer1
    global labelplayer2
    scoring1.config(text = jeu.joueur1.score) 
    if jeu.joueurTour == jeu.joueur1:
        labelplayer1.config(text = '>'+jeu.joueur1.nom+'-')
        labelplayer2.config(text = jeu.joueur2.nom+'-')
    else:
        labelplayer2.config(text = '>'+jeu.joueur2.nom+'-')
        labelplayer1.config(text = jeu.joueur1.nom+'-')
     
    if(jeu.nbjoueurs == 2):
        global scoring2
        global labeltimeleft
        scoring2.config(text = jeu.joueur2.score)
        labeltimeleft.config(text=jeu.tempsTour)
        
        
def horloge(idpartie):
    fenetre.after(1000, lambda: decrementetemps(idpartie))


def decrementetemps(idpartie):  
    if (idpartie == nbpartie):
        horloge(idpartie)    
        jeu.tempsTour = jeu.tempsTour - 1        
        if (jeu.tempsTour == 0):
            jeu.conditionsfin()
            jeu.tempsTour = jeu.tempsTourMax
        
        updatescoreboard()
    
        
def fin():
    global canvasGame
    canvasGame.create_rectangle(100,200,500,400,fill="black")
    canvasGame.create_text(300,250,font=("Impact",35,"bold"),text="Partie Terminée",fill="white")
    if (jeu.nbjoueurs == 1):        
        canvasGame.create_text(300,350,font=("Impact",30,"bold"),text="Score final : "+ str(jeu.joueur1.score),fill="white")
    else:
        if (jeu.joueur1.score > jeu.joueur2.score):
            canvasGame.create_text(300,310,font=("Impact",30,"bold"),text="Gagnant : "+jeu.joueur1.nom,fill="white")
        else:
            if (jeu.joueur1.score < jeu.joueur2.score):                
                canvasGame.create_text(300,310,font=("Impact",30,"bold"),text="Gagnant : "+jeu.joueur2.nom,fill="white")
            else:                
                canvasGame.create_text(300,310,font=("Impact",30,"bold"),text="Egalité",fill="white")
        canvasGame.create_text(300,360,font=("Impact",30,"bold"),text="Score final : "+str(jeu.joueur1.score)+" à "+str(jeu.joueur2.score),fill="white")


        
def selectionsize():    
    popup = Toplevel()
    popup.title("Nouveau")
    popup.geometry("350x270+200+200")
    
    texte = Label(popup,text="Choix des détails de la partie")
    texte.grid(row=0,column = 1,pady=10)
    
    varTaille = StringVar()
    varJoueurs = StringVar()
    #varTemps = IntVar()
    
    bouton10=Radiobutton(popup,indicatoron=0, variable = varTaille,value = 10 ,text="10 Cases")
    bouton10.grid(row=1,column = 0,pady=10,ipadx=20,ipady=20)
    bouton20=Radiobutton(popup,indicatoron=0, variable = varTaille,value = 20 , text="20 Cases")
    bouton20.grid(row=1,column = 2,pady=10,ipadx=20,ipady=20)    
    
    
    bouton1p=Radiobutton(popup,indicatoron=0, variable = varJoueurs ,value = 1 , text="1 Joueur ")
    bouton1p.grid(row=2,column = 0,pady=10,ipadx=20,ipady=20)
    bouton2p=Radiobutton(popup,indicatoron=0, variable = varJoueurs ,value = 2, text="2 Joueurs")
    bouton2p.grid(row=2,column = 2,pady=10,ipadx=20,ipady=20)
    

    valider=Button(popup, text="Valider", command= lambda:start(varTaille.get(),varJoueurs.get(),popup))
    valider.grid(row=3,column = 1,pady=10,ipadx=25,ipady=15)
    popup.mainloop()
    
    

#Instanciations
    #fenetre
fenetre = Tk()
fenetre.title("Square Assembler")
fenetre.resizable(False, False)
fenetre.geometry("800x600+200+200")

    #Modele   
nbpartie = 0

jeu = Jeu(2)
    
    #Canvas
canvasScore = Canvas(fenetre,width = 180, height = jeu.tab.lignes * jeu.taillecase, bg = "black")
canvasGame = Canvas(fenetre,width = jeu.tab.colonnes * jeu.taillecase, height = jeu.tab.lignes * jeu.taillecase, bg = "white")

canvasGame.bind("<Button-1>", cliqueGauche)

canvasScore.place()
canvasScore.config(highlightbackground="Black")


canvasGame.pack(side=RIGHT)
canvasScore.pack(side=TOP,ipady = 100,ipadx = 100)

#Créations des labels

titre = Label(canvasScore,text="SQUARE\n\nASSEMBLER",font=("Impact",26,"bold"),bg="black",fg="white")
titre.pack(side=TOP,ipady = 100)

labeltimeleft = Label(canvasScore,text=jeu.tempsTour ,font=("Impact",30),bg="black",fg="black")
labeltimeleft.pack(side=TOP)

labelplayer1 = Label(canvasScore,text=jeu.joueur1.nom+'-',font=("Impact",20),bg="black",fg="black")
scoring1 = Label(canvasScore,text=jeu.joueur1.score,font=("Impact",20),bg="black",fg="black")

labelplayer1.pack(side=LEFT)
scoring1.pack(side=LEFT)

labelplayer2 = Label(canvasScore,text=jeu.joueur2.nom+'-',font=("Impact",20),bg="black",fg="black")
scoring2 = Label(canvasScore,text=jeu.joueur2.score,font=("Impact",20),bg="black",fg="black")

scoring2.pack(side=RIGHT)
labelplayer2.pack(side=RIGHT)



#Créations des menus

menubar = Menu(fenetre)
fenetre.config(menu = menubar)

menufichier = Menu(menubar,tearoff = 0)
menuanonymat = Menu(menubar,tearoff = 0)

menubar.add_cascade(label="Jeu", menu=menufichier)

menufichier.add_command(label="Nouveau", command = selectionsize)
menufichier.add_command(label="Quitter", command=fenetre.destroy )

menubar.add_cascade(label="A propos", menu=menuanonymat)
menuanonymat.add_cascade(label="17820046")
menuanonymat.add_cascade(label="17820047")


#Affichage de la fenêtre

fenetre.mainloop()


