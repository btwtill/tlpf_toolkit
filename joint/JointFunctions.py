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

def MoveJointSRTtoParentMatrixOffset():
    sel = cmds.ls(selection =True)

    for i in sel:
        
        cmds.connectAttr(i + ".matrix" , i + ".offsetParentMatrix")
        cmds.disconnectAttr(i + ".matrix" , i + ".offsetParentMatrix")

        for j in "XYZ":
            cmds.setAttr(i + ".translate" + j, 0)
            
            cmds.setAttr(i + ".rotate" + j, 0)
            cmds.setAttr(i + ".jointOrient" + j, 0)

            cmds.setAttr(i + ".scale" + j, 1)


#=======================================
## Move Joints Tranforms to Parent Matrix Offset - END
#=======================================


#=======================================
## Clear Joint Orient Values
#=======================================

def ClearJointOrientValues():

    for i in cmds.ls(selection = True):
        for j in "XYZ":
            cmds.setAttr(i + ".jointOrient" + j, 0)

#=======================================
## Clear Joint Orient Values - END
#=======================================



#=======================================
## Clear Joint Orient Values Internal
#=======================================

def ClearJointOrientValuesInternal(targets):

    for i in targets:
        for j in "XYZ":
            cmds.setAttr(i + ".jointOrient" + j, 0)

#=======================================
## Clear Joint Orient Values Internal - END
#=======================================


#=======================================
## Build Forward Joint Chain form Selection 
#=======================================
            
def buildForwardJointChain(joints, doFreeze):

    for index, jnt in enumerate(joints):
        if index != 0:
            cmds.parent(jnt, joints[index - 1])
    if doFreeze:
        for i in joints:
            cmds.makeIdentity(i, apply =True, pn =True, n = True)

#=======================================
## Build Forward Joint Chain form Selection - End
#=======================================
            
#=======================================
## Convert Guides to Joint Chain
#=======================================
            
def convertGuidesToJointChain(guides, replaceTerm = "_drv", searchTerm = "_guide"):
    newJoints = []
    for index, guide in enumerate(guides):
        newJointMatrix = cmds.xform(guide, query = True, m =True, ws = True)
        newJoint = cmds.joint(name = guide.replace(searchTerm, replaceTerm))

        cmds.select(clear = True)
        cmds.xform(newJoint, m = newJointMatrix, ws = True)
        newJoints.append(newJoint)
    
    buildForwardJointChain(newJoints, True)

    return newJoints

#=======================================
## Convert Guides to Joint Chain -END
#=======================================


#=======================================
## Convert Guides to individual Joints
#=======================================

def convertGuidesToIndividualJoints(guides, targetLocation = "World",searchTerm = "_guide", replaceTerm = "_skn", radius = 1):
    joints = []
    
    for guide in guides:
        worldMatrix = cmds.xform(guide, query = True, ws = True, m =True)
        cmds.select(clear=True)
        newJoint = cmds.joint(name = guide.replace(searchTerm, replaceTerm))
        cmds.xform(newJoint, m = worldMatrix, ws = True)
        cmds.setAttr(f"{newJoint}.radius", radius)
        cmds.parent(newJoint, targetLocation)
        joints.append(newJoint)
    return joints

#=======================================
## Convert Guides to individual Joints - END
#=======================================