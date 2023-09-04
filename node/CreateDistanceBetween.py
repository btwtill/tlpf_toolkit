#Module Import
import maya.cmds as cmds


#=======================================
## Create Distance between Function
#=======================================
def createDistance():
    sel = cmds.ls(selection=True)

    distNode = cmds.rename(cmds.createNode("distanceBetween"), "distanceBetween_" + sel[0] + "_" + sel[1])

    cmds.connectAttr(sel[0] + ".worldMatrix[0]", distNode + ".inMatrix1")
    cmds.connectAttr(sel[1] + ".worldMatrix[0]", distNode + ".inMatrix2")
#=======================================
## Create Distance between Function - END
#=======================================