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

#=======================================
## Create Joints at Selected SRT with Names
#=======================================

def copyJointsReplaceNameUI():
    #window
    configWindow = cmds.window(title="Copy Joints with Name", iconName = "CopyJoints", widthHeight=(200, 300), sizeable=True)

    #window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="CopyJoints and Replace String", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
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

    #Space Divider
    cmds.text(label="", height=10)
    

    #Create pairBlends Button
    copyJointsButton = cmds.button(label = "CopyJoints", command = lambda _: copyJointsReplaceName(cmds.ls(sl=True),
                                                                                                   cmds.textField(searchTermInput, query =True, text=True),
                                                                                                   cmds.textField(replaceTermInput, query = True, text = True)))

    #display Window 
    cmds.showWindow(configWindow)

def copyJointsReplaceName(pos, searchTerm, replaceTerm):

    for index, item in enumerate(pos):
        matrixPos = cmds.xform(item, query = True, ws= True, m = True)
        
        cmds.select(clear=True)
        newJoint = cmds.joint(name = item.replace(searchTerm, replaceTerm))
        
        cmds.xform(newJoint, m = matrixPos, ws =True)
        cmds.makeIdentity(newJoint, apply=True, t = True, r=True, s = True, n = False, pn = True)

#=======================================
## Create Joints at Selected SRT with Names - END
#=======================================