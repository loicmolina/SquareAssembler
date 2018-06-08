#!/usr/bin/env python
"""An ivyprobe script for ivy-python
"""
import os
import signal
import sys
from Modele.Jeu import Jeu
sys.path.append("D:\Programmes\ivy-python-3.1")
from ivy.std_api import *

# The next line taken from https://pythonhosted.org/six/
# Copyright (c) 2010-2016 Benjamin Peterson
class connection:
    
    def __init__(self,partie):    
        self.IVYAPPNAME = "IvyApp"
        self.name = ""
        self.game = partie  
        self.on_die_accepted = False
        self.matefound = False
        
        from ivy.ivy import ivylogger
        import logging
    

        self.on_die_accepted = False
        self.ivybus = ''
        self.readymsg = '[%s is ready]' % self.IVYAPPNAME
        
        ivylogger.setLevel(logging.WARN)    
    
        self.info('Broadcasting on %s', self.ivybus or os.environ.get('IVYBUS') or 'ivydefault')
        
        # initialising the bus 
        IvyInit(self.IVYAPPNAME,             # application name for Ivy
                self.readymsg,               # ready message
                0,                      # parameter ignored
                self.on_connection_change,   # handler called on connection/disconnection
                self.on_die)                 # handler called when a die msg is received
    
        # direct msg
        IvyBindDirectMsg(self.on_direct_msg)
        
        #Bind
        IvyBindMsg(self.on_msg, "(.*)")
        


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

        else:
            self.info('Ivy application %r has connected', agent) 
                
                
        #print("il y a ",IvyGetApplicationList().__len__()," dans le bus")
        self.info('Ivy applications currently on the bus: %s',','.join(IvyGetApplicationList()))
    
    
    def on_die(self,agent, _id):
        self.info('Received the order to die from %r with id = %d', agent, _id)
        self.on_die_accepted = True
        # will interrupt the raw_input()/input() in the main loop, below
        os.kill(os.getpid(), signal.SIGINT)
        
    def on_msg(self,agent, *arg):
        self.info('Received from %r: %s', agent, arg and str(arg) or '<no args>')        
        if ("size:" in str(arg) and self.name == 'Guest' and self.matefound):
            #print("size reçu : "+str(arg)[7:-3])
            self.game.jeu = Jeu(2,10)
            self.game.jeu.newTable(int(str(arg)[7:-3]))
        elif "asking" in str(arg) and self.name == 'Host' and self.matefound==False:
            self.sendmsg("nom:"+self.name) 
        elif ("asking" in str(arg) and self.name == "Guest") or ("Host" in  str(arg) and self.name == "Host"):
            self.sendmsg("forcequit")
        elif ("forcequit" in str(arg) and self.matefound == False):
            self.game.drawInstanceAlreadyExists()
            self.stop()
             
        elif "nom:" in str(arg) and self.matefound == False: 
            if self.name == 'Guest' and str(arg)[6:-3] == "Host" :
                self.sendmsg("nom:"+self.name)  
                self.matefound = True
                self.game.player2ready()
                    
            if self.name == 'Host' and (str(arg)[6:-3] == "Guest"):
                self.sendDataToGuest()
                self.game.render()
                self.game.updatescoreboard()
                self.matefound = True
                self.game.player1ready() 
                #print("_____________________________________________")
                    
        elif ("tab:" in str(arg) and self.name == 'Guest' and self.matefound):
            #print("tab reçu : "+str(arg)[8:-5])     
            self.game.jeu.joinTable(str(arg)[8:-5])     
            
        elif ("time:" in str(arg) and self.name == 'Guest' and self.matefound):   
            self.game.jeu.setTime(int(str(arg)[7:-3]))  
            self.game.render()   
            self.game.updatescoreboard()
            #print("_____________________________________________")
            
        elif ("coup:"in str(arg) and self.matefound):
            pos = str(arg)[7:-3].split(",")
            #print("positions reçus : "+ pos[0]+" "+pos[1])  
            self.game.jeu.tour(int(pos[0]),int(pos[1]))
            self.game.render()            
            self.game.updatescoreboard()
            
        elif ("end" in str(arg) and self.matefound):
            #print("END pour "+self.name)
            self.matefound = False
            self.game.fin()
            self.stop()
        
    def on_direct_msg(self,agent, num_id, msg):
        self.info('%r sent a direct message, id=%s, message=%s',agent, num_id, msg)    
        
    def sendmsg(self,texte):  
        #print("envoi de "+texte)      
        IvySendMsg(texte)
        
    def stop(self):
        if not self.on_die_accepted and self.name!="": 
            #print("Le client se ferme")               
            IvyStop()   
            if (self.matefound):         
                self.matefound = False              
                self.sendmsg("end")      
            self.on_die_accepted = False
            self.name=""
        
    
    def run(self):       
        # starting the bus
        #print("taille liste avant :"+str(IvyGetApplicationList().__len__()))
        #print("nouveau nom :"+self.name)
        IvyStart(self.ivybus)
             
            
            
    def runJoin(self):     
        import time   
        self.name = "Guest"
        self.run()      
        time.sleep(0.1)
        self.sendmsg("asking")  
        
    def runHost(self,partie):   
        import time  
        self.name = "Host"
        self.game = partie  
        self.run()
        time.sleep(0.1)
        self.sendmsg("nom:"+self.name)  
    
        