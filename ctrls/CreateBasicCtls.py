#Module Import
import maya.cmds as cmds


#=======================================
## Basic Ctrl Function
#=======================================
def CreateCircleCtrls():

    sel = cmds.ls(selection=True)

    ctrlList = []
    for i in sel:
        translation = cmds.xform(i, q=True, ws=True, t=True)
        rotation = cmds.xform(i, q=True, ws=True, rotation=True)
        
        newCtrl = cmds.circle(name=i)
        
        cmds.setAttr(newCtrl[0]+'.translate', *translation)
        cmds.setAttr(newCtrl[0] + '.rotate', *rotation)
        ctrlList.append(newCtrl)
        
    ctrlList = list(reversed(ctrlList))
    for i in range(len(ctrlList)):
        if i != (len(ctrlList) - 1):
            cmds.parent(ctrlList[i], ctrlList[i + 1])
#=======================================
## Basic Ctrl Function - END
#=======================================