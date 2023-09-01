import maya.cmds as mc


#=======================================
##Shape Parent
#=======================================

def ShapeParent(*args):
    selection = mc.ls(selection=True)
    PosOffset = True

    if(selection):
        mc.parent(selection[0], selection[1], shape=True, relative=PosOffset)

#=======================================
##Shape Parent - END
#=======================================