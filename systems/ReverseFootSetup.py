#Module Import
import maya.cmds as cmds


#=======================================
## Reverse Foot Function
#=======================================
def createReverseChain():
    sel = cmds.ls(selection=True)

    cmds.select(clear=True)

    jointList = []
    ctrlList = []

    for i in sel:
        translation = cmds.xform(i, q=True, ws=True, translation=True)
        rotation = cmds.xform(i, q=True, ws=True, rotation=True)
        
        newJoint = cmds.joint(name=i, orientation=rotation, position=translation)
        jointList.append(newJoint)
        
        if i == "Heel":
            exractrl = cmds.circle(name=newJoint + '_swivel_ctrl')
            cmds.setAttr(exractrl[0] + '.translate', *translation)
            cmds.setAttr(exractrl[0] + '.rotate', *rotation)
            ctrlList.append(exractrl)
        if i == "Tip":
            exractrl = cmds.circle(name=newJoint + '_swivel_ctrl')
            cmds.setAttr(exractrl[0] + '.translate', *translation)
            cmds.setAttr(exractrl[0] + '.rotate', *rotation)
            ctrlList.append(exractrl)
            
        ctrl = cmds.circle(name=newJoint + '_ctrl')
        cmds.setAttr(ctrl[0] + '.translate', *translation)
        cmds.setAttr(ctrl[0] + '.rotate', *rotation)
        ctrlList.append(ctrl)
        
        cmds.select(clear=True)
        
        
    jointList = list(reversed(jointList))
    ctrlList = list(reversed(ctrlList))


    def hirarchyReparenting(_targetList):
        for i in range(len(_targetList)):
            if i != (len(_targetList) - 1):
                cmds.parent(_targetList[i], _targetList[i + 1])
            else:
                pass

    hirarchyReparenting(jointList)
    hirarchyReparenting(ctrlList)
#=======================================
## Reverse Foot Function - END
#=======================================
