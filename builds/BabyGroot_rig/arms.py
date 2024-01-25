import maya.cmds as cmds
import logging
import maya.api.OpenMaya as om


from tlpf_toolkit.joint import JointFunctions
from tlpf_toolkit.systems import IkFkSwitch
from tlpf_toolkit.builds.BabyGroot_rig import utilityFunctions
from tlpf_toolkit.utils import GeneralFunctions
from tlpf_toolkit.mtrx import MatrixZeroOffset

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

#CONSTANTS
GUIDE = "guide"
CTRL = "ctrl"
HRC = "hrc"
COMPONENT = "cmpnt"
MID = "M"
LEFT = "L"
RIGHT = "R"

def buildLeftArm():
    cmds.select(clear = True)
    leftArmGuides = cmds.listRelatives("L_arm_Guides", c = True, typ = "transform")[0]
    leftArmGuides = cmds.listRelatives(leftArmGuides, c = True, ad = True, typ = "transform")
    leftArmGuides = list(reversed(leftArmGuides))
    log.info(f"Left Arm Guides: {leftArmGuides}")

    leftArmDrvIKFKJoints = list(reversed(cmds.listRelatives("L_arm_driver", c = True, ad = True)))
    log.info(f"Left Arm IKFK Driver Joints: {leftArmDrvIKFKJoints}")

    leftArmIKFKSystems = cmds.createNode("transform", name = f"{LEFT}_arm_IKFKSystem", parent =f"{LEFT}_arm_systems")

    leftArmClavicleCtrl = "l_clavicle_ctrl"


    #create Anchor Locator for FK Ctrl Chain
    leftArmWordMatrixPosition = cmds.xform(leftArmDrvIKFKJoints[1], query = True, m = True, ws = True)
    leftArmANCHOR = cmds.spaceLocator(name = f"{LEFT}_arm_ANCHOR_srt")[0]
    cmds.select(clear = True)
    cmds.parent(leftArmANCHOR, leftArmIKFKSystems)
    cmds.xform(leftArmANCHOR, m = leftArmWordMatrixPosition, ws = True)

    leftArmIKFKGuides = leftArmGuides

    log.info(f"{leftArmIKFKGuides}")

    cmds.select(clear=True)
    #Create IK JointChain
    leftArmIKJoints = JointFunctions.convertGuidesToJointChain(leftArmIKFKGuides, "_ik")

    cmds.select(clear=True)
    #Create FKJointChain
    leftArmFKJoints = JointFunctions.convertGuidesToJointChain(leftArmIKFKGuides, "_fk")

    cmds.select(clear = True)
    cmds.parent(leftArmIKJoints[0], leftArmIKFKSystems)
    cmds.parent(leftArmFKJoints[0], leftArmIKFKSystems)

    cmds.connectAttr(f"{leftArmDrvIKFKJoints[0]}.worldMatrix[0]", f"{leftArmFKJoints[0]}.offsetParentMatrix")
    cmds.connectAttr(f"{leftArmDrvIKFKJoints[0]}.worldMatrix[0]", f"{leftArmIKJoints[0]}.offsetParentMatrix")

    leftArmDrvIKFKRelativeTranslateParentOffset = cmds.xform(leftArmDrvIKFKJoints[1], query = True, t = True)

    log.info(f"Arm Translate Values: {leftArmDrvIKFKRelativeTranslateParentOffset}")

    cmds.xform(leftArmIKJoints[0], t = leftArmDrvIKFKRelativeTranslateParentOffset)
    cmds.xform(leftArmFKJoints[0], t = leftArmDrvIKFKRelativeTranslateParentOffset)

    cmds.select(clear=True)

    #create IKFK Switch nodes
    leftArmClavicelJoint = leftArmDrvIKFKJoints.pop(0)

    log.info(f"Joints to be Blend: {leftArmDrvIKFKJoints}")
    leftArmIKFKBlendNodes = []

    for index, joint in enumerate(leftArmDrvIKFKJoints):
        leftArmIKFKPairBlendNode = IkFkSwitch.CreateSinglePairBlend(leftArmIKJoints[index], leftArmFKJoints[index], leftArmDrvIKFKJoints[index])
        leftArmIKFKBlendNodes.append(leftArmIKFKPairBlendNode)

    log.info(f"Left Arm IKFK blend Nodes {leftArmIKFKBlendNodes}")

    cmds.select(clear=True)

    leftArmLocalWorldInput = cmds.createNode("transform", name = f"{LEFT}_arm_localWorld_srt")
    cmds.parent(leftArmLocalWorldInput, f"{LEFT}_arm_input")
    cmds.connectAttr(f"cn_chest_ctrl.worldMatrix[0]", f"{leftArmLocalWorldInput}.offsetParentMatrix")

    clavicleOffsetMatrix = GeneralFunctions.getOffsetSrt("cn_chest_ctrl", leftArmClavicleCtrl)

    log.info(f"{clavicleOffsetMatrix}")

    clavicleOffsetMatrixTranslation = GeneralFunctions.getMatrixTranslation(clavicleOffsetMatrix)
    
    leftArmClavicleOffsetCMNode = cmds.createNode("composeMatrix", name = f"{LEFT}_clavicle_OffsetComposeMatrix_fNode")

    cmds.setAttr(f"{leftArmClavicleOffsetCMNode}.inputTranslate", *clavicleOffsetMatrixTranslation)
    
    #zeroing the clavicle Ctrl
    leftArmCalvicleOffsetMultMatrixNode = cmds.createNode("multMatrix", name = f"{LEFT}_clavicle_OffsetMultMatrix_fNode")

    cmds.connectAttr(f"{leftArmClavicleOffsetCMNode}.outputMatrix", f"{leftArmCalvicleOffsetMultMatrixNode}.matrixIn[0]")
    cmds.connectAttr(f"{leftArmLocalWorldInput}.worldMatrix[0]", f"{leftArmCalvicleOffsetMultMatrixNode}.matrixIn[1]")
    cmds.connectAttr(f"{leftArmCalvicleOffsetMultMatrixNode}.matrixSum", f"{leftArmClavicleCtrl}.offsetParentMatrix")

    #reordering the hirarchy
    cmds.parent(leftArmClavicleCtrl, "L_arm_controls")
    cmds.select(clear=True)
    GeneralFunctions.clearTransformsSpecific([leftArmClavicleCtrl], True, True, False)
    
    #Zero 
    leftArmFKctrls = ["l_arm_FKCtrl", "l_elbow_FKCtrl", "l_wrist_FKCtrl"]

    leftArmFKCtrlsOffsetMatrixComposeNodes = MatrixZeroOffset.createMatrixZeroOffsetSpecific(leftArmFKctrls, True, True, True, True, True, False, True)

    cmds.parent(leftArmFKctrls, "L_arm_controls")

    #connect FK controls to FK Joints
    for index, ctrl in enumerate(leftArmFKctrls):
        offsetAdditionNode = cmds.createNode("plusMinusAverage", name = f"{ctrl}_offsetAdditionPMA_fNode")
        for channel in "xyz":
            cmds.connectAttr(f"{leftArmFKCtrlsOffsetMatrixComposeNodes[index]}.inputTranslate{channel.upper()}", f"{offsetAdditionNode}.input3D[0].input3D{channel}")
            cmds.connectAttr(f"{ctrl}.translate{channel.upper()}", f"{offsetAdditionNode}.input3D[1].input3D{channel}")
            cmds.connectAttr(f"{offsetAdditionNode}.output3D{channel}", f"{leftArmFKJoints[index]}.translate{channel.upper()}")

    return True

    

def buildRightArm():
    return True