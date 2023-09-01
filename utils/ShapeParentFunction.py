import maya.cmds as mc


##ShapeParent Function 
def ShapeParent(*args):
    selection = mc.ls(selection=True)
    PosOffset = True

    if(selection):
        mc.parent(selection[0], selection[1], shape=True, relative=PosOffset)
############################