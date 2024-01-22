import maya.cmds as cmds
import logging

from tlpf_toolkit.joint import JointFunctions
from tlpf_toolkit.utils import GeneralFunctions

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


    #Implement Squash plus Switch for Squash and Multiplyiers

    return True