
#Module Import
import maya.cmds as cmds



#=======================================
##Match ALL Transform Function
#=======================================
def matchAll():
    selection = cmds.ls(selection=True)
    print(selection)
    if len(selection) >= 2:
        targetMatrix = cmds.xform(selection[-1], query=True, worldSpace=True, matrix=True)
        print(targetMatrix)
        for i in range(len(selection)):
            if i != (len(selection) - 1):
                cmds.xform(selection[i], worldSpace=True, matrix=targetMatrix)
                print(i)
#=======================================
##Match ALL Transform Function - END
#=======================================


#=======================================
##Match Translation Function
#=======================================
def matchTranslation():
    selection = cmds.ls(selection=True)
    if len(selection) >= 2:
        targetTranslation = cmds.xform(selection[-1], query=True, worldSpace=True, translation=True)
        for i in range(len(selection)):
            if i != (len(selection) - 1):
                cmds.xform(selection[i], worldSpace=True, translation=targetTranslation)

#=======================================
##Match Translation Function End
#=======================================


#=======================================
##Match Rotation Function
#=======================================
def matchRotation():
    selection = cmds.ls(selection=True)
    if len(selection) >= 2:
        rotationTarget = cmds.xform(selection[-1], query=True, worldSpace=True, rotation=True)
        for i in range(len(selection)):
            if i != (len(selection) - 1):
                cmds.xform(selection[i], worldSpace=True, rotation=rotationTarget)
#=======================================
##Match Rotation Function - END
#=======================================


#=======================================
##Match Scale Function
#=======================================
def matchScale():
    selection = cmds.ls(selection=True)
    if len(selection) >= 2:
        scaleTarget = cmds.xform(selection[-1], query=True, worldSpace=True, scale=True)
        for i in range(len(selection)):
            if i != (len(selection) - 1):
                cmds.xform(selection[i], worldSpace=True, scale=scaleTarget)
#=======================================
##Match Scale Function - END
#=======================================