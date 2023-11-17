#Module Import
import maya.cmds as cmds
import maya.app as app
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
GUIDES = "Guides"
GROUP = "grp"

def guidedRibbonUI():

    #basic Window creation
    configWindow = cmds.window(title="SamLipSetup", iconName='SamLips', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.columnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Guided Ribbon Tool", height = 30, backgroundColor = [.5, .5, .5])

    #Manual Guides Label
    baseNameLabel = cmds.text(label="Set Base Name", height = 20, backgroundColor = [.3, .3, .3])

    #Base Name Label
    baseNameTextField = cmds.textField()

    #Manual Guides Label
    sideLabel = cmds.text(label="Define Side", height = 20, backgroundColor = [.3, .3, .3])
    
    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])

    #create Guides Button
    setLeftSideBtn = cmds.button(label="Left", width = 100,  command = lambda _: toggleButtonColor([setLeftSideBtn, setCenterBtn, setRightBtn], setLeftSideBtn, [0, 0.5, 0]))

    #create Guides Button
    setCenterBtn = cmds.button(label="Center", width = 100, command = lambda _: toggleButtonColor([setLeftSideBtn, setCenterBtn, setRightBtn], setCenterBtn, [0, 0.5, 0]))

    #create Guides Button
    setRightBtn = cmds.button(label="Right", width = 100, command = lambda _: toggleButtonColor([setLeftSideBtn, setCenterBtn, setRightBtn], setRightBtn, [0, 0.5, 0]))

    cmds.setParent('..')

    #Window Layout
    cmds.columnLayout(adjustableColumn=True)


    #Space Divider
    cmds.text(label="", height=10)

    #Manual Guides Label
    guidesLabel = cmds.text(label="Manual Guides", height = 20, backgroundColor = [.3, .3, .3])

    #create Guides Button
    createGuidesBtn = cmds.button(label="Create Guide Hirarchy", command = lambda _: createGuideHirarchy(getSideUserInput([setLeftSideBtn, setCenterBtn, setRightBtn]), 
                                                                                                         cmds.textField(baseNameTextField, query = True, text = True)))
    
    #Space Divider
    cmds.text(label="", height=10)

    #Build Ribbon Label
    buildRibbonLabel = cmds.text(label="Create Guided Ribbon", height = 20, backgroundColor = [.3, .3, .3])

    #create Guides Button
    buildRibbonButton = cmds.button(label="Build Ribbon", height = 40, command = lambda _: buildGuidedRibbon("l", "armVineC"))

    cmds.showWindow(configWindow)

    #Create Guide Setup Button

def changeButtonBackgroundColor(button, color):
    cmds.button(button, edit=True, backgroundColor = color)

def toggleButtonColor(buttons, targetButton, color):
    for btn in buttons:
        changeButtonBackgroundColor(btn, [0.5, 0.5, 0.5])
    changeButtonBackgroundColor(targetButton, color)
    
def getSideUserInput(buttons):
    side = ""

    for i in buttons:
        buttonColor = cmds.button(i, query = True, backgroundColor= True)
        buttonColorR = round(buttonColor[0], 1)
        buttonColorG = round(buttonColor[1], 1)
        buttonColorB = round(buttonColor[2], 1)
        buttonColorRound = [buttonColorR, buttonColorG, buttonColorB]

        if buttonColorRound == [0, 0.5, 0]:
            side = cmds.button(i, query = True, label = True)

    if side == "Center":
        return "cn"
    elif side == "Right":
        return "r"
    elif side == "Left":
        return "l"

def remapValues(list, min, max, outMin=0, outMax=1):
    remapped_values = [
        outMin + (outMax - outMin) * ((value - min) / (max - min))
        for value in list
    ]
    return remapped_values

#Build the Ribbon
def buildGuidedRibbon(side, baseName):

    createRibbonHirarchy(side, baseName)
    createRibbonCurve(side, baseName)

#create Guide Hirarchy Function
def createGuideHirarchy(side, baseName):
    
    mainGuideGrp = cmds.createNode("transform", name = f"{side}_{baseName}_{GUIDES}_{GROUP}")

    pinGuidesGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Pin{GUIDES}_{GROUP}", parent = mainGuideGrp)

    ctrlGuidesGrp = cmds.createNode("transform", name = f"{side}_{baseName}_ctrl{GUIDES}_{GROUP}", parent = mainGuideGrp)

#create Ribbon Hirarchy Function
def createRibbonHirarchy(side, baseName):

    mainRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Rig_{GROUP}")

    #Pin Grp
    pinRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Pin_{GROUP}", parent = mainRibbonGrp)

    #Curves Grp
    curvesRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_{CURVE}_{GROUP}", parent = mainRibbonGrp)

    #Ctrls Grp
    ctrlRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_{CTRL}_{GROUP}", parent = mainRibbonGrp)

# create the Curve used to build the Surface Patch of the Ribbon
def createRibbonCurve(side, baseName):

    guideLocators = cmds.listRelatives(f"{side}_{baseName}_Pin{GUIDES}_{GROUP}")

    ribbonCurve, ribbonCurveKnots = CurveFunctions.createLinearCurveFromSelection(guideLocators, f"{side}_CenterRibbon_{CURVE}")

    cmds.parent(ribbonCurve, f"{side}_{baseName}_{CURVE}_{GROUP}")

    cmds.rebuildCurve(ribbonCurve, ch = True, rpo = True, rt = 0, end = 1, kr = 0, kcp = False, kep = True, kt = False, spans = len(cmds.listRelatives(f"{side}_{baseName}_ctrl{GUIDES}_{GROUP}")) - 1, d = 3, tol = 0.01) 

    ribbonPins = list()

    cmds.select(clear=True)

    #create pin Locators
    for index, guide in enumerate(guideLocators):
        guideMtrx = cmds.xform(guide, query = True, ws=True, m = True)

        ribbonPin = cmds.spaceLocator(name = f"{side}_{baseName}{index:02d}_pin")[0]

        cmds.xform(ribbonPin, m = guideMtrx, ws = True)

        cmds.parent(ribbonPin, f"{side}_{baseName}_Pin_{GROUP}")

        ribbonPins.append(ribbonPin)


    curveLength = cmds.arclen(ribbonCurve)

    spacing = curveLength / (len(ribbonPins) - 1)

    #position pins along curve
    for index, pin in enumerate(ribbonPins):
        param = index * spacing

        param = remapValues([param], 0, curveLength, 0, 1)[0]

        position = cmds.pointOnCurve(ribbonCurve, parameter = param, position = True, top = True)
        print(position)
        cmds.move(position[0], position[1], position[2], pin, absolute=True)

    cmds.select(clear=True)

    upperCurve  = cmds.duplicate(ribbonCurve, name = f"{side}_UpperRibbon_{CURVE}")[0]
    cmds.setAttr(f"{upperCurve}.translateY", 0.3)

    lowerCurve  = cmds.duplicate(ribbonCurve, name = f"{side}_LowerRibbon_{CURVE}")[0]
    cmds.setAttr(f"{lowerCurve}.translateY", -0.3)

    ribbonSurfacePatch = cmds.loft(upperCurve, lowerCurve, su = 3, sv = 1)
    cmds.rebuildSurface(ribbonSurfacePatch)

    