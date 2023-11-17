#Module Import
import maya.cmds as cmds
from tlpf_toolkit.curves import CurveFunctions

import logging
import os

#=======================================
## Guided Ribbon tool
#=======================================


CTRL = "ctrl"
SKIN = "skn"
JOINT = "jnt"
CURVE = "crv"
GUIDES = "guides"
GROUP = "grp"

def guidedRibbonUI():

    #basic Window creation
    configWindow = cmds.window(title="SamLipSetup", iconName='SamLips', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])

    #create Guides Button
    setLeftSideBtn = cmds.button(label="Left", command = lambda _: createGuideHirarchy())

    #create Guides Button
    setCenterBtn = cmds.button(label="Center", command = lambda _: createGuideHirarchy())

    #create Guides Button
    setRightBtn = cmds.button(label="Right", command = lambda _: createGuideHirarchy())

    # #Title Text
    # titleText = cmds.text(label="Guided Ribbon Tool", height = 30, backgroundColor = [.5, .5, .5])

    # #Space Divider
    # cmds.text(label="", height=10)


    


    # #Manual Guides Label
    # guidesLabel = cmds.text(label="Manual Guides", height = 20, backgroundColor = [.3, .3, .3])

    # #create Guides Button
    # createGuidesBtn = cmds.button(label="Create Guide Hirarchy", command = lambda _: createGuideHirarchy())

    # #Space Divider
    # cmds.text(label="", height=10)

    cmds.showWindow(configWindow)



    #Create Guide Setup Button

def buildGuidedRibbon(side, baseName):

    createRibbonHirarchy(side, baseName)


def createGuideHirarchy(side, baseName):
    
    mainGuideGrp = cmds.createNode("transform", name = f"{side}_{baseName}_{GUIDES}_{GROUP}")

    pinGuidesGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Pin{GUIDES}_{GROUP}", parent = mainGuideGrp)

    ctrlGuidesGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Ctrl{GUIDES}_{GROUP}", parent = mainGuideGrp)


def createRibbonHirarchy(side, baseName):

    mainRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Rig_{GROUP}")

    #Pin Grp
    pinRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Pin_{GROUP}")

    #Curves Grp
    curvesRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_{CURVE}_{GROUP}")

    #Ctrls Grp
    ctrlRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_{CTRL}_{GROUP}")


def createRibbonCurve(side, baseName):

    guideLocators = cmds.listRelatives(f"{side}_{baseName}_Pin{GUIDES}_{GROUP}")

    ribbonCurve = CurveFunctions.createLinearCurveFromSelection(guideLocators, f"{side}_CenterRibbon_{CURVE}")


