#!/usr/bin/env python
"""An ivyprobe script for ivy-python
"""
import getopt
import os
import signal
import sys
import time, getopt, queue
import random
from random import randint
from asyncio.tasks import sleep
from Modele import Jeu
sys.path.append("D:\Programmes\ivy-python-3.1")
from ivy.std_api import *

# The next line taken from https://pythonhosted.org/six/
# Copyright (c) 2010-2016 Benjamin Peterson
class connection:
    
    def __init__(self,partie):    
        self.IVYAPPNAME = ""
        self.modele = partie  
        self.on_die_accepted = False
    
    def setmodele(self,partie):
        self.modele=partie

    def info(self,fmt, *arg):
        1
        #print(fmt % arg)
    
    def on_connection_change(self,agent, event):
        if event == IvyApplicationDisconnected:
            self.info('Ivy application %r has disconnected', agent)
            if (IvyGetApplicationList().__len__()==0):
                self.modele.fin()
        else:
            self.info('Ivy application %r has connected', agent)
            if (IvyGetApplicationList().__len__()==1 and self.IVYAPPNAME == 'Host'):
                self.sendmsg("size:"+str(self.modele.jeu.tab.colonnes))
                self.sendmsg("tab:"+str(self.modele.jeu.tab.tableau))
                self.sendmsg("time:"+str(self.modele.jeu.tempsTourMax)+","+str(self.modele.jeu.tempsTour))
                self.modele.readyplayer2()
                self.modele.render()
                
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
            self.modele.jeu.newTable(int(str(arg)[7:-3]))
        elif ("tab:" in str(arg) and self.IVYAPPNAME == 'Guest'):
            #print("tab reçu : "+str(arg)[8:-5])     
            self.modele.jeu.joinTable(str(arg)[8:-5])     
        elif ("time:" in str(arg) and self.IVYAPPNAME == 'Guest'):
            timers = str(arg)[7:-3].split(",")
            #print("temps reçu : "+ timers[0])      
            self.modele.jeu.setTime(int(timers[0]),int(timers[1]))    
            self.modele.render()   
        elif ("coup:"in str(arg)):
            pos = str(arg)[7:-3].split(",")
            #print("positions reçus : "+ pos[0]+" "+pos[1])  
            self.modele.jeu.tour(int(pos[0]),int(pos[1]))
            self.modele.render()
            
    
    
    def on_direct_msg(self,agent, num_id, msg):
        self.info('%r sent a direct message, id=%s, message=%s',agent, num_id, msg)    
    
    def on_pong(self,agent, delta):
        self.info('%s answered to ping in %fs', agent, delta)
        
    def sendmsg(self,texte):        
        IvySendMsg(texte)
        
    def stop(self):
        if (self.IVYAPPNAME != ""):
            IvyStop()
        self.on_die_accepted = False
        self.IVYAPPNAME = ""
    
    def run(self):
        from ivy.ivy import ivylogger
        import logging
    
        ivybus = ''
        readymsg = '[%s is ready]' % self.IVYAPPNAME
        verbose = 0
        showbind = 0
    
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
    
        # pong
        IvyBindPong(self.on_pong)    
        
        #Bind
        IvyBindMsg(self.on_msg, "(.*)")
    
    
    def runJoin(self):        
        self.IVYAPPNAME = 'Guest'
        self.run()
        
        
    def runHost(self):
        self.IVYAPPNAME = 'Host'
        self.run()
        
    
        