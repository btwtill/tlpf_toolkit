#Module Import
import maya.cmds as cmds
import maya.app as app
import maya.mel as mel
import maya.internal.common.cmd.base
from tlpf_toolkit.curves import CurveFunctions
from tlpf_toolkit.utils import ZeroOffsetFunction
from tlpf_toolkit.mtrx import MatrixZeroOffset

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

    #Tweak Ctrls checkbox
    createTweakCtrls = cmds.checkBox(label="Create Tweak Ctrls", value = False)

    #Space Divider
    cmds.text(label="", height=10)

    setCustomTweakCtrl = cmds.checkBox(label = "Custom Tweak Control Object", value = False, changeCommand = lambda _: toggleAutoBindMesh(customTweakCtrlBtn))

    #Space Divider
    cmds.text(label="", height=10)

    customTweakCtrlBtn = cmds.button(label="Set Custom Tweak Ctrl", height = 30, command = lambda _: updateBindMeshButton(customTweakCtrlBtn), enable = False)

    #Space Divider
    cmds.text(label="", height=10)

    #DO Auto Bind Checkbox
    doAutoBind = cmds.checkBox(label="Bind to Mesh", value = False, changeCommand = lambda _: toggleAutoBindMesh(autoBindMeshBtn))

    #Space Divider
    cmds.text(label="", height=10)

    autoBindMeshBtn = cmds.button(label="Define Bind Mesh", command = lambda _: updateBindMeshButton(autoBindMeshBtn), enable = False)

    #Space Divider
    cmds.text(label="", height=10)

    doMirrorRibbon = cmds.checkBox(label = "Mirror X", value = False)

    #Space Divider
    cmds.text(label="", height=10)

    setCustomCtrl = cmds.checkBox(label = "Custom Control Object", value = False, changeCommand = lambda _: toggleAutoBindMesh(customCtrlBtn))

    #Space Divider
    cmds.text(label="", height=10)

    customCtrlBtn = cmds.button(label="Set Custom Ctrl", height = 30, command = lambda _: updateBindMeshButton(customCtrlBtn), enable = False)

    #Space Divider
    cmds.text(label="", height=10)

    #Build Ribbon Label
    buildRibbonLabel = cmds.text(label="Create Guided Ribbon", height = 20, backgroundColor = [.3, .3, .3])

    #create Guides Button
    buildRibbonButton = cmds.button(label="Build Ribbon", height = 40, command = lambda _: buildGuidedRibbon(getSideUserInput([setLeftSideBtn, setCenterBtn, setRightBtn]), 
                                                                                                         cmds.textField(baseNameTextField, query = True, text = True), 
                                                                                                         cmds.checkBox(createTweakCtrls, query = True, value = True),
                                                                                                         cmds.checkBox(doAutoBind, query = True, value = True),
                                                                                                         cmds.checkBox(doMirrorRibbon, query = True, value = True), 
                                                                                                         cmds.button(autoBindMeshBtn, query = True, label = True),
                                                                                                         cmds.checkBox(setCustomCtrl, query = True, value = True), 
                                                                                                         cmds.button(customCtrlBtn, query = True, label = True),
                                                                                                         cmds.checkBox(setCustomTweakCtrl, query = True, value = True), 
                                                                                                         cmds.button(customTweakCtrlBtn, query = True, label = True)))

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

def updateBindMeshButton(button):
    cmds.button(button, edit = True, label= cmds.ls(selection=True)[0], backgroundColor = [0, 0.5, 0])

def toggleAutoBindMesh(button):
    buttonState = cmds.button(button, query = True, enable = True)
    cmds.button(button, edit = True, enable = not buttonState)

#Build the Ribbon
def buildGuidedRibbon(side, baseName, createTweakCtrls, doBindMesh, doMirrorRibbon, bindMesh, doCustomCtrl, customCtrlObject, doCustomTweakCtrl, customTweakCtrlObject):

    createRibbonHirarchy(side, baseName, createTweakCtrls)
    ribbonPatch = createRibbonCurve(side, baseName)
    createRibbonDeformJoints(side, baseName, createTweakCtrls, doCustomTweakCtrl, customTweakCtrlObject)
    createRibbonControls(side, baseName, ribbonPatch, doCustomCtrl, customCtrlObject)

    if doMirrorRibbon:
        mirroredSide = defineMirroredSideLabel(side)
        mirrorGuides(side, mirroredSide, baseName)

        createRibbonHirarchy(mirroredSide, baseName, createTweakCtrls)
        ribbonPatch = createRibbonCurve(mirroredSide, baseName)
        createRibbonDeformJoints(mirroredSide, baseName, createTweakCtrls, doCustomTweakCtrl, customTweakCtrlObject)
        createRibbonControls(mirroredSide, baseName, ribbonPatch, doCustomCtrl, customCtrlObject)
        cleanMirroredCtrlJoints(mirroredSide, baseName)

    if doBindMesh:
        bindSelectionToRibbonJoints(bindMesh, doMirrorRibbon, createTweakCtrls, defineMirroredSideLabel(side), side, baseName)

    addVisibilityAttributes(side, baseName, doMirrorRibbon, createTweakCtrls, defineMirroredSideLabel(side))

#create Guide Hirarchy Function
def createGuideHirarchy(side, baseName):
    
    mainGuideGrp = cmds.createNode("transform", name = f"{side}_{baseName}_{GUIDES}_{GROUP}")

    pinGuidesGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Pin{GUIDES}_{GROUP}", parent = mainGuideGrp)

    ctrlGuidesGrp = cmds.createNode("transform", name = f"{side}_{baseName}_ctrl{GUIDES}_{GROUP}", parent = mainGuideGrp)

#create Ribbon Hirarchy Function
def createRibbonHirarchy(side, baseName, createTweakCtrls):

    mainRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Rig_{GROUP}")

    #Pin Grp
    pinRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Pin_{GROUP}", parent = mainRibbonGrp)

    #Curves Grp
    curvesRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_{CURVE}_{GROUP}", parent = mainRibbonGrp)

    #Ctrls Grp
    ctrlRibbonGrp = cmds.createNode("transform", name = f"{side}_{baseName}_{CTRL}_{GROUP}", parent = mainRibbonGrp)

    #tweakCtrl
    if createTweakCtrls:
        ribbonTweakCtrlsGrp = cmds.createNode("transform", name = f"{side}_{baseName}_Tweak{CTRL}_{GROUP}",  parent = mainRibbonGrp)

# create the Curve used to build the Surface Patch of the Ribbon
def createRibbonCurve(side, baseName):

    guideLocators = cmds.listRelatives(f"{side}_{baseName}_Pin{GUIDES}_{GROUP}")

    ribbonCurve, ribbonCurveKnots = CurveFunctions.createLinearCurveFromSelection(guideLocators, f"{side}_{baseName}_CenterRibbon_{CURVE}")

    cmds.parent(ribbonCurve, f"{side}_{baseName}_{CURVE}_{GROUP}")

    print(ribbonCurve, side)

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

    upperCurve  = cmds.duplicate(ribbonCurve, name = f"{side}_{baseName}_UpperRibbon_{CURVE}")[0]
    cmds.setAttr(f"{upperCurve}.translateY", 0.3)

    lowerCurve  = cmds.duplicate(ribbonCurve, name = f"{side}_{baseName}__LowerRibbon_{CURVE}")[0]
    cmds.setAttr(f"{lowerCurve}.translateY", -0.3)

    ribbonSurfacePatch = cmds.loft(lowerCurve, upperCurve, ch = 1, u = 1, c = 0, ar = 1, d = 3, ss = 1, rn = 0, po = 0, rsn = True, name = f"{side}_{baseName}_SurfacePatch")[0]
    cmds.rebuildSurface(ribbonSurfacePatch, sv = 1, su = len(cmds.listRelatives(f"{side}_{baseName}_ctrl{GUIDES}_{GROUP}")) - 1, du = 3, dv = 1)

    cmds.select(clear=True)
    cmds.select(ribbonSurfacePatch)
    cmds.select(cmds.listRelatives(f"{side}_{baseName}_Pin_{GROUP}"), add = True)

    maya.internal.common.cmd.base.executeCommand('uvpin.cmd_create')
    cmds.select(clear=True)

    cmds.parent(ribbonSurfacePatch, f"{side}_{baseName}_{CURVE}_{GROUP}")

    return ribbonSurfacePatch

# create and organize the deformation joints of the ribbon
def createRibbonDeformJoints(side, baseName, createTweakCtrls, doCustomTweakCtrl, customTweakCtrlObject):

    pins = cmds.listRelatives(f"{side}_{baseName}_Pin_{GROUP}")

    
    for index, pin in enumerate(pins):

        if not createTweakCtrls:
            cmds.select(clear=True)
            cmds.select(pin)
            newSkinJoint = cmds.joint(name = f"{side}_{baseName}{index:02d}_{SKIN}")
        else:
            pinMatrix = cmds.xform(pin, q = True, m = True, worldSpace = True)

            if doCustomTweakCtrl:
                newCtrl = cmds.duplicate(customTweakCtrlObject, name = f"{side}_{baseName}Tweak{index:02d}_{CTRL}")[0]

                for channel in "XYZ":
                    cmds.setAttr(f"{newCtrl}.translate{channel}", 0)
                    cmds.setAttr(f"{newCtrl}.rotate{channel}", 0)
                    cmds.setAttr(f"{newCtrl}.scale{channel}", 1)
            else:
                newCtrl = cmds.circle(name = f"{side}_{baseName}Tweak{index:02d}_{CTRL}")[0]

            cmds.xform(newCtrl, m = pinMatrix, worldSpace=True)
            cmds.parent(newCtrl, pin)

            cmds.select(clear = True)
            cmds.select(newCtrl)
            zeroNode = ZeroOffsetFunction.insertNodeBefore(sfx = "_zro")[0]
        
            cmds.select(clear = True)
            cmds.select(newCtrl)
            MatrixZeroOffset.createMatrixZeroOffset(newCtrl)

            cmds.select(clear=True)

            cmds.parent(newCtrl, f"{side}_{baseName}_Tweak{CTRL}_{GROUP}")

            cmds.select(clear=True)

            cmds.select(newCtrl)
            newSkinJoint = cmds.joint(name = f"{side}_{baseName}{index:02d}_{SKIN}")

#create the ctrl Joints, transforms and ctrls
def createRibbonControls(side, baseName, surfacePatch, doCustomCtrl, customCtrlObject):
    ctrlGuides = cmds.listRelatives(f"{side}_{baseName}_ctrl{GUIDES}_{GROUP}")

    ctrlJoints = list()

    for index, ctrl in enumerate(ctrlGuides):
        guideMatrix = cmds.xform(ctrl, query = True, m = True, worldSpace= True)

        cmds.select(clear= True)

        newCtrlJoint = cmds.joint(name = f"{side}_{baseName}Ctrl{index:02d}_{JOINT}")
        cmds.setAttr(f"{newCtrlJoint}.radius", 1.5)
        ctrlJoints.append(newCtrlJoint)

        if doCustomCtrl:
            newCtrl = cmds.duplicate(customCtrlObject, name = f"{side}_{baseName}{index:02d}_{CTRL}")[0]

            for channel in "XYZ":
                cmds.setAttr(f"{newCtrl}.translate{channel}", 0)
                cmds.setAttr(f"{newCtrl}.rotate{channel}", 0)
                cmds.setAttr(f"{newCtrl}.scale{channel}", 1)
        else:
            newCtrl = cmds.circle(name = f"{side}_{baseName}{index:02d}_{CTRL}")[0]

        cmds.parent(newCtrlJoint, newCtrl)
        cmds.xform(newCtrl, m = guideMatrix, ws = True)
        cmds.parent(newCtrl, f"{side}_{baseName}_{CTRL}_{GROUP}")

        cmds.select(clear=True)
        cmds.select(newCtrl)
        ZeroOffsetFunction.insertNodeBefore(sfx= "_zro")

        cmds.select(clear=True)
        cmds.select(newCtrl)
        ZeroOffsetFunction.insertNodeBefore(sfx= "_const")

        cmds.select(clear=True)
        cmds.select(newCtrl)
        ZeroOffsetFunction.insertNodeBefore(sfx= "_off")

    cmds.select(clear= True)

    cmds.select(ctrlJoints)
    cmds.select(surfacePatch, add = True)

    maya.internal.common.cmd.base.executeCommand('skincluster.cmd_create')

#get the prefix for the mirrored Side Names  
def defineMirroredSideLabel(side):
    if side == "l":
        return "r"
    if side == "r":
        return "l"

#mirror The Guides in world X  
def mirrorGuides(side, mirrorSide, baseName):

    mainGroup = f"{side}_{baseName}_{GUIDES}_{GROUP}"

    mainMirrorGroup = cmds.duplicate(mainGroup)[0]

    print(mainMirrorGroup)

    cmds.select(clear = True)
    cmds.select(mainMirrorGroup)
    
    mel.eval('searchReplaceNames "{}_" "{}_" "hierarchy"'.format(side, mirrorSide))
    mainMirrorGroup = cmds.rename(f"{mirrorSide}_{baseName}_{GUIDES}_{GROUP}1", f"{mirrorSide}_{baseName}_{GUIDES}_{GROUP}")

    print(mainMirrorGroup)

    tmpMirrorGrp = cmds.createNode("transform", name = f"{baseName}_TmpMirroGrp")
    cmds.parent(mainMirrorGroup, tmpMirrorGrp)

    cmds.setAttr(f"{tmpMirrorGrp}.scaleX", -1)
    cmds.parent(mainMirrorGroup, world=True)
    cmds.delete(tmpMirrorGrp)

#selecte the Deformation Joints
def SelectDeformationJoints(mirrored, createTweakCtrls, mirroredSide, side, baseName):

    if not mirrored:
        if createTweakCtrls:
            skinjoints = cmds.listRelatives(f"{side}_{baseName}_Tweak{CTRL}_{GROUP}")
            cmds.select(clear = True)
            cmds.select(skinjoints)
            cmds.pickWalk(direction="Down")
            cmds.pickWalk(direction="right")
        else:
            skinjoints = cmds.listRelatives(f"{side}_{baseName}_Pin_{GROUP}")
            cmds.select(clear = True)
            cmds.select(skinjoints)
            cmds.pickWalk(direction="Down")
            cmds.pickWalk(direction="right")
    else:
        if createTweakCtrls:
            skinJointsSide01 = cmds.listRelatives(f"{side}_{baseName}_Tweak{CTRL}_{GROUP}")
            skinJointsSide02 = cmds.listRelatives(f"{mirroredSide}_{baseName}_Tweak{CTRL}_{GROUP}")

            cmds.select(clear = True)
            cmds.select(skinJointsSide01)
            cmds.select(skinJointsSide02, add = True)

            cmds.pickWalk(direction="Down")
            cmds.pickWalk(direction="right")
        else:
            skinJointsSide01 = cmds.listRelatives(f"{side}_{baseName}_Pin_{GROUP}")
            skinJointsSide02 = cmds.listRelatives(f"{mirroredSide}_{baseName}_Pin_{GROUP}")

            cmds.select(clear = True)
            cmds.select(skinJointsSide01)
            cmds.select(skinJointsSide02, add = True)
            cmds.pickWalk(direction="Down")
            cmds.pickWalk(direction="right")

#bin selected Geometry to the Deformation Joints
def bindSelectionToRibbonJoints(bindMesh, doMirrorRibbon, createTweakCtrls, mirrorSide, side, baseName):

    SelectDeformationJoints(doMirrorRibbon, createTweakCtrls, mirrorSide, side, baseName)

    cmds.select(bindMesh, add=True)

    skinCluster = maya.internal.common.cmd.base.executeCommand('skincluster.cmd_create')

    cmds.select(clear=True)

#adding extra attribute to main Group and Hide all mechanism parts of the ribbon
def addVisibilityAttributes(side, baseName, doMirrorRibbon, createTweakCtrls, mirroredSide):

    cmds.addAttr(f"{side}_{baseName}_Rig_{GROUP}", at= "float", ln = f"{baseName}_MechanismVisibility", min = 0, max = 1, dv = 0)
    cmds.connectAttr(f"{side}_{baseName}_Rig_{GROUP}.{baseName}_MechanismVisibility", f"{side}_{baseName}_{CURVE}_{GROUP}.visibility")

    cmds.select(clear=True)
    SelectDeformationJoints(doMirrorRibbon, createTweakCtrls, mirroredSide, side, baseName)

    deformationJoints = cmds.ls(selection=True)
    cmds.select(clear=True)

    for jnt in deformationJoints:
        cmds.connectAttr(f"{side}_{baseName}_Rig_{GROUP}.{baseName}_MechanismVisibility", f"{jnt}.visibility")

    pins = cmds.listRelatives(f"{side}_{baseName}_Pin_{GROUP}")

    for pin in pins:
        cmds.connectAttr(f"{side}_{baseName}_Rig_{GROUP}.{baseName}_MechanismVisibility", f"{pin}.visibility")


    ctrlJointsMainSide = getCtrlJoints(side, baseName)
    for jnt in ctrlJointsMainSide:
        cmds.connectAttr(f"{side}_{baseName}_Rig_{GROUP}.{baseName}_MechanismVisibility", f"{jnt}.visibility")


    if doMirrorRibbon:

        cmds.connectAttr(f"{side}_{baseName}_Rig_{GROUP}.{baseName}_MechanismVisibility", f"{mirroredSide}_{baseName}_{CURVE}_{GROUP}.visibility")

        pins = cmds.listRelatives(f"{mirroredSide}_{baseName}_Pin_{GROUP}")

        for pin in pins:
            cmds.connectAttr(f"{side}_{baseName}_Rig_{GROUP}.{baseName}_MechanismVisibility", f"{pin}.visibility")
        
        ctrlJointsMirroredSide = getCtrlJoints(mirroredSide, baseName)

        for jnt in ctrlJointsMirroredSide:
            cmds.connectAttr(f"{side}_{baseName}_Rig_{GROUP}.{baseName}_MechanismVisibility", f"{jnt}.visibility")
    
#get all the Ctrl Joints in the Ribbon
def getCtrlJoints(side, baseName):

    ctrlJoints = list()

    ctrlHirarchysMainSide = cmds.listRelatives(f"{side}_{baseName}_{CTRL}_{GROUP}")

    for obj in ctrlHirarchysMainSide:
        ctrlJoints.append(cmds.listRelatives(obj, allDescendents=True)[1])

    return ctrlJoints

#set the Rotation value for ctrl and Constraint node to 0
def cleanMirroredCtrlJoints(side, baseName):

    ctrlsNode = list()
    constNode = list()

    ctrlHirarchysMainSide = cmds.listRelatives(f"{side}_{baseName}_{CTRL}_{GROUP}")

    for obj in ctrlHirarchysMainSide:
        ctrlsNode.append(cmds.listRelatives(obj, allDescendents=True)[2])
        constNode.append(cmds.listRelatives(obj, allDescendents=True)[-1])

    print(ctrlsNode, constNode)
    for index, node in enumerate(ctrlsNode):
        cmds.setAttr(f"{node}.rotateZ", 0) ############## Needs adjustment if Mirror side ever should change from Mirror X to Y OR Z
        cmds.setAttr(f"{constNode[index]}.rotateZ", 0) ############## Needs adjustment if Mirror side ever should change from Mirror X to Y OR Z


##TODO
##Forward Visibility Attribute for Tweak and Main Ctrls to Main Grp