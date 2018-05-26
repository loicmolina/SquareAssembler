#!/usr/bin/env python
"""An ivyprobe script for ivy-python
"""
import os
import signal
import sys
sys.path.append("D:\Programmes\ivy-python-3.1")
from ivy.std_api import *

# The next line taken from https://pythonhosted.org/six/
# Copyright (c) 2010-2016 Benjamin Peterson
class connection:
    
    def __init__(self,partie):    
        self.IVYAPPNAME = ""
        self.game = partie  
        self.matefound=False
        self.on_die_accepted = False
    
    def setmodele(self,partie):
        self.game=partie

    def info(self,fmt, *arg):
        1
        #print(fmt % arg)
        
        
    def sendDataToGuest(self):
        self.sendmsg("size:"+str(self.game.jeu.tab.colonnes))
        self.sendmsg("tab:"+str(self.game.jeu.tab.tableau))
        self.sendmsg("time:"+str(self.game.jeu.tempsTourMax))
    
    def on_connection_change(self,agent, event):
        if event == IvyApplicationDisconnected:
            self.info('Ivy application %r has disconnected', agent)
            if (IvyGetApplicationList().__len__()==0):
                self.game.fin()
        else:
            self.info('Ivy application %r has connected', agent)
            if (IvyGetApplicationList().__len__()==1 and self.IVYAPPNAME == 'Host'):
                self.sendmsg("nom:"+self.IVYAPPNAME)
                
                
        #print("il y a ",IvyGetApplicationList().__len__()," dans le bus")
        self.info('Ivy applications currently on the bus: %s',','.join(IvyGetApplicationList()))
    
    
    def on_die(self,agent, _id):
        self.info('Received the order to die from %r with id = %d', agent, _id)
        self.on_die_accepted = True
        # will interrupt the raw_input()/input() in the main loop, below
        os.kill(os.getpid(), signal.SIGINT)
        
        
    
    def on_msg(self,agent, *arg):
        self.info('Received from %r: %s', agent, arg and str(arg) or '<no args>')        
        if ("size:" in str(arg) and self.IVYAPPNAME == 'Guest'):
            #print("size reçu : "+str(arg)[7:-3])
            self.game.jeu.newTable(int(str(arg)[7:-3]))
            
        elif "nom:" in str(arg): 
            if self.IVYAPPNAME == 'Guest':
                #print("tab reçu : "+str(arg)[8:-5])    
                if (str(arg)[6:-3] == "Host"):
                    self.matefound = True
                    self.sendmsg("nom:"+self.IVYAPPNAME)  
                    self.game.player1ready()
                    
            if self.IVYAPPNAME == 'Host':
                #print("tab reçu : "+str(arg)[8:-5])    
                if (str(arg)[6:-3] == "Guest"):
                    self.matefound = True
                    self.sendDataToGuest()
                    self.game.render()
                    self.game.updatescoreboard()
                    self.game.player2ready() 
                    
        elif ("tab:" in str(arg) and self.IVYAPPNAME == 'Guest'):
            #print("tab reçu : "+str(arg)[8:-5])     
            self.game.jeu.joinTable(str(arg)[8:-5])     
            
        elif ("time:" in str(arg) and self.IVYAPPNAME == 'Guest'):   
            self.game.jeu.setTime(int(str(arg)[7:-3]))  
            self.game.render()   
            self.game.updatescoreboard()
            
        elif ("coup:"in str(arg)):
            pos = str(arg)[7:-3].split(",")
            #print("positions reçus : "+ pos[0]+" "+pos[1])  
            self.turn(int(pos[0]),int(pos[1]))
            self.game.updatescoreboard()
            
            
    def turn(self,x,y):
        listMove = []
        valeur = self.game.jeu.tab.tableau[x][y]
        self.game.jeu.tab.findrec(x,y,valeur,listMove)
        if (listMove.__len__()>=3):
            self.game.jeu.tour(x,y)
            self.game.render()    
    
    def on_direct_msg(self,agent, num_id, msg):
        self.info('%r sent a direct message, id=%s, message=%s',agent, num_id, msg)    
        
    def sendmsg(self,texte):        
        IvySendMsg(texte)
        
    def stop(self):
        if not self.on_die_accepted and self.IVYAPPNAME!="":
            IvyStop()
        self.on_die_accepted = False
        self.IVYAPPNAME = ""
    
    def run(self):
        from ivy.ivy import ivylogger
        import logging
    
        self.matefound = False
        self.on_die_accepted = False
        ivybus = ''
        readymsg = '[%s is ready]' % self.IVYAPPNAME
        
        ivylogger.setLevel(logging.WARN)    
    
        self.info('Broadcasting on %s', ivybus or os.environ.get('IVYBUS') or 'ivydefault')
        
        # initialising the bus 
        IvyInit(self.IVYAPPNAME,             # application name for Ivy
                readymsg,               # ready message
                0,                      # parameter ignored
                self.on_connection_change,   # handler called on connection/disconnection
                self.on_die)                 # handler called when a die msg is received
    
        # starting the bus
        IvyStart(ivybus)
    
        # direct msg
        IvyBindDirectMsg(self.on_direct_msg)
        
        #Bind
        IvyBindMsg(self.on_msg, "(.*)")
        
        if IvyGetApplicationList().__len__()==1 and self.IVYAPPNAME=="Host":
            self.sendmsg("nom:"+self.IVYAPPNAME)
    
    def runJoin(self):        
        self.IVYAPPNAME = 'Guest'
        self.run()        
        
    def runHost(self,partie):
        self.IVYAPPNAME = 'Host'
        self.game = partie  
        self.run()
    
        