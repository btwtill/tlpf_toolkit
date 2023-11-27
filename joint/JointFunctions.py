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
## Corrective Joints Setup V001
#=======================================


def correctivejointSystemUI():

    #basic Window creation
    configWindow = cmds.window(title="CorrectiveSystemV01", iconName='Corrective', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.columnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Corrective Setup Tool", height = 30, backgroundColor = [.5, .5, .5])

    #Manual Guides Label
    baseNameLabel = cmds.text(label="Set Base Name", height = 20, backgroundColor = [.3, .3, .3])

    #Base Name Label
    baseNameTextField = cmds.textField()

    #Space Divider
    cmds.text(label="", height=10)

    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])
    
    restPoseLabel = cmds.text(label = "REST Pose: ", width = 100)
    posePoseLabel = cmds.text(label ="Posed Pose: ", width = 100)
    correctedPoseLabel = cmds.text(label = "Corrected Pose: ", width = 100)

    cmds.setParent('..')

    #define Start pos
    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])

    startPosBtn = cmds.button(label="REST", width = 100, command = lambda _: toggleLocButton(startPosBtn, "restPosLoc", [0, 0.5, 0]))
    posedPosBtn = cmds.button(label="POSE", width = 100, command = lambda _: toggleLocButton(posedPosBtn, "posedPosLoc", [0, 0.5, 0]))
    correctedPosBtn = cmds.button(label="CORRECTED", width = 100, command = lambda _: toggleLocButton(correctedPosBtn, "correctedPosLoc", [0, 0.5, 0]))

    cmds.setParent('..')
    cmds.columnLayout(adjustableColumn=True)

    #Space Divider
    cmds.text(label="", height=10)

    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])

    targetLabel = cmds.text(label ="Target Object: ", width = 100)
    followLabel = cmds.text(label ="Follow Object: ", width = 100)
    parentLabel = cmds.text(label = "Parent Object: ", width = 100)

    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])

    #set Target
    targetObject = cmds.button(label = "Set", width = 100, command = lambda _: toggleDefButton(targetObject, [0, 0.5, 0]))

    #set Parent
    followObject = cmds.button(label = "Set ", width = 100, command = lambda _: toggleDefButton(followObject, [0, 0.5, 0]))

    parentObject = cmds.button(label = "Set ", width = 100, command = lambda _: toggleDefButton(parentObject, [0, 0.5, 0]))
    cmds.setParent('..')

    cmds.columnLayout(adjustableColumn=True)

    #Space Divider
    cmds.text(label="", height=10)

    #Build Ribbon Label
    buildCorrectiveSystemLabel = cmds.text(label="Create Corrective System", height = 20, backgroundColor = [.3, .3, .3])

    #create Guides Button
    buildSystemButton = cmds.button(label="Build System", height = 40, command = lambda _: buildCorrectiveSystem(cmds.textField(baseNameTextField, query = True, text = True),
                                                                                                                 cmds.button(startPosBtn, query = True, label = True),
                                                                                                                 cmds.button(posedPosBtn, query = True, label = True),
                                                                                                                 cmds.button(correctedPosBtn, query = True, label = True),
                                                                                                                 cmds.button(targetObject, query=True, label = True),
                                                                                                                 cmds.button(followObject, query = True, label = True),
                                                                                                                 cmds.button(parentObject, query = True, label = True)))
 
    
    #show Window
    cmds.showWindow(configWindow)

def toggleLocButton(button, locName, color):
    pos = cmds.ls(selection = True)[0]

    posMatrix = cmds.xform(pos, query = True, ws=True, m = True)

    newLoc = cmds.spaceLocator(name = f"{pos}_{locName}")[0]

    cmds.xform(newLoc, m = posMatrix, ws = True)

    cmds.button(button, edit = True, label = f"{newLoc}")
    cmds.button(button, edit = True, backgroundColor = color)

def toggleDefButton(button, color):

    sel = cmds.ls(selection = True)[0]

    cmds.button(button, edit = True, label = sel)
    cmds.button(button, edit = True, backgroundColor = color)

def buildCorrectiveSystem(baseName, followLoc, referenceLoc, correctedLoc, targetObject,followObject, parentObject):
    print(baseName, followLoc, referenceLoc, correctedLoc, targetObject, followObject, parentObject)