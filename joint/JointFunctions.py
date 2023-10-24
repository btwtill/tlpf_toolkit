#Module Import
import logging

from maya import cmds

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


#=======================================
## Create Joints at selected Pos
#=======================================
def CreateJointsOnSelected():
    targetList = cmds.ls(selection=True, flatten=True)
    if targetList:
        for i in targetList:
            cmds.select(clear=True)
            targetPos = cmds.xform(i, ws=True, query=True, translation=True)
            targetRot = cmds.xform(i, ws=True, query=True, rotation=True)
            targetScl = cmds.xform(i, ws=True, query=True, scale=True)

            newJoint = cmds.joint()

            cmds.setAttr(newJoint + ".translate", targetPos[0], targetPos[1], targetPos[2])
            cmds.setAttr(newJoint + ".rotate", targetRot[0], targetRot[1], targetRot[2])
            cmds.setAttr(newJoint + ".scale", targetScl[0], targetScl[1], targetScl[2])
            
    else:
        log.error("no Objects Selected")
        raise
#=======================================
## Create Joints at selected Pos - END
#=======================================


#=======================================
## Move Joints Tranforms to Parent Matrix Offset
#=======================================

def MoveJointSRTtoParentMatirxOffset():
    sel = cmds.ls(selection =True)

    for i in sel:
        
        cmds.connectAttr(i + ".matrix" , i + ".offsetParentMatrix")
        cmds.disconnectAttr(i + ".matrix" , i + ".offsetParentMatrix")

        for j in "XYZ":
            cmds.setAttr(i + ".translate" + j, 0)
            
            cmds.setAttr(i + ".rotate" + j, 0)
            cmds.setAttr(i + ".jointOrient" + j, 0)

            cmds.setAttr(i + ".scale" + j, 1)
