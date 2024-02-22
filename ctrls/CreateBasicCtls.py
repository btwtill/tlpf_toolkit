#Module Import
import maya.cmds as cmds
import logging


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

#=======================================
## Basic Ctrl Function
#=======================================

def CreateCircleCtrlsHirarchyUserInput():
    sel = cmds.ls(selection = True)
    CreateCircleCtrlsHirarchy(sel)

def CreateCircleCtrlsUserInput():
    sel = cmds.ls(selection = True)
    CreateCircleCtrls(sel)

def CreateCircleCtrlsHirarchy(inputList):
    ctrlList = []
    for input in inputList:
        translation = cmds.xform(input, q=True, ws=True, t=True)
        rotation = cmds.xform(input, q=True, ws=True, rotation=True)
        
        newCtrl = cmds.circle(name=f"{input}_ctrl")
        
        cmds.setAttr(newCtrl[0]+'.translate', *translation)
        cmds.setAttr(newCtrl[0] + '.rotate', *rotation)
        ctrlList.append(newCtrl)
        
    ctrlList = list(reversed(ctrlList))
    for i in range(len(ctrlList)):
        if i != (len(ctrlList) - 1):
            cmds.parent(ctrlList[i], ctrlList[i + 1])

    #Response 
    log.info(f"Created Ctrls: {ctrlList}")
    #Return the Ctrl Hirarchy
    return ctrlList

def CreateCircleCtrls(inputList):
    #output List
    ctrlList = []

    for input in inputList:
        translation = cmds.xform(input, q=True, ws=True, t=True)
        rotation = cmds.xform(input, q=True, ws=True, rotation=True)
        
        newCtrl = cmds.circle(name=f"{input}_ctrl")
        
        cmds.setAttr(newCtrl[0]+'.translate', *translation)
        cmds.setAttr(newCtrl[0] + '.rotate', *rotation)
        ctrlList.append(newCtrl)

    #Response
    log.info(f"Created Ctrls: {ctrlList}")
    #return List
    return ctrlList
        

#=======================================
## Basic Ctrl Function - END
#=======================================