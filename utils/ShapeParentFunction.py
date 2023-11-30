#Module Import
import maya.cmds as cmds


#=======================================
##Shape Parent
#=======================================

def ShapeParent(*args):
    selection = cmds.ls(selection=True)
    PosOffset = True

    if(selection):
        cmds.parent(selection[0], selection[1], shape=True, relative=PosOffset)

#=======================================
##Shape Parent - END
#=======================================


#=======================================
##Shape Replace
#=======================================

def ShapeReplace():
    sel = cmds.ls(selection = True)

    targetShapeName = cmds.listRelatives(sel[1], shapes = True)[0]
    cmds.select(clear=True)
    cmds.select(sel[0])
    cmds.pickWalk(direction="down")
    cmds.select(sel[1], add = True)

    selection = cmds.ls(selection=True)
    PosOffset = True

    if(selection):
        cmds.parent(selection[0], selection[1], shape=True, relative=PosOffset)

    cmds.delete(targetShapeName)


#=======================================
##Shape Replace - END
#=======================================