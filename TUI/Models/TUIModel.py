#!/usr/bin/env python
"""An object that models the overall state of TUI.
Includes the following items:
- dispatcher: the keyword dispatcher (RO.KeyDispatcher.KeyDispatcher)
    note: the network connection is dispatcher.connection
- prefs: the application preferences (TUI.TUIPrefs.TUIPrefs)
- tlSet: the set of toplevels (windows) (RO.Wdg.ToplevelSet)
- root: the root application window (Tkinter.Toplevel);
    mostly used when one to execute some Tkinter command
    (all of which require an arbitrary Tkinter object)

Note: the model must be created after the Tkinter root
has been created. Otherwise you will get a Tkinter error.

Most items are defined and loaded when the model is created.
However, "tlSet" is empty to start; use this object to add
windows to the application (so their geometry is recorded).

History:
2003-06-09 ROwen
2003-07-18 ROwen    Added getConnection, getUsername, getProgID.
2003-10-06 ROwen    Added getCmdr; changed getProgramName to getProgID
                    and made it return in the case used by the Hub.
2003-10-10 ROwen    Modified to use new RO.Comm.HubConnection
2004-02-03 ROwen    Modified to use RO.OS.getPrefsDir and thus to
                    look for the geom file where it really belongs.
2004-08-11 ROwen    Modified to use RO.Constants.
2004-09-03 ROwen    Modified for RO.Wdg._setHelpURLBase -> RO.Constants._setHelpURLBase.
2004-09-08 ROwen    Added logMsg method.
2005-01-05 ROwen    Changed logMsg state -> severity.
                    Bug fix: logMsg was misusing severity (formerly state).
2005-06-16 ROwen    Modified logMsg for updated KeyDispatcher.logMsg.
2005-08-02 ROwen    Modified to find the help directory without it being a package.
2005-09-28 ROwen    Modified to use RO.OS.getPrefsDirs instead of getPrefsDir.
2005-10-06 ROwen    getprefsDir needs new inclNone=True argument.
2006-03-30 ROwen    Supply platform info during login.
2006-10-25 ROwen    Enhanced the logMsg function:
                    - Added keyword argument
                    - Output is now formatted like hub output.
2009-03-27 ROwen    Switch to opscore.actor dispatcher.
2009-03-31 ROwen    Changed to use Model() instead of getModel(); internally changed to use
                    singleton pattern based on __new__.
                    Renamed instance variable root to tkRoot to be less ambiguous.
                    Modified for use twisted; added instance variable "reactor".
2009-07-21 ROwen    Modified to set new CmdKeyVarDispatcher flag includeName.
2009-07-22 ROwen    Modified to log to stdout in test mode (to compensate for the fact
                    that the dispatcher's default changed to not log).
2009-10-03 ROwen    Changed name of prefs file from TUIGeom to <ApplicationName>Geom.
2009-11-09 ROwen    Removed a redundant import.
"""
import os
import platform
import sys
import traceback
import twisted.internet.tksupport
import RO.Comm
import RO.Comm.HubConnection
import RO.Constants
import RO.OS
import RO.TkUtil
import RO.Wdg
import opscore.actor.model
import opscore.actor.cmdkeydispatcher
import Tkinter
import TUI.TUIPrefs
import TUI.Version

def _getGeomFile():
    geomDir = RO.OS.getPrefsDirs(inclNone=True)[0]
    if geomDir == None:
        raise RuntimeError("Cannot determine prefs dir")
    geomName = "%s%sGeom" % (RO.OS.getPrefsPrefix(), TUI.Version.ApplicationName)
    return os.path.join(geomDir, geomName)

class Model(object):
    def __new__(cls, testMode=False):
        if hasattr(cls, 'self'):
            return cls.self

        cls.self = object.__new__(cls)
        self = cls.self

        self.tkRoot = Tkinter.Frame().winfo_toplevel()
        twisted.internet.tksupport.install(self.tkRoot)
        self.reactor = twisted.internet.reactor
    
        # network connection
        if testMode:
            print "Running in test mode, no real connection possible"
            connection = RO.Comm.HubConnection.NullConnection()
        else:
            connection = RO.Comm.HubConnection.HubConnection(
                loginExtra = getLoginExtra(),
            )

        # keyword dispatcher
        self.dispatcher = opscore.actor.cmdkeydispatcher.CmdKeyVarDispatcher(
            name = "stui",
            connection = connection,
            includeName = False,
        )
        opscore.actor.model.Model.setDispatcher(self.dispatcher)
        if testMode:
            self.dispatcher.setLogFunc(opscore.actor.cmdkeydispatcher.logToStdOut)
    
        # TUI preferences
        self.prefs = prefs = TUI.TUIPrefs.TUIPrefs()
        
        # TUI window (topLevel) set;
        # this starts out empty; others add windows to it
        self.tlSet = RO.Wdg.ToplevelSet(
            fileName = _getGeomFile(),
            createFile = True,  # create file if it doesn't exist
        )

        # set up standard bindings (since the defaults are poor)
        RO.Wdg.stdBindings(self.tkRoot)

        # set up the base URL for TUI help
        RO.Constants._setHelpURLBase (getBaseHelpURL())

        return self
        
    def __init__(self, *args, **kargs):
        pass
        
    def getConnection(self):
        """Return the network connection, an RO.Comm.HubConnection object.
        """
        return self.dispatcher.connection

    def getCmdr(self):
        """Return the commander (in the form program.username)
        assigned by the Hub, or None if not connected.
        """
        return self.getConnection().getCmdr()
    
    def getProgID(self):
        """Return the program ID (in the case the hub uses),
        or None if not connected.
        """
        return self.getConnection().getProgID()

    def getUsername(self):
        """Return the user name assigned by the Hub,
        or None if not connected.
        """
        return self.getConnection().getUsername()
    
    def logMsg(self,
        msgStr,
        severity = RO.Constants.sevNormal,
        copyStdErr = False,
        doTraceback = False,
        keyword = "Text",
    ):
        """Writes a message to the log window, if available,
        else to standard error.
        
        Inputs:
        - msgStr    message to display; a final \n is appended
        - severity      one of RO.Constants.sevNormal, sevWarning or sevError
        - copyStdErr    write copy to standard error?
        - doTraceback   write traceback to standard error?
                        (if True then a copy of msgStr is always written to std error)
        - keyword       keyword for message string; use None if msgStr is already
                        in keyword-value format.
        
        Note: use tuiModel.dispatcher.logMsg if you want full control
        over the message format.
        """
        if keyword:
            msgStr = ".tui 0 tui %s=%r" % (keyword, msgStr)
        else:
            msgStr = ".tui 0 tui %s" % (msgStr,)
        self.dispatcher.logMsg(msgStr, severity = severity)
        
        if copyStdErr or doTraceback:
            sys.stderr.write (msgStr + "\n")
            if doTraceback:
                traceback.print_exc(file=sys.stderr)

def getBaseHelpURL():
    """Return the file URL to the base directory for help"""
    # set up the base URL for TUI help
    helpDir = RO.OS.getResourceDir(TUI, "Help")
    pathList = RO.OS.splitPath(helpDir)
    if pathList[0] == "/":
        pathList = pathList[1:]
    urlStylePath = "/".join(pathList)
    if not urlStylePath.endswith("/"):
        urlStylePath += "/"
    return "file:///" + urlStylePath

def getLoginExtra():
    """Return extra login data"""
    versName, versDate = TUI.Version.VersionStr.split()
    versData = " ".join((TUI.Version.VersionDate, TUI.Version.VersionName))
    platData = platform.platform()
# the following code fails on intel Macs
# at least with python 2.4.2;
# apparently gestalt is not yet working
#   if platData.lower().startswith("darwin"):
#       # replace Version-kernel#- with MacOSX-vers#-
#       macVers = platform.mac_ver()[0]
#       if macVers:
#           extraInfo = platData.split("-", 2)[-1]
#           platData = "MacOSX-%s-%s" % (macVers, extraInfo)
    wsysData = RO.TkUtil.getWindowingSystem()
    platData = " ".join((platData, wsysData))
    
    return "type=TUI version=%r platform=%r" % \
        (versData, platData)
    

if __name__ == "__main__":
    tuiModel = Model()
    print "getBaseHelpURL = ", getBaseHelpURL()
