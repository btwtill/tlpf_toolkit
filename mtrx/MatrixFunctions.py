#Module Import
import maya.cmds as cmds


def resetOffsetParentMatrix():
    sel = cmds.ls(selection=True)

    for i in sel:
        tmpLoc = cmds.spaceLocator(name = f"{i}_tmpmatrix")[0]
        tmpmatrix = cmds.xform(i, query = True, m = True, ws=True)
        cmds.xform(tmpLoc, m = tmpmatrix, ws =True)
        identity = cmds.createNode("composeMatrix", name = f"{i}_tmpIdentityMatrix")
        cmds.connectAttr(f"{identity}.outputMatrix", f"{i}.offsetParentMatrix", force=True)
        
        cmds.xform(i, m = tmpmatrix, ws = True)
        cmds.delete([tmpLoc, identity])