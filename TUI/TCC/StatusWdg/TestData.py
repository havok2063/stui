#!/usr/bin/env python
"""Supplies test data for the tcc status window

To do:
- fix so order of data is preserved
  by specifying the data as a tuple of tuples
  and turning it into an ordered dict for each dispatched message

- convert all axis widgets to use this 
  or at least fix them to use AxisCmdState instead of TCCStatus
  as necessary

History:
2006-03-16 ROwen
2009-03-31 ROwen    Modified to use TUI.Base.TestDispatcher.
2009-07-09 ROwen    Bug fix: test code was sending SlewEnds instead of SlewEnd.
2010-03-11 ROwen    Modified to send guide state and plate pointing information.
"""
import TUI.Base.TestDispatcher

testDispatcher = TUI.Base.TestDispatcher.TestDispatcher("tcc")
tuiModel = testDispatcher.tuiModel

def init():
    testDispatcher.dispatch("pointingInfo=3853, 11, A, 207.841, 35.3105, 15.0, 0.0, nan", actor="platedb")
    testDispatcher.dispatch("instrumentNum=10", actor="mcp")
    testDispatcher.dispatch("guideState=on; cartridgeLoaded=11, 3853, A, 1, 1", actor="guider")
    testDispatcher.dispatch(
        (   # start with Echelle (no rotator) and stop buttons in
            "Inst=BOSS",
            "IPConfig=FTF",
            "AxisCmdState=Tracking, Tracking, NotAvailable",
            "AxisErrCode='', '', NotAvailable",
            "AxePos=-340.009, 45, NaN",
            "AzStat=-340.009, 0.0, 4565, 0x801",
            "AltStat=45.0, 0.0, 4565, 0x801",
            "SecFocus=570",
            "GCFocus=-300",
            "scaleFac=1.00017",
        ),
        actor="tcc",
    )

def runTest():
    dataSet = (
        (   # enable stop buttons
            "AxePos=-340.009, 45, NaN",
            "AzStat=-340.009, 0.0, 4565, 0",
            "AltStat=45.0, 0.0, 4565, 0",
        ),
        (   # slew
            "ObjName='test object with a long name'",
            "ObjSys=FK5, 2000.0",
            "ObjNetPos=120.123450, 0.000000, 4494436859.66000, -2.345670, 0.000000, 4494436859.66000",
            "RotType=None",
            "AxePos=-350.999, 45, NAN",
            "SlewDuration=14.0",
            "AxisCmdState=Slewing, Slewing, NotAvailable",
            "AxisErrCode='', '', NotAvailable",
            "AxePos=-340.009, 45, NaN",
            "SecFocus=570",
            "GCFocus=-300",
            "TCCPos=-342.999, 38.623, NaN",
        ),
        (
            "AxePos=-348.121, 43.432, NaN",
            "TCCPos=-342.999, 38.623, NaN",
        ),
        (
            "AxePos=-346.329, 41.765, NaN",
            "TCCPos=-342.999, 38.623, NaN",
        ),
        (
            "AxePos=-344.325, 39.424, NaN",
            "TCCPos=-342.999, 38.623, NaN",
        ),
        (
            "AxePos=-343.012, 38.532, NaN",
            "TCCPos=-342.999, 38.623, NaN",
        ),
        (
            "AxePos=-342.999, 38.623, NaN",
            "TCCPos=-342.999, 38.623, NaN",
        ),
        (   # slew ends
            "SlewEnd",
            "AxisCmdState=Tracking, Tracking, NotAvailable",
            "AxisErrCode='','', NotAvailable",
            "AxePos=-342.974, 38.645, 10.0",
            "TCCPos=-342.974, 38.645, NaN",
        ),
        (   # tracking
            "AxisCmdState=Tracking, Tracking, NotAvailable",
            "AxisErrCode='','', NotAvailable",
            "AxePos=-342.964, 38.725, 10.0",
            "TCCPos=-342.964, 38.725, NaN",
        ),
        (   # change to dis, re-enabling the rotator
            "Inst=DIS",
            "IPConfig=TTF",
            "SlewDuration=2.0",
            "AxisCmdState = Slewing, Slewing, Halting",
            "AxisErrCode='', '', NoRestart",
            "AzStat=-342.953, -0.011, 4565, 0",
            "AltStat=38.815, 0.10, 4565, 0",
            "RotStat=10.0, 0.0, 4565, 0",
            "AxePos=-342.563, 38.625, 10.0",
            "TCCPos=-342.563, 38.625, NaN",
        ),
        (
            "SlewEnd",
            "AxisCmdState=Tracking, Tracking, Halted",
            "AxisErrCode='', '', NoRestart",
            "AxePos=-342.563, 38.625, 10.0",
            "TCCPos=-342.563, 38.625, NaN",
        ),
        (   # slew rotator
            "SlewDuration=6.0",
            "AxisCmdState=Slewing, Slewing, Slewing",
            "AxisErrCode='', '', ''",
            "RotType=Obj",
            "RotPos=3.456789, 0.000000, 4494436895.07921",
            "AxePos=-342.563, 38.625, 9.4",
            "TCCPos=-342.563, 38.625, 5.0",
        ),
        (
            "AxePos=-342.563, 38.625, 7.3",
            "TCCPos=-342.563, 38.625, 5.0",
        ),
        (
            "AxePos=-342.563, 38.625, 6.1",
            "TCCPos=-342.563, 38.625, 5.0",
        ),
        (
            "AxePos=-342.563, 38.625, 5.4",
            "TCCPos=-342.563, 38.625, 5.0",
        ),
        (
            "SlewEnd",
            "AxisCmdState=Tracking, Tracking, Tracking",
            "AxisErrCode='', '', ''",
            "AxePos=-342.563, 38.625, 5.0",
            "TCCPos=-342.563, 38.625, 5.0",
        ),
    )
    
    testDispatcher.runDataSet(dataSet)
