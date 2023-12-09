#Module Import
import maya.cmds as cmds


#=======================================
## Matrix Node Zero Offset
#=======================================
def iterateCreateMatrixZeroOffset():
    sel = cmds.ls(selection=True)
    for i in sel:
        cmds.select(clear=True)
        cmds.select(i)
        createMatrixZeroOffset(sel[i])
    


def createMatrixZeroOffset(sel):
    #zero Node Input
    zro_node = cmds.pickWalk(direction="up")
    
    #get parent Node Input
    parent_node = cmds.listRelatives(zro_node, parent=True)
    
    
    #create zro Matrix
    zro_mtrx = cmds.rename(cmds.createNode("composeMatrix"), zro_node[0] + "_mtrx")
    
    #set translation
    cmds.setAttr(zro_mtrx + ".inputTranslateX", cmds.getAttr(zro_node[0] + ".translateX"))
    cmds.setAttr(zro_mtrx + ".inputTranslateY", cmds.getAttr(zro_node[0] + ".translateY"))
    cmds.setAttr(zro_mtrx + ".inputTranslateZ", cmds.getAttr(zro_node[0] + ".translateZ"))
    
    #set rotation
    cmds.setAttr(zro_mtrx + ".inputRotateX", cmds.getAttr(zro_node[0] + ".rotateX"))
    cmds.setAttr(zro_mtrx + ".inputRotateY", cmds.getAttr(zro_node[0] + ".rotateY"))
    cmds.setAttr(zro_mtrx + ".inputRotateZ", cmds.getAttr(zro_node[0] + ".rotateZ"))
    
    #set scale
    cmds.setAttr(zro_mtrx + ".inputScaleX", cmds.getAttr(zro_node[0] + ".scaleX"))
    cmds.setAttr(zro_mtrx + ".inputScaleY", cmds.getAttr(zro_node[0] + ".scaleY"))
    cmds.setAttr(zro_mtrx + ".inputScaleZ", cmds.getAttr(zro_node[0] + ".scaleZ"))
    
    #create multMatrix
    mult_mtrx = cmds.rename(cmds.createNode("multMatrix"), zro_mtrx + "_mult")
    
    #connect zro mtrx to multMatrix
    cmds.connectAttr(zro_mtrx + ".outputMatrix", mult_mtrx + ".matrixIn[0]")
    
    #connect parent worldmatrix to mult matirx 
    if parent_node:
        cmds.connectAttr(parent_node[0] + ".worldMatrix[0]", mult_mtrx + ".matrixIn[1]")
    else:
        origin_mtrx = cmds.rename(cmds.createNode("composeMatrix"), "Origin_mtrx")
        cmds.connectAttr(origin_mtrx + ".outputMatrix", mult_mtrx + ".matrixIn[1]")
    
    #connect outmatrix to selected transform
    cmds.connectAttr(mult_mtrx + ".matrixSum", sel + ".offsetParentMatrix")
    
    #unparent selected transform 
    cmds.parent(sel, world=True)
    
    cmds.delete(zro_node)
    
    #zero out selected transforms transfrom channels
    cmds.setAttr(sel + ".translateX", 0)
    cmds.setAttr(sel + ".translateY", 0)
    cmds.setAttr(sel + ".translateZ", 0)
    
    cmds.setAttr(sel + ".rotateX", 0)
    cmds.setAttr(sel + ".rotateY", 0)
    cmds.setAttr(sel + ".rotateZ", 0)
    
    cmds.setAttr(sel + ".scaleX", 1)
    cmds.setAttr(sel + ".scaleY", 1)
    cmds.setAttr(sel + ".scaleZ", 1)
#=======================================
## Matrix Node Zero Offset - END
#=======================================



