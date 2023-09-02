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