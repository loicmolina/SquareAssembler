'''
Created on 6 mai 2018

@author: Loic
'''
from tkinter import *
from Modele.Jeu import Jeu
import time
from Ivy.Connect import connection


#Fonctions
class Vue:
    def __init__(self):
            
        #Instanciations
            #fenetre
        self.fenetre = Tk()
        self.fenetre.title("Square Assembler")
        self.fenetre.resizable(False, False)
        self.fenetre.geometry("800x600+200+200")
        
            #Modele   
        self.nbpartie = 0        
        self.jeu = Jeu(1,10)
        
            #Canvas
        self.canvasScore = Canvas(self.fenetre,width = 180, height = self.jeu.tab.lignes * self.jeu.taillecase, bg = "black")
        self.canvasGame = Canvas(self.fenetre,width = self.jeu.tab.colonnes * self.jeu.taillecase, height = self.jeu.tab.lignes * self.jeu.taillecase, bg = "white")
        
        self.canvasGame.bind("<Button-1>", self.cliqueGauche)
        
        self.canvasScore.config(highlightbackground="Black")
        
        
        self.canvasGame.pack(side=RIGHT)
        self.canvasScore.pack(side=TOP,ipady = 100,ipadx = 100)
        
        #Créations des labels
        
        self.titre = Label(self.canvasScore,text="SQUARE\n\nASSEMBLER",font=("Impact",26,"bold"),bg="black",fg="white")
        self.titre.pack(side=TOP,ipady = 100)
        
        self.labeltimeleft = Label(self.canvasScore,text=self.jeu.tempsTour ,font=("Impact",30),bg="black",fg="black")
        self.labeltimeleft.pack(side=TOP)
        
        self.labelplayer1 = Label(self.canvasScore,text=self.jeu.joueur1.nom+'-',font=("Impact",20),bg="black",fg="black")
        self.scoring1 = Label(self.canvasScore,text=self.jeu.joueur1.score,font=("Impact",20),bg="black",fg="black")
        
        self.labelplayer1.pack(side=LEFT)
        self.scoring1.pack(side=LEFT)
        
        self.labelplayer2 = Label(self.canvasScore,text=self.jeu.joueur2.nom+'-',font=("Impact",20),bg="black",fg="black")
        self.scoring2 = Label(self.canvasScore,text=self.jeu.joueur2.score,font=("Impact",20),bg="black",fg="black")
        
        self.scoring2.pack(side=RIGHT)
        self.labelplayer2.pack(side=RIGHT)
        
        
        
        #Créations des menus
        
        self.menubar = Menu(self.fenetre)
        self.fenetre.config(menu = self.menubar)
        
        self.menufichier = Menu(self.menubar,tearoff = 0)
        self.menuanonymat = Menu(self.menubar,tearoff = 0)
        
        self.menubar.add_cascade(label="Jeu", menu=self.menufichier)
        
        self.menufichier.add_command(label="Nouveau", command = self.selectionsize)
        self.menufichier.add_command(label="Rejoindre", command=self.joinRoom)
        self.menufichier.add_command(label="Quitter", command=self.stop )
        
        self.menubar.add_cascade(label="A propos", menu=self.menuanonymat)
        self.menuanonymat.add_cascade(label="17820046")
        self.menuanonymat.add_cascade(label="17820047")
        
        
    
        self.c = connection(self)
    
    
    def drawTable(self):  
        self.canvasGame.delete("all")
        for i in range(self.jeu.tab.colonnes ):
            for j in range(self.jeu.tab.lignes ):            
                self.canvasGame.create_rectangle(1+i* self.jeu.taillecase, 1+j * self.jeu.taillecase,2+ (i+1)* self.jeu.taillecase,2+ (j+1) * self.jeu.taillecase , fill = self.jeu.couleurs.couleur(self.jeu.tab.tableau[i][j]))
    
    
    def drawColors(self):
        self.canvasScore.delete("all")
        if (self.jeu.nbjoueurs == 2):
            for i in range(self.jeu.joueur1.couleurs.__len__()):
                self.canvasScore.create_rectangle(10,460-i*10+1,40,460-(i+1)*10, fill =self.jeu.couleurs.couleur(self.jeu.joueur1.couleurs[i])) 
            
            for i in range(self.jeu.joueur2.couleurs.__len__()):
                self.canvasScore.create_rectangle(145,460-i*10+1,175,460-(i+1)*10, fill = self.jeu.couleurs.couleur(self.jeu.joueur2.couleurs[i])) 
                
            if (self.jeu.gameover >= 0):
                for i in range(1,int(self.jeu.tab.colonnes/2.5)+1):
                    if (i not in self.jeu.joueur1.couleurs and i not in self.jeu.joueur2.couleurs):
                        if (i%2 == 0):
                            self.canvasScore.create_rectangle(78,460-(i-1)*5+1,98,460-i*5, fill = self.jeu.couleurs.valeurs[i]) 
                        else:
                            self.canvasScore.create_rectangle(99,460-i*5+1,119,460-(i+1)*5, fill = self.jeu.couleurs.valeurs[i]) 
                    
            
    
    def drawWaitingForPlayer2(self):
        self.canvasGame.create_rectangle(100,200,500,400,fill="black")
        self.canvasGame.create_text(300,250,font=("Impact",30,"bold"),text="Recherche du Joueur 2",fill="white")      
        self.canvasGame.create_text(300,350,font=("Impact",30,"bold"),text="En attente...",fill="white")
        
        
    def drawWaitingForPlayer1(self):
        self.canvasGame.create_rectangle(100,200,500,400,fill="black")
        self.canvasGame.create_text(300,250,font=("Impact",30,"bold"),text="Recherche du Joueur 1",fill="white")      
        self.canvasGame.create_text(300,350,font=("Impact",30,"bold"),text="En attente...",fill="white")
    
    def start(self,nbCases,nbJoueurs,tempsTour,popup):  
        try:
            tps = int(tempsTour)
        except:
            tps = 0
        
        if (nbCases != "" and nbJoueurs != "" and (nbJoueurs=="1" or tps>2)):     
            
            self.jeu = Jeu(int(nbJoueurs),tps)   
            self.jeu.newTable(int(nbCases))
            self.nbpartie = self.nbpartie +1                    
            
            if (self.jeu.nbjoueurs==2):      
                self.createRoom()                    
                
                self.labelplayer1.config(text = '>'+self.jeu.joueur1.nom+'-',fg="white")
                self.labelplayer2.config(text = self.jeu.joueur2.nom+'-',fg="white")
                
                self.scoring1.config(text = self.jeu.joueur1.score,fg="white")
                self.scoring2.config(text = self.jeu.joueur2.score,fg="white")   
                
                if self.c.IVYAPPNAME == 'Host':                     
                    self.labelplayer2.config(fg="grey")            
                    self.scoring2.config(fg="grey")
                         
                
                self.labeltimeleft.config(fg="white",text=tempsTour)
            else:
                self.closeRoom()
                
                     
                self.labelplayer1.config(text = '>'+self.jeu.joueur1.nom+'-',fg="white")
                self.labelplayer2.config(fg= "black")
                
                self.labeltimeleft.config(fg="black")
                
                self.scoring1.config(text = self.jeu.joueur1.score,fg="white")
                self.scoring2.config(fg= "black")
                self.render()
            
            popup.destroy()
            
            
    
    def cliqueGauche(self,event):   
        if (self.jeu.gameover == 0 and (self.jeu.nbjoueurs==1 or((self.c.IVYAPPNAME == 'Guest' and self.jeu.joueurTour==self.jeu.joueur2) or (self.c.IVYAPPNAME == 'Host' and self.jeu.joueurTour==self.jeu.joueur1)))):
            x = int(event.x/self.jeu.taillecase)
            y = int(event.y/self.jeu.taillecase) 
            if (self.jeu.nbjoueurs == 2):
                self.c.sendmsg("coup:"+str(x)+","+str(y)) 
            self.jeu.tour(x, y)   
            self.drawTable() 
            self.drawColors()    
            self.updatescoreboard()  
        if self.jeu.gameover == 1 :
            self.fin()
    
    
    
    def updatescoreboard(self):
        self.scoring1.config(text = self.jeu.joueur1.score) 
        if self.jeu.joueurTour == self.jeu.joueur1:
            self.labelplayer1.config(text = '>'+self.jeu.joueur1.nom+'-')
            self.labelplayer2.config(text = self.jeu.joueur2.nom+'-')
        else:
            self.labelplayer2.config(text = '>'+self.jeu.joueur2.nom+'-')
            self.labelplayer1.config(text = self.jeu.joueur1.nom+'-')
         
        if(self.jeu.nbjoueurs == 2):
            self.scoring2.config(text = self.jeu.joueur2.score)
            self.labeltimeleft.config(text=self.jeu.tempsTour)
            
            
            
    def horloge(self,idpartie):
        self.fenetre.after(1000, lambda: self.decrementetemps(idpartie))
        
        
    #fonction de mise à jour de l'affichage pour le joueur qui ne joue pas actuellement    
    def render(self):    
        self.drawTable()
        self.drawColors()
        if (self.jeu.gameover==1 ):
            self.fin()
    
    
    def decrementetemps(self,idpartie):  
        if (idpartie == self.nbpartie):
            self.horloge(idpartie)    
            self.jeu.tempsTour -= 1       
            if (self.jeu.tempsTour == 0):
                self.jeu.conditionsfin()
                self.jeu.tempsTour = self.jeu.tempsTourMax
            
            self.updatescoreboard()
        
            
    def fin(self):
        self.nbpartie += 1
        self.canvasGame.create_rectangle(100,200,500,400,fill="black")
        self.canvasGame.create_text(300,250,font=("Impact",35,"bold"),text="Partie Terminée",fill="white")
        if (self.jeu.nbjoueurs == 1):        
            self.canvasGame.create_text(300,350,font=("Impact",30,"bold"),text="Score final : "+ str(self.jeu.joueur1.score),fill="white")
        else:
            if (self.jeu.joueur1.score > self.jeu.joueur2.score):
                self.canvasGame.create_text(300,310,font=("Impact",30,"bold"),text="Gagnant : "+self.jeu.joueur1.nom,fill="white")
            else:
                if (self.jeu.joueur1.score < self.jeu.joueur2.score):                
                    self.canvasGame.create_text(300,310,font=("Impact",30,"bold"),text="Gagnant : "+self.jeu.joueur2.nom,fill="white")
                else:                
                    self.canvasGame.create_text(300,310,font=("Impact",30,"bold"),text="Egalité",fill="white")
            self.canvasGame.create_text(300,360,font=("Impact",30,"bold"),text="Score final : "+str(self.jeu.joueur1.score)+" à "+str(self.jeu.joueur2.score),fill="white")
    
    
            
    def selectionsize(self):    
        popup = Toplevel()
        popup.title("Nouveau")
        popup.geometry("380x330+200+200")
        
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
        
        labelTemps = Label(popup,text="Temps pour chaque tour (en sec) :\n(Mode 2 Joueurs, Supérieur à 2sec)")
        labelTemps.grid(row=3,column=1)
        entryTemps = Entry(popup)
        entryTemps.grid(row=4,column=1)
    
        valider=Button(popup, text="Valider", command= lambda:self.start(varTaille.get(),varJoueurs.get(),entryTemps.get(),popup))
        valider.grid(row=5,column = 1,pady=10,ipadx=25,ipady=15)
        popup.mainloop()
        
        
    def stop(self):
        self.c.stop()
        self.fenetre.destroy()    
        
        
    def player2ready(self): 
        self.jeu.gameover = 0
        self.drawColors()
        self.horloge(self.nbpartie)
        
        
    def player1ready(self):        
        self.jeu.nbjoueurs = 2
        self.nbpartie = self.nbpartie +1    
        
        self.labelplayer1.config(text = '>'+self.jeu.joueur1.nom+'-',fg="white")
        self.labelplayer2.config(text = self.jeu.joueur2.nom+'-',fg="white")

        
        self.scoring1.config(text = self.jeu.joueur1.score,fg="white")
        self.scoring2.config(text = self.jeu.joueur2.score,fg="white")                 
        
        
        if self.c.IVYAPPNAME == 'Guest':                     
            self.labelplayer1.config(fg="grey")            
            self.scoring1.config(fg="grey")
        
        self.updatescoreboard()
        self.render()
        
        self.labeltimeleft.config(fg="white")    
        
        self.horloge(self.nbpartie)
                
        
    def joinRoom(self):   
        self.closeRoom()      
        self.c = connection(self)
        self.c.runJoin()  
        self.drawWaitingForPlayer1()
        
    
    def createRoom(self):    
        self.closeRoom()      
        self.c = connection(self)
        self.c.runHost(self) 
        self.drawWaitingForPlayer2()
        
        
    def closeRoom(self):
        self.c.stop()
        
    
vue = Vue()
vue.fenetre.mainloop()

