import maya.cmds as cmds

from tlpf_toolkit import global_variables
import logging
import os
from tlpf_toolkit.ctrlShapes import utils

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


#=======================================
## Scale Mirroring
#=======================================

def MirrorCtrlsBehaviorUserInput():
    userInput = cmds.ls(sl=True)
    MirrorCtrlsBehavior(userInput)

def MirrorCtrlsBehavior(input):
    
    for i in input:
        dup = cmds.duplicate(i)

        try:
            cmds.parent(dup[0], world = True)
        except:
            pass

        mirrorGrp = cmds.group(empty=True, world=True, name="tmpMirrorGrp")
        
        cmds.parent(dup[0], mirrorGrp)

        cmds.setAttr(mirrorGrp + ".scaleX", -1)

        cmds.parent(dup[0], world = True)
        
        cmds.delete(mirrorGrp)
#=======================================
## Scale Mirroring - End
#=======================================


#=======================================
## Behaviour Mirroring
#=======================================


def fetchMirrorCtrlSelectionData(doReparent, searchTerm, replaceTerm):
    userInput = cmds.ls(sl=True)
    
    mirrorCtrlsBehavior(userInput, doReparent, direction = "YZ", searchTerm = searchTerm, replaceTerm = replaceTerm)

def mirrorCtrlsJointsMethodUI():
    #window
    configWindow = cmds.window(title="MirrorCtrls", iconName = "mirrorCtrls", widthHeight=(200, 180), sizeable=True)

    #window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Mirror your Ctrls", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    #Reparent CheckBox
    reparentCheckbox = cmds.checkBox(label = "Reparent Mirrored Ctrls", value = False)

    #SpaceDivider

    cmds.text(label="", height=10)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])
    cmds.text(label = "Search Term", width = 150, height = 20, backgroundColor = [.3, .3, .3])
    cmds.text(label = "replace Term", width = 150, height = 20, backgroundColor = [.3, .3, .3])
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])
    searchTermInput = cmds.textField(width=150)
    replaceTermInput = cmds.textField(width = 150)
    cmds.setParent('..')

    cmds.rowColumnLayout(adjustableColumn=True)

    #SpaceDivider
    cmds.text(label="", height=10)

    #Create constraints Button
    matrixConstraintToJointsBuild = cmds.button(label = "Mirror Ctrls", command = lambda _: fetchMirrorCtrlSelectionData(cmds.checkBox(reparentCheckbox, query = True, value = True),
                                                                                                                        cmds.textField(searchTermInput, query= True, text = True),
                                                                                                                        cmds.textField(replaceTermInput, query = True, text = True)))

    #display Window 
    cmds.showWindow(configWindow)

def mirrorCtrlsBehavior(input, reparent = False, direction = "YZ", searchTerm = "L", replaceTerm = "R", ):
    mirroredCtrls = []
    for index, ctrl in enumerate(input):
        print(searchTerm, ctrl)
        print(searchTerm in ctrl)
        if searchTerm in ctrl:
            newTransform = cmds.createNode("transform", name = f"{ctrl.replace(searchTerm, replaceTerm)}")
        else:
            newTransform = cmds.createNode("transform", name = f"{ctrl}_otherSide")
            
        cmds.select(clear=True)
        
        newJoint = cmds.joint(name = "tmp_mirrorJoint")
        
        cmds.select(clear=True)
        
        cmds.matchTransform(newJoint, ctrl)
        
        mirroredJoint = cmds.mirrorJoint(newJoint, mirrorBehavior = True, mirrorYZ = True)
        
        cmds.matchTransform(newTransform, mirroredJoint)
        
        dup = cmds.duplicate(ctrl, renameChildren = True)[0]
        try:
            duplicateRelatives = cmds.listRelatives(dup, children = True)[1]
        except:
            duplicateRelatives = None

        if cmds.nodeType(duplicateRelatives) != "nurbsCurve":
            if duplicateRelatives != None:
                cmds.delete(duplicateRelatives)
            
        cmds.select(clear=True)
        try:
            cmds.parent(dup, world=True)
        except:
            log.info(f"Already Child of the World")

        cmds.select(clear=True)
        
        dupShape = cmds.listRelatives(dup, shapes = True)
        print(type(dupShape))
        print(dupShape)

        for shape in dupShape:
            cmds.parent(shape, newTransform, shape=True, relative=True)
            
        cmds.delete(mirroredJoint)
        cmds.delete(newJoint)
        cmds.delete(dup)
        cmds.select(clear=True)
        
        for channel in "XYZ":
            cmds.setAttr(f"{newTransform}.scale{channel}", -1)
        
        cmds.makeIdentity(newTransform, apply = True, t = False, r=False, s = True, n = False, pn = True)
        
        mirroredCtrls.append(newTransform)
        
        if reparent:
            try:
                cmds.parent(newTransform, mirroredCtrls[index -1])
                print("reparented")
            except:
                print("No Parent ctrl selected")

#=======================================
## Behaviour Mirroring - End
#=======================================