import maya.cmds as cmds
import maya.api.OpenMaya as om
from tlpf_toolkit.mtrx import MatrixZeroOffset
from tlpf_toolkit.systems import TwistJoints



def parentVineCtrlToBendy():

    sel  = cmds.ls(selection=True)

    parentGrp = cmds.listRelatives(parent = True)[0]
    print(parentGrp)

    cmds.parent(sel[0], sel[1])

    cmds.select(clear=True)
    cmds.select(sel[0]) 

    constraintNode = cmds.pickWalk(direction="down")[0]
    print(constraintNode)

    MatrixZeroOffset.createMatrixZeroOffset(constraintNode)

    cmds.parent(constraintNode, parentGrp)
    cmds.select(clear=True)


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

def connectVisibilityRemap():
    sel = cmds.ls(selection=True)

    stage01Remap = cmds.createNode("remapValue", name = f"{sel[0]}_Stage01VisibilityRemap")
    stage02Remap = cmds.createNode("remapValue", name = f"{sel[0]}_Stage02VisibilityRemap")

    cmds.connectAttr(f"{sel[0]}.translateX", f"{stage01Remap}.inputValue")
    cmds.connectAttr(f"{sel[0]}.translateX", f"{stage02Remap}.inputValue")

    cmds.setAttr(f"{stage01Remap}.inputMax", 3)
    cmds.setAttr(f"{stage01Remap}.outputMax", 0.5)

    cmds.setAttr(f"{stage02Remap}.inputMin", 3)
    cmds.setAttr(f"{stage02Remap}.inputMax", 6)
    cmds.setAttr(f"{stage02Remap}.outputMax", 0.5)

    cmds.connectAttr(f"{stage01Remap}.outValue", f"{sel[1]}.CtrlVisibility")
    cmds.connectAttr(f"{stage02Remap}.outValue", f"{sel[1]}.TweakCtrlVisibility")

def ConnectMainModuleGeoVisibilityToMeshGroup():
    inputAttributes = [["L_Arm_Roots", "l_arm_roots"], ["R_Arm_Roots", "r_arm_roots"], ["L_Leg_Roots", "l_leg_roots"]]


def BuildTwistJoints(parentJoint, childJoint, side, suffix, limb):
    cmds.select(clear=True)
    cmds.select(parentJoint)
    cmds.select(childJoint, add=True)
    twistJoints = TwistJoints.createTwistSetup(3, False, "NONE")
    #rename and Parent Joints
    for index, twistJnt in enumerate(twistJoints):
        twistJoints[index] = cmds.rename(twistJnt, twistJnt.replace(suffix, "_skn"))
        cmds.parent(twistJoints[index], f"{side}_{limb}_deform")
    cmds.select(clear=True)
    return twistJoints


