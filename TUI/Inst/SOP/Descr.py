"""Objects that describe the basics of commands, stages and parameters
Used to paint the GUI

To do: allow each parameter to be associated with more than one stage
(in which case the parametrs are shown if any of the stages is shown),]
or no stages (in which case the parameters are always shown).
That would simplify the definitions quite a bit: no need for specifying StageWdgSet in this file;
just name the real stages and the fake stages and list the parameters.
This will get fix a known minor issue in gotoField and simplify commands
that have no real stages (doBossCalibs).

History:
2010-05-27 ROwen    Reordered the commands and added gotoInstrumentChange.
2011-07-05 ROwen    Added doApogeeScience and gotoGangChange.
                    Added "(BOSS)" to the button names for the doScience and doCalibs commands.
2011-07-11 ROwen    Added comment parameter to doApogeeScience and alt parameter to gotoGangChange.
2013-10-22 ROwen    Fixed ticket #1915 by changing default seqCount from 3 to 2 for doApogeeScience.
2014-02-11 ROwen    Renamed doScience, doCalibs to doBossScience, doBossCalibs.
2014-02-12 ROwen    Fixed ticket #1972: use guiderTime instead guiderExpTime for gotoField.
2014-03-24 ROwen    Implemented enhancement request #2018 by rearranging the stages so that
                    calibration states are after gotoGangChange and gotoInstrumentChange.
                    Made pyflakes linter happier by explicitly importing symbols from CommandWdgSet.
2014-06-20 ROwen    Updated for more recent sop, including handling fake stages.
2014-06-21 ROwen    Bug fix: doBossCalibs parameters were associated with a stage that doesn't exist,
                    and (since the command now has fake stages) were not being shown.
2014-06-23 ROwen    Modified to use improved CommandWdgSet: parameters are specified separately from stages.
2014-08-29 ROwen    Added support for doApogeeMangaDither and doApogeeMangaSequence commands.
"""
from CommandWdgSet import CommandWdgSet, LoadCartridgeCommandWdgSetSet, \
    CountParameterWdgSet, IntParameterWdgSet, FloatParameterWdgSet, StringParameterWdgSet

def getCommandList():
    return (
        # guider loadcartridge command
        LoadCartridgeCommandWdgSetSet(),

        # sop gotoField [<arcTime>] [<flatTime>] [<guiderFlatTime>] [<guiderTime>]
        #   [noSlew] [noHartmann] [noCalibs] [noGuider] [abort] [keepOffsets]
        # 
        # Slew to the current cartridge/pointing
        # Arguments:
        # 	abort                               Abort a command
        # 	arcTime                             Exposure time for arcs
        # 	flatTime                            Exposure time for flats
        # 	guiderFlatTime                      Exposure time for guider flats
        # 	noCalibs                            Don't run the calibration step
        # 	noGuider                            Don't start the guider
        # 	noHartmann                          Don't make Hartmann corrections
        # 	noSlew                              Don't slew to field
        # 
        # Slew to the position of the currently loaded cartridge. At the beginning of the
        # slew all the lamps are turned on and the flat field screen petals are closed.
        # When you arrive at the field, all the lamps are turned off again and the flat
        # field petals are opened if you specified openFFS.
        CommandWdgSet(
            name = "gotoField",
            realStageStr = "slew hartmann calibs guider",
            fakeStageStr = "cleanup",
            parameterList = (
                FloatParameterWdgSet(
                    name = "arcTime",
                    units = "sec",
                    stageStr = "calibs",
                    helpText = "exposure time for each arc",
                ),
                FloatParameterWdgSet(
                    name = "flatTime",
                    units = "sec",
                    stageStr = "calibs",
                    helpText = "exposure time for each flat",
                ),
                FloatParameterWdgSet(
                    name = "guiderFlatTime",
                    units = "sec",
                    stageStr = "calibs guider",
                    helpText = "exposure time for each guider flat",
                ),
                FloatParameterWdgSet(
                    name = "guiderTime",
                    units = "sec",
                    stageStr = "guider",
                    helpText = "initial exposure time for guider images",
                ),
            ),
        ),

        # Usage: sop doApogeeScience [expTime=FF.F] [ditherSeq=SSS] [seqCount=N] [stop]   
        #                 [abort=] [comment=SSS]   
        #    
        # Take a sequence of dithered APOGEE science frames, or stop or modify a running   
        # sequence.   
        # Arguments:   
        # 	abort                               Abort a command   
        # 	comment                             comment for headers   
        # 	ditherSeq                           dither positions for each sequence. e.g. AB   
        # 	expTime                             Exposure time   
        # 	seqCount                            number of times to launch sequence   
        # 	stop                                no help   
        CommandWdgSet(
            name = "doApogeeScience",
            parameterList = (
                StringParameterWdgSet(
                    name = "ditherSeq",
                    defValue = "AB",
                ),
                CountParameterWdgSet(
                    name = "seqCount",
                    defValue = 2,
                ),
                StringParameterWdgSet(
                    name = "comment",
                    defValue = "",
                    units = None,
                    trackCurr = False,
                    ctrlColSpan = 10,
                    ctrlSticky = "ew",
                    helpText = "comment for FITS file",
                ),
                FloatParameterWdgSet(
                    name = "expTime",
                    startNewColumn = True,
                    defValue = 500.0,
                    units = "sec",
                    helpText = "exposure time for each exposure",
                ),
            ),
        ),

        # Usage: sop doBossScience [expTime=FF.F] [nexp=N] [abort] [stop] [test]   
        #    
        # Take a set of science frames   
        # Arguments:   
        #   abort                               Abort a command   
        #   expTime                             Exposure time   
        #   nexp                                Number of exposures to take   
        #   stop                                no help   
        #   test                                Assert that the exposures are not expected to be meaningful   
        CommandWdgSet(
            name = "doBossScience",
            parameterList = (
                CountParameterWdgSet(
                    name = "nExp",
                    defValue = 0,
                    helpText = "number of science exposures",
                ),
                FloatParameterWdgSet(
                    name = "expTime",
                    startNewColumn = True,
                    units = "sec",
                    helpText = "exposure time for each exposure",
                ),
            ),
        ),

        # Usage: sop doMangaDither [dither={NSEC}] [expTime=FF.F]
        #    
        # Take one manga exposure at a specified dither
        #
        # Arguments:   
        #   dither                              One of [CNSE], default N
        #   expTime                             Exposure time (sec), default=900
        CommandWdgSet(
            name = "doMangaDither",
            fakeStageStr = "expose dither",
            parameterList = (
                StringParameterWdgSet(
                    name = "dither",
                    defValue = "N",
                    paramWidth = 2,
                    helpText = "Manga dither: C, N, S or E",
                ),
                FloatParameterWdgSet(
                    name = "expTime",
                    startNewColumn = True,
                    units = "sec",
                    defValue = 900,
                    helpText = "exposure time for each flat",
                ),
            ),
        ),

        # Usage: sop doMangaDither [count=N] [dithers=str] [expTime=FF.F]
        #    
        # Take multiple sequences of manga exposures at various dithers
        # The number of exposures = count * len(dither)
        #
        # Arguments:   
        #   count                               Number of repetitions of the dither sequence, default 3
        #   dither                              String of letters from CNSE, default NSE
        #   expTime                             Exposure time (sec), default=900
        CommandWdgSet(
            name = "doMangaSequence",
            fakeStageStr = "expose calibs dither",
            parameterList = (
                CountParameterWdgSet(
                    name = "count",
                    defValue = 3,
                    helpText = "number of repetitions of the dither sequence",
                ),
                StringParameterWdgSet(
                    name = "dithers",
                    startNewColumn = True,
                    defValue = "NSE",
                    paramWidth = 4,
                    helpText = "Manga dithers: any sequence of letters C, N, S or E",
                ),
                FloatParameterWdgSet(
                    name = "expTime",
                    startNewColumn = True,
                    units = "sec",
                    defValue = 900,
                    helpText = "exposure time for each exposure",
                ),
            ),
        ),


        # Usage: sop doApogeeMangaDither [dither={NSEC}] [expTime=FF.F]
        #    
        # Take one manga exposure at a specified dither
        #
        # Arguments:   
        #   mangaDither                         One of [CNSE], default C
        #   mangaExpTime                        Manga exposure time (sec), default=900
        #   apogeeExpTime                       Apogee exposure time (sec), default=450
        CommandWdgSet(
            name = "doApogeeMangaDither",
            fakeStageStr = "expose dither",
            parameterList = (
                StringParameterWdgSet(
                    name = "mangaDither",
                    skipRows = 1,
                    defValue = "N",
                    paramWidth = 2,
                    helpText = "manga dither sequence".
                ),
                FloatParameterWdgSet(
                    name = "apogeeExpTime",
                    startNewColumn = True,
                    units = "sec",
                    defValue = 450,
                    helpText = "Apogee exposure time".
                ),
                FloatParameterWdgSet(
                    name = "mangaExpTime",
                    units = "sec",
                    defValue = 900,
                    helpText = "Manga exposure time".
                ),
            ),
        ),

        # Usage: sop doApogeeMangaDither [count=N] [dithers=str] [expTime=FF.F]
        #    
        # Take multiple sequences of manga exposures at various dithers
        # The number of exposures = count * len(dither)
        #
        # Arguments:   
        #   count                               Number of repetitions of the dither sequence, default 3
        #   mangaDithers                        String of letters from CNSE, default NSE
        #   mangaExpTime                        Manga exposure time (sec), default=900
        #   apogeeExpTime                       Apogee exposure time (sec), default=450
        CommandWdgSet(
            name = "doApogeeMangaSequence",
            fakeStageStr = "expose calibs dither",
            parameterList = (
                CountParameterWdgSet(
                    name = "count",
                    defValue = 2,
                    helpText = "number of repetitions of the dither sequence",
                ),
                StringParameterWdgSet(
                    name = "mangaDithers",
                    defValue = "NSE",
                    paramWidth = 4,
                    helpText = "Manga dithers: any sequence of letters C, N, S or E",
                ),
                FloatParameterWdgSet(
                    name = "apogeeExpTime",
                    startNewColumn = True,
                    paramWidth = 4,
                    units = "sec",
                    defValue = 450,
                    helpText = "Apogee exposure time",
                ),
                FloatParameterWdgSet(
                    name = "mangaExpTime",
                    units = "sec",
                    defValue = 900,
                    helpText = "Manga exposure time",
                ),
            ),
        ),

        # Usage: sop gotoGangChange [alt=FF.F] [abort] [stop]   
        #    
        # Go to the gang connector change position   
        # Arguments:   
        #   abort                               Abort a command   
        #   alt                                 what altitude to slew to   
        #   stop                                no help   
        CommandWdgSet(
            name = "gotoGangChange",
            realStageStr = "domeFlat slew",
            parameterList = (
                FloatParameterWdgSet(
                    name = "alt",
                    units = "deg",
                    stageStr = "slew",
                    helpText = "desired altitude",
                ),
            ),
        ),

        # Usage: sop gotoInstrumentChange
        # 
        # Go to the instrument change position
        CommandWdgSet(
            name = "gotoInstrumentChange",
        ),

        # Usage: sop doApogeeSkyFlats [expTime=FF.F] [ditherSeq=SSS] [stop] [abort=]
        #
        # RUSSELL WARNING: I am guessing a bit because sop help didn't show this command.
        #    
        # Take a sequence of dithered APOGEE sky flats, or stop or modify a running sequence.   
        # Arguments:   
        # 	abort                               Abort a command   
        # 	ditherSeq                           dither positions for each sequence. e.g. AB   
        # 	expTime                             Exposure time   
        # 	stop                                no help   
        CommandWdgSet(
            name = "doApogeeSkyFlats",
            parameterList = (
                StringParameterWdgSet(
                    name = "ditherSeq",
                    defValue = "AB",
                    helpText = "Apogee dither sequence",
                ),
                FloatParameterWdgSet(
                    name = "expTime",
                    startNewColumn = True,
                    defValue = 500.0,
                    units = "sec",
                    helpText = "exposure time for each flat",
                ),
            ),
        ),

        # Usage: sop doApogeeDomeFlat
        CommandWdgSet(
            name = "doApogeeDomeFlat",
        ),
        
        # sop doBossCalibs [narc=N] [nbias=N] [ndark=N] [nflat=N] [arcTime=FF.F]
        #          [darkTime=FF.F] [flatTime=FF.F] [guiderFlatTime=FF.F]
        # 
        # Take a set of calibration frames
        # Arguments:
        # 	arcTime                             Exposure time for arcs
        # 	darkTime                            Exposure time for darks
        # 	flatTime                            Exposure time for flats
        # 	guiderFlatTime                      Exposure time for guider flats
        # 	narc                                Number of arcs to take
        # 	nbias                               Number of biases to take
        # 	ndark                               Number of darks to take
        # 	nflat                               Number of flats to take
        CommandWdgSet(
            name = "doBossCalibs",
            fakeStageStr = "bias dark flat arc cleanup",
            parameterList = (
                CountParameterWdgSet(
                    name = "nBias",
                    defValue = 0,
                    helpText = "number of bias exposures",
                ),
                CountParameterWdgSet(
                    name = "nDark",
                    defValue = 0,
                    helpText = "number of dark exposures",
                ),
                CountParameterWdgSet(
                    name = "nFlat",
                    defValue = 0,
                    helpText = "number of flat exposures",
                ),
                CountParameterWdgSet(
                    name = "nArc",
                    skipRows = 1,
                    defValue = 0,
                    helpText = "number of arc exposures",
                ),
                FloatParameterWdgSet(
                    name = "darkTime",
                    startNewColumn = True,
                    skipRows = 1,
                    units = "sec",
                    helpText = "exposure time for each dark",
                ),
                FloatParameterWdgSet(
                    name = "flatTime",
                    units = "sec",
                    helpText = "exposure time for each flat",
                ),
                FloatParameterWdgSet(
                    name = "guiderFlatTime",
                    units = "sec",
                    helpText = "exposure time for each guider flat",
                ),
                FloatParameterWdgSet(
                    name = "arcTime",
                    units = "sec",
                    helpText = "exposure time for each arc",
                ),
            ),
        ),

        # Usage: sop gotoStow
        # 
        # Go to the gang connector change/stow position
        #
        # It is a quirk of sop that a command with no stages has one stage named after the command
        CommandWdgSet(
            name = "gotoStow",
        ),
    )
