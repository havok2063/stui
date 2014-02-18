
"""
takes short dark to check apogee binding 

History
02-21-2013 EM: proceed if gang connector is in podium;  UT time changed to TAI
08/23/2013 EM: moved to STUI  and changed name to  APOGEE Short Dark.py 
08/29/2013 EM: changed mcp.gang descriptions for updated keyword 
09/05/2013 EM: refinement
09/25/2013  EM:  check gang position, but run at any position. 
                    print information where is gang connector.
01/24/2014  fixed bug,  "apogeecal shutterOpen" changed to  "apogeecal shutterClose",
                    do not know why it was so. 
02-17-2014 EM: fixed bug: checkFail was False, and I change to True, to halt script 
                is command fault
     
"""

import RO.Wdg
import TUI.Models
from datetime import datetime
import time
#import RO.Astro.Tm
import subprocess
import tkMessageBox as box

class ScriptClass(object):
    def __init__(self, sr):
        # if True, run in debug-only mode (which doesn't DO anything)
        # if False, real time run
        sr.debug = False
        
        sr.master.winfo_toplevel().wm_resizable(True, True)
        self.logWdg = RO.Wdg.LogWdg(master=sr.master, width=35, height =20,)
        self.logWdg.grid(row=0, column=0, sticky="news")
        sr.master.rowconfigure(0, weight=1)
        sr.master.columnconfigure(0, weight=1)
        self.name="APOGEE Short Dark"        
        self.logWdg.text.tag_config("a", foreground="magenta")
        self.logWdg.text.tag_config("g", foreground="grey")

#        self.logWdg.addMsg("%s" % self.name)

        self.cmdList=[
            "apogeecal allOff",
            "apogee shutter close",
     #    "apogeecal shutterOpen",
            "apogeecal shutterClose",
            "apogee expose nreads=3 ; object=Dark",
         #   "apogee expose nreads=10 ; object=Dark",
            "apogeecal shutterClose",
            "apogeecal allOff", 
            ]
        self.logWdg.addMsg("-- %s -" % (self.name),  tags=["a"] )
        for ll in self.cmdList: 
            self.logWdg.addMsg("%s" % ll,tags=["g"] )

    
    def getTAITimeStr(self,):
      currPythonSeconds = RO.Astro.Tm.getCurrPySec()
      currTAITuple= time.gmtime(currPythonSeconds - RO.Astro.Tm.getUTCMinusTAI())
      self.taiTimeStr = time.strftime("%H:%M:%S", currTAITuple) 
      return self.taiTimeStr
      
    def checkGangPodium(self, sr): 
      self.mcpModel = TUI.Models.getModel("mcp")
      ngang=sr.getKeyVar(self.mcpModel.apogeeGang, ind=0, defVal="n/a")
      hlp=self.mcpModel.apogeeGangLabelDict.get(ngang, "?")
      self.logWdg.addMsg("mcp.gang=%s  (%s)" % (ngang, hlp))
      return True
  #    if ngang != 12:         
  #      self.logWdg.addMsg(" Error: gang must be = 12 (podium dense)",    
  #                severity=RO.Constants.sevError)
  #      subprocess.Popen(['say','error'])       
  #      return False 
  #    else:
  #      return True
      
    def run(self, sr):       
      self.logWdg.clearOutput() 
      tm = self.getTAITimeStr()      
      self.logWdg.addMsg("-- %s -- %s " % (tm,self.name),tags=["a"])  

      if not self.checkGangPodium(sr):
           raise sr.ScriptError("") 
 
      for actorCmd in [
            "apogeecal allOff",
            "apogee shutter close",
     #    "apogeecal shutterOpen",
            "apogeecal shutterClose",
            "apogee expose nreads=3 ; object=Dark",
         #   "apogee expose nreads=10 ; object=Dark",
            "apogeecal shutterClose",
            "apogeecal allOff",          
      ]:
         actor, cmd = actorCmd.split(None, 1)
         self.logWdg.addMsg("%s" % (actorCmd)) 
         yield sr.waitCmd(actor=actor, cmdStr=cmd, checkFail = True,)
         cmdVar = sr.value
         if cmdVar.didFail:
             ss1=" %s   ** FAILED **" % (actorCmd)
             self.logWdg.addMsg("      %s" % (ss1),severity=RO.Constants.sevError)
             print self.name, ss1
             break

      self.logWdg.addMsg("-- done --",tags=["a"])  
      self.logWdg.addMsg("")

#mcp.py
#Key("apogeeGang",
#Enum("0", "1", "2", "3", labelHelp=("Disconnected", "Podium", "Cart", "Sparse cals"))),

#apogeecal allOff
#apogee shutter close
#apogeecal shutterOpen
#apogee expose nreads=3 ; object=Dark
#apogeecal shutterClose
#apogeecal allOff
