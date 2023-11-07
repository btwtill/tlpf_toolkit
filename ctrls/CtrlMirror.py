import maya.cmds as cmds


def MirrorCtrlsBehavior():
    
    for i in cmds.ls(selection=True):
        dup = cmds.duplicate(i)

        try:
            cmds.parent(dup[0], world = True)
        except:
            pass

        mirrorGrp = cmds.group(empty=True, world=True, name="tmpMirrorGrp")
        
        cmds.parent(dup[0], mirrorGrp)

        cmds.setAttr(mirrorGrp + ".scaleX", -1)

        cmds.parent(dup[0], world = True)
        
        cmds.delete(mirrorGrp)

        