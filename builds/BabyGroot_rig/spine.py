import maya.cmds as cmds
import logging

from tlpf_toolkit.joint import JointFunctions
from tlpf_toolkit.utils import GeneralFunctions
from tlpf_toolkit.node import MultiConnectFunction
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


GUIDE = "guide"
CTRL = "ctrl"
HRC = "hrc"
COMPONENT = "cmpnt"
MID = "M"
LEFT = "L"
RIGHT = "R"


def buildSpine():

    #build Curv driver joints
    spineIKFKSystem = cmds.createNode("transform", name = f"{MID}_spine_IKFK_system", parent = f"{MID}_spine_systems")

    chestSpineCurveDriverGuide = "M_chest_guide"
    midSpineCurveDriverGuide = "M_spine02_guide"
    hipSpineCurveDriverGuide = "M_hip_guide"

    spineCurveDriverGuides = [chestSpineCurveDriverGuide, midSpineCurveDriverGuide, hipSpineCurveDriverGuide]

    spineCurveDriverJoints = JointFunctions.convertGuidesToIndividualJoints(spineCurveDriverGuides, spineIKFKSystem, "_guide", "_ctrlDriver", 1.4)

    cmds.select(clear= True)
    log.info(f"Spine Curve Driver Joints: {spineCurveDriverJoints}")
    cmds.parent("M_spine_splineIKCurve_srt", spineIKFKSystem)

    #build IK Spline
    spineDriverJoints = cmds.listRelatives(f"{MID}_spine_driver", ad = True, c = True)
    spineDriverJoints = list(reversed(spineDriverJoints))
    log.info(f"Spine Driver Joints: {spineDriverJoints}")

    cmds.select(clear = True)

    spineIKHandle = cmds.ikHandle(ccv = False, c = f"{MID}_spine_splineIKCurve_srt", 
                  endEffector = spineDriverJoints[-1], 
                  freezeJoints = True, rootOnCurve = True, 
                  solver = "ikSplineSolver", 
                  startJoint = spineDriverJoints[0],
                  parentCurve = False,
                  name = f"{MID}_spine_splineIKHandle_srt")
    cmds.select(clear=True)
    spineIKHandle[1] = cmds.rename(spineIKHandle[1], f"{MID}_spine_splineIKEffector_dnt")
    cmds.parent(spineIKHandle[0], spineIKFKSystem)

    spineSplineIKSkinCluster = cmds.skinCluster(spineCurveDriverJoints, f"{MID}_spine_splineIKCurve_srt", name = f"{MID}_spine_splineIKSkinCluster_fNode")
    log.info(f"Spine IK Handle: {spineIKHandle[0]}")
    log.info(f"Spine IK SkinCluster Node: {spineSplineIKSkinCluster}")

    #noodle the Ctrls into the mix
    cmds.connectAttr(f"{MID}_chest_ctrl.worldMatrix[0]", f"{spineCurveDriverJoints[0]}.offsetParentMatrix")
    cmds.connectAttr(f"{MID}_spine02_ikCtrl.worldMatrix[0]", f"{spineCurveDriverJoints[1]}.offsetParentMatrix")

    hipsCtrlToJointOffsetValue = -4.5

    composeOffsetMatrixNode = cmds.createNode("composeMatrix", name = f"{MID}_spine_hipsCtrlOffsetToJoint_cm_fNode")
    multiplyOffsetMatrixNode = cmds.createNode("multMatrix", name = f"{MID}_spine_hipsCtrlOffsetToJoint_mmult_fNode")

    cmds.setAttr(f"{composeOffsetMatrixNode}.inputTranslateY", hipsCtrlToJointOffsetValue)
    cmds.connectAttr(f"{composeOffsetMatrixNode}.outputMatrix", f"{multiplyOffsetMatrixNode}.matrixIn[0]")
    cmds.connectAttr(f"{MID}_hips_ctrl.worldMatrix[0]", f"{multiplyOffsetMatrixNode}.matrixIn[1]")
    cmds.connectAttr(f"{multiplyOffsetMatrixNode}.matrixSum", f"{spineCurveDriverJoints[2]}.offsetParentMatrix")

    GeneralFunctions.clearTransforms(spineCurveDriverJoints)

    steadyChestpointConstraint  = cmds.pointConstraint(f"{MID}_chest_drvIkfk", f"{MID}_chest_ctrlDriver", f"{MID}_chest_skn")[0]

    steadyChestAttributeReverseNode = cmds.createNode("reverse", name = f"{MID}_Spine_steadyChestAttributeRevesre_fNode")

    cmds.connectAttr(f"{MID}_chest_ctrl.SteadySpine", f"{steadyChestAttributeReverseNode}.inputX")
    cmds.connectAttr(f"{MID}_chest_ctrl.SteadySpine", f"{steadyChestpointConstraint}.{MID}_chest_ctrlDriverW1")
    cmds.connectAttr(f"{steadyChestAttributeReverseNode}.outputX", f"{steadyChestpointConstraint}.{MID}_chest_drvIkfkW0")

    chestCtrlWorldSpaceRotationDecomposeNode = cmds.createNode("decomposeMatrix", name = f"{MID}_spine_chestCtrlWorldSpaceRotation_dcm_fNode")
    cmds.connectAttr(f"{MID}_chest_ctrl.worldMatrix[0]", f"{chestCtrlWorldSpaceRotationDecomposeNode}.inputMatrix")
    for channel in "XYZ":
        cmds.connectAttr(f"{chestCtrlWorldSpaceRotationDecomposeNode}.outputRotate{channel}", f"{MID}_chest_skn.rotate{channel}")

    #configure Spine Twist Ctrl
    cmds.setAttr(f"{spineIKHandle[0]}.dTwistControlEnable", 1)
    cmds.setAttr(f"{spineIKHandle[0]}.dForwardAxis", 2)
    cmds.setAttr(f"{spineIKHandle[0]}.dWorldUpType", 4)
    cmds.setAttr(f"{spineIKHandle[0]}.dWorldUpAxis", 4)
    cmds.setAttr(f"{spineIKHandle[0]}.dWorldUpVectorZ",-1)
    cmds.setAttr(f"{spineIKHandle[0]}.dWorldUpVectorEndZ", -1)
    cmds.connectAttr(f"{MID}_hips_ctrl.worldMatrix[0]", f"{spineIKHandle[0]}.dWorldUpMatrix")
    cmds.connectAttr(f"{MID}_chest_ctrl.worldMatrix[0]", f"{spineIKHandle[0]}.dWorldUpMatrixEnd")

    #Implement Stretch
    spineIKCurveLengthInfoNode = cmds.createNode("curveInfo", name = f"{MID}_spine_splineIKCurveLengthInfo_fNode")
    cmds.connectAttr(f"{MID}_spine_splineIKCurve_srtShape.local", f"{spineIKCurveLengthInfoNode}.inputCurve")

    #Multiply divide node to calculate the stetch value of the curve
    spineIKCurveLengthStretchFactorMultiplyNode = cmds.createNode("multiplyDivide", name = f"{MID}_spine_splineIKStretchFactorMultiply_fNode")
    cmds.connectAttr(f"{spineIKCurveLengthInfoNode}.arcLength", f"{spineIKCurveLengthStretchFactorMultiplyNode}.input1X")
    spineIKCurveRestLengthValue = cmds.getAttr(f"{spineIKCurveLengthInfoNode}.arcLength")
    cmds.setAttr(f"{spineIKCurveLengthStretchFactorMultiplyNode}.input2X", spineIKCurveRestLengthValue)
    cmds.setAttr(f"{spineIKCurveLengthStretchFactorMultiplyNode}.operation", 2)

    #Spine Sretch Condition Node
    spineStretchTypeMainConditionNode = cmds.createNode("condition", name = f"{MID}_spine_splineIKStretchtypeMainCondition_fNode")
    cmds.setAttr(f"{spineStretchTypeMainConditionNode}.secondTerm", 1)
    cmds.setAttr(f"{spineStretchTypeMainConditionNode}.colorIfFalseG", 1)
    cmds.connectAttr(f"{spineIKCurveLengthStretchFactorMultiplyNode}.outputX", f"{spineStretchTypeMainConditionNode}.colorIfTrueR")
    cmds.connectAttr(f"{spineIKCurveLengthStretchFactorMultiplyNode}.outputX", f"{spineStretchTypeMainConditionNode}.firstTerm")

    #Create and Connect a Plus minus Average node to get set the right operation for the condition node for selection the spine stretch type
    spineStretchTypeOffsetAdditionNode = cmds.createNode("plusMinusAverage", name = f"{MID}_spine_splineIKFKStretchTypeOffsetAddition_fNode")
    cmds.setAttr(f"{spineStretchTypeOffsetAdditionNode}.input1D[0]", 1)
    cmds.connectAttr(f"{MID}_chest_ctrl.StretchType", f"{spineStretchTypeOffsetAdditionNode}.input1D[1]")
    cmds.connectAttr(f"{MID}_chest_ctrl.StretchType", f"{spineStretchTypeOffsetAdditionNode}.input1D[2]")
    cmds.connectAttr(f"{spineStretchTypeOffsetAdditionNode}.output1D", f"{spineStretchTypeMainConditionNode}.operation")

    #blend between using the volume preservation or not using the attribute on the Chest Ctrl
    spineStretchVolumePreservationBlendNode = cmds.createNode("blendTwoAttr", name = f"{MID}_spine_splineVolumePreservationBlend_fNode")
    cmds.connectAttr(f"{MID}_chest_ctrl.VolumePreservation", f"{spineStretchVolumePreservationBlendNode}.attributesBlender")
    cmds.setAttr(f"{spineStretchVolumePreservationBlendNode}.input[0]", 1)
    cmds.connectAttr(f"{spineStretchTypeMainConditionNode}.outColorR", f"{spineStretchVolumePreservationBlendNode}.input[1]")
    
    #connect the calculated value to the joints scaleY inputs
    MultiConnectFunction.ConnectNodesMulti("outColorR", "scaleY", spineStretchTypeMainConditionNode, spineDriverJoints)
    
    #Multiply Divide not to calculate the volume Preservation Value for the other scale channels for the joints
    spineIKSquashFactorMultiplyNode = cmds.createNode("multiplyDivide", name = f"{MID}_spine_splineIKSquashFactorMultiply_fNode")
    cmds.connectAttr(f"{spineStretchVolumePreservationBlendNode}.output", f"{spineIKSquashFactorMultiplyNode}.input1X")
    cmds.setAttr(f"{spineIKSquashFactorMultiplyNode}.input2X", -1)
    cmds.setAttr(f"{spineIKSquashFactorMultiplyNode}.operation", 3)
    
    #animatable attributes to change the Volume Preservation Factors for each joint
    spineSquashFactorAttributes = ["HipSquashFactor", "Spine01SquashFactor", "Spine02SquashFactor", "Spine03SquashFactor", "ChestSquashFactor"]

    for index, node in enumerate(spineDriverJoints):
        newMultDoubleNode = cmds.createNode("multDoubleLinear", name = f"{MID}_spine_{node}SquashMulti_fNode")
        cmds.connectAttr(f"{spineIKSquashFactorMultiplyNode}.outputX", f"{newMultDoubleNode}.input1")
        newSquashFactorBlendNode = cmds.createNode(f"blendTwoAttr", name = f"{MID}_spine_{node}blendStretchType_fNode")
        cmds.connectAttr(f"{MID}_chest_ctrl.VolumePreservation", f"{newSquashFactorBlendNode}.attributesBlender")
        cmds.setAttr(f"{newSquashFactorBlendNode}.input[0]", 1)
        cmds.connectAttr(f"{MID}_chest_ctrl.{spineSquashFactorAttributes[index]}", f"{newSquashFactorBlendNode}.input[1]")
        cmds.connectAttr(f"{newSquashFactorBlendNode}.output", f"{newMultDoubleNode}.input2")
        cmds.connectAttr(f"{newMultDoubleNode}.output", f"{node}.scaleX")
        cmds.connectAttr(f"{newMultDoubleNode}.output", f"{node}.scaleZ")
    
    return True




