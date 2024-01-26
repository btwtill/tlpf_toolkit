import maya.cmds as cmds
import logging
import maya.api.OpenMaya as om


from tlpf_toolkit.joint import JointFunctions
from tlpf_toolkit.systems import IkFkSwitch, PoleVectorFunction, RibbonSetup
from tlpf_toolkit.builds.BabyGroot_rig import utilityFunctions
from tlpf_toolkit.utils import GeneralFunctions, ZeroOffsetFunction
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

    #connectIKFK Attribute to the Blend Nodes
    for blendNode in leftArmIKFKBlendNodes:
        cmds.connectAttr(f"iKfK.L_Arm_IKFK", f"{blendNode}.weight")

    #create the input Transform for the Arm Component and connect the Incomping Matrix into the Input Node
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

    #connect Clavicle Ctrl to clavicle IKFK Joint

    leftArmClavicleWorldSRTDecompose = cmds.createNode("decomposeMatrix", name = f"{leftArmClavicleCtrl}_WorldSRTDecompose_fNode")
    cmds.connectAttr(f"{leftArmClavicleCtrl}.worldMatrix[0]", f"{leftArmClavicleWorldSRTDecompose}.inputMatrix")

    for channel in "XYZ":
        cmds.connectAttr(f"{leftArmClavicleWorldSRTDecompose}.outputTranslate{channel}", f"{leftArmClavicelJoint}.translate{channel}")
        cmds.connectAttr(f"{leftArmClavicleCtrl}.rotate{channel}", f"{leftArmClavicelJoint}.rotate{channel}")

    leftArmFKCtrlParentSpaces = [leftArmClavicelJoint] + leftArmFKctrls

    #connect Ctrl Translation though Matrix Multiplication
    for index, ctrl in enumerate(leftArmFKctrls):
        newMultMatrix = cmds.createNode("multMatrix", name = f"{ctrl}_MatrixInParentSpaceMulti_fNode")
        decomposeLocalTranslation = cmds.createNode("decomposeMatrix", name = f"{ctrl}_decomposeLocalTranslationValues_fNode")
        #connect World Position to Mult Matrix 0 input
        cmds.connectAttr(f"{ctrl}.worldMatrix[0]", f"{newMultMatrix}.matrixIn[0]")
        #connect inverse Coord System of parent Space to Mult Matrix 1 input
        cmds.connectAttr(f"{leftArmFKCtrlParentSpaces[index]}.worldInverseMatrix[0]", f"{newMultMatrix}.matrixIn[1]")
        #connect Multiplication Result into decompose Input
        cmds.connectAttr(f"{newMultMatrix}.matrixSum", f"{decomposeLocalTranslation}.inputMatrix")
        #connect Translation and Rotation Values to Joint
        for channel in "XYZ":
            cmds.connectAttr(f"{decomposeLocalTranslation}.outputTranslate{channel}", f"{leftArmFKJoints[index]}.translate{channel}")
            cmds.connectAttr(f"{ctrl}.rotate{channel}", f"{leftArmFKJoints[index]}.rotate{channel}")


    #create Left Arm IK Chain
    leftArmIKHandle = cmds.ikHandle(solver = "ikRPsolver",
                                    startJoint = leftArmIKJoints[0],
                                    endEffector = leftArmIKJoints[-1],
                                    name = f"{LEFT}_arm_IKHandle_srt")
    
    log.info(f"Left Arm IK Return Values: {leftArmIKHandle}")
    cmds.select(clear = True)
    leftArmIKHandle[1] = cmds.rename(f"{leftArmIKHandle[1]}", f"{LEFT}_arm_IKHandleEnd_dnt")
    cmds.select(clear=True)

    log.info(f"Left Arm IK Return Values: {leftArmIKHandle}")

    ZeroOffsetFunction.internalZeroOffset([leftArmIKHandle[0]], ["_mtrxOff", "_srtBuffer"] )

    cmds.select(clear= True)
    cmds.parent(f"{leftArmIKHandle[0]}_mtrxOff", "l_wrist_IKCtrl")
    cmds.select(clear= True)

    log.info(f"Matrix Offset Target: {cmds.listRelatives(leftArmIKHandle[0], parent=True)}")

    MatrixZeroOffset.createMatrixZeroOffsetSpecific(cmds.listRelatives(leftArmIKHandle[0], parent=True))

    cmds.parent(f"{leftArmIKHandle[0]}_srtBuffer", leftArmIKFKSystems)
    cmds.select(clear=True)

    #connect Wrist Ctrl Rotation to IK Joint
    for channel in "XYZ":
        cmds.connectAttr(f"l_wrist_IKCtrl.rotate{channel}", f"{leftArmIKJoints[-1]}.rotate{channel}")
    
    #create Pole Vector Constraint
    cmds.poleVectorConstraint("l_armPV_ctrl", f"{leftArmIKHandle[0]}")

    #create Pole Vector Line
    poleVectorLineColor = (0, 0.33, 1)
    poleVectorLineComponents = PoleVectorFunction.createPoleVectorLineInternal("l_armPV_ctrl", leftArmIKJoints[1])
    cmds.setAttr(f"{poleVectorLineComponents[2]}.overrideEnabled", 1)
    cmds.setAttr(f"{poleVectorLineComponents[2]}.overrideRGBColors", 1)
    cmds.setAttr(f"{poleVectorLineComponents[2]}.overrideColorR", poleVectorLineColor[0])
    cmds.setAttr(f"{poleVectorLineComponents[2]}.overrideColorG", poleVectorLineColor[1])
    cmds.setAttr(f"{poleVectorLineComponents[2]}.overrideColorB", poleVectorLineColor[2])
    
    cmds.setAttr(f"{poleVectorLineComponents[2]}.isHistoricallyInteresting", 0)
    log.info(f"Pole Vector line Components: {poleVectorLineComponents}")

    #create Arm Twist Setup

    #create Arm Vines

    


    return True

    

def buildRightArm():
    return True