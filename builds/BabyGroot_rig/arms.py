import maya.cmds as cmds
import logging
import maya.api.OpenMaya as om


from tlpf_toolkit.joint import JointFunctions
from tlpf_toolkit.systems import IkFkSwitch, PoleVectorFunction, RibbonSetup, TwistJoints, SimpleStretchSetup
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

    #     leftArmClavicleWorldSRTDecompose = cmds.createNode("decomposeMatrix", name = f"{leftArmClavicleCtrl}_WorldSRTDecompose_fNode")
    #     cmds.connectAttr(f"{leftArmClavicleCtrl}.worldMatrix[0]", f"{leftArmClavicleWorldSRTDecompose}.inputMatrix")

    #     for channel in "XYZ":
    #         cmds.connectAttr(f"{leftArmClavicleWorldSRTDecompose}.outputTranslate{channel}", f"{leftArmClavicelJoint}.translate{channel}")
    #         cmds.connectAttr(f"{leftArmClavicleCtrl}.rotate{channel}", f"{leftArmClavicelJoint}.rotate{channel}")

    # leftArmFKCtrlParentSpaces = [leftArmClavicelJoint] + leftArmFKctrls

    #     #connect Ctrl Translation though Matrix Multiplication
    #     for index, ctrl in enumerate(leftArmFKctrls):
    #         newMultMatrix = cmds.createNode("multMatrix", name = f"{ctrl}_MatrixInParentSpaceMulti_fNode")
    #         decomposeLocalTranslation = cmds.createNode("decomposeMatrix", name = f"{ctrl}_decomposeLocalTranslationValues_fNode")
    #         #connect World Position to Mult Matrix 0 input
    #         cmds.connectAttr(f"{ctrl}.worldMatrix[0]", f"{newMultMatrix}.matrixIn[0]")
    #         #connect inverse Coord System of parent Space to Mult Matrix 1 input
    #         cmds.connectAttr(f"{leftArmFKCtrlParentSpaces[index]}.worldInverseMatrix[0]", f"{newMultMatrix}.matrixIn[1]")
    #         #connect Multiplication Result into decompose Input
    #         cmds.connectAttr(f"{newMultMatrix}.matrixSum", f"{decomposeLocalTranslation}.inputMatrix")
    #         #connect Translation and Rotation Values to Joint
    #         for channel in "XYZ":
    #             cmds.connectAttr(f"{decomposeLocalTranslation}.outputTranslate{channel}", f"{leftArmFKJoints[index]}.translate{channel}")
    #             cmds.connectAttr(f"{ctrl}.rotate{channel}", f"{leftArmFKJoints[index]}.rotate{channel}")

    #clavicle Parent Constraint
    cmds.parentConstraint(f"{leftArmClavicleCtrl}", f"{leftArmClavicelJoint}")

    #fk Chain Parent Constraint
    for index, joint in enumerate(leftArmFKJoints):
        cmds.parentConstraint(f"{leftArmFKctrls[index]}", f"{joint}")


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

        # #connect Wrist Ctrl Rotation to IK Joint
        # for channel in "XYZ":
        #     cmds.connectAttr(f"l_wrist_IKCtrl.rotate{channel}", f"{leftArmIKJoints[-1]}.rotate{channel}")
    
    cmds.orientConstraint("l_wrist_IKCtrl", f"{leftArmIKJoints[-1]}")

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
    #Upper Arm Twist
    leftUpperArmNoRollJoint = cmds.duplicate(f"{leftArmDrvIKFKJoints[0]}", rc = True)
    log.info(f"Left Upper Arm No Roll Joints: {leftUpperArmNoRollJoint}")
    cmds.delete(leftUpperArmNoRollJoint[-1])
    leftUpperArmNoRollJoint.pop(-1)

    leftUpperArmNoRollJoint[0] = cmds.rename(leftUpperArmNoRollJoint[0], leftUpperArmNoRollJoint[0].replace("1", "_noRoll"))
    leftUpperArmNoRollJoint[1] = cmds.rename(leftUpperArmNoRollJoint[1], leftUpperArmNoRollJoint[1].replace("1", "_noRoll"))

    #cmds.parent(leftUpperArmNoRollJoint[0], "L_arm_drvIkfk")
    #cmds.select(clear=True)
    log.info(f"Renamed No Roll Joints: {leftUpperArmNoRollJoint}")
    for joint in leftUpperArmNoRollJoint:
        cmds.setAttr(f"{joint}.radius", 1.6)
    
    cmds.parent(leftUpperArmNoRollJoint[0], f"{leftArmDrvIKFKJoints[0]}")
    cmds.select(clear=True)

    leftUpperArmNoRollIK = cmds.ikHandle(solver = "ikSCsolver",
                                         name = "l_upperArmNoRollIKHandle_srt",
                                         startJoint = f"{leftUpperArmNoRollJoint[0]}",
                                         endEffector = f"{leftUpperArmNoRollJoint[1]}")
    
    log.info(f"Upper Arm No Roll IK components: {leftUpperArmNoRollIK}")

    leftUpperArmNoRollIK[1] = cmds.rename(leftUpperArmNoRollIK[1], "l_upperArmNoRollIKHandle_dnt")
    cmds.pointConstraint(leftArmDrvIKFKJoints[1], leftUpperArmNoRollIK[0])
    cmds.select(clear=True)
    cmds.parent(leftUpperArmNoRollIK[0], leftArmClavicelJoint)
    cmds.select(clear=True)

    leftArmNoRollFollowJoint = cmds.duplicate(leftUpperArmNoRollJoint[0], po = True, name = leftUpperArmNoRollJoint[0].replace("noRoll", "RollRef"))[0]
    cmds.setAttr(f"{leftArmNoRollFollowJoint}.radius", 2)
    cmds.parent(leftArmNoRollFollowJoint, leftUpperArmNoRollJoint[0])
    cmds.select(clear=True)

    cmds.aimConstraint(leftUpperArmNoRollJoint[1], leftArmNoRollFollowJoint, 
                       aimVector = [0, 1, 0], 
                       upVector = [-1, 0, 0], 
                       worldUpType = "objectrotation", 
                       worldUpObject = leftArmDrvIKFKJoints[0], 
                       worldUpVector = [-1, 0, 0])

    #Distribute Rotation Weights to twist Ctrl Offset Nodes
    leftUpperArmBendyCtrlConstraintNodes = cmds.listRelatives("l_upperArmBeny_ctrls", c = True)
    pointConstraintWeights = TwistJoints.getWeights(3)
    TwistJoints.createTwistJointPointConstraints(leftUpperArmBendyCtrlConstraintNodes, leftArmDrvIKFKJoints[0], leftArmDrvIKFKJoints[1], pointConstraintWeights[0], pointConstraintWeights[1])

    for node in leftUpperArmBendyCtrlConstraintNodes:
        cmds.connectAttr(f"{leftArmDrvIKFKJoints[0]}.worldMatrix[0]", f"{node}.offsetParentMatrix")
        GeneralFunctions.clearTransformsSpecific([node], False, True, False)

    #connect Bendy Twist Ctrls to Twist Joints
    leftUpperArmTwistWeightMultiplyNode = cmds.createNode("multiplyDivide", name = "l_arm_upperArmTwistWeightMultiply_fNode")
    cmds.connectAttr(f"{leftArmNoRollFollowJoint}.rotateY", f"{leftUpperArmTwistWeightMultiplyNode}.input1X")
    cmds.setAttr(f"{leftUpperArmTwistWeightMultiplyNode}.input2X", -1)
    cmds.connectAttr(f"{leftUpperArmTwistWeightMultiplyNode}.outputX", f"{leftUpperArmBendyCtrlConstraintNodes[0]}.rotateY")

    cmds.connectAttr(f"{leftArmNoRollFollowJoint}.rotateY", f"{leftUpperArmTwistWeightMultiplyNode}.input1Y")
    cmds.setAttr(f"{leftUpperArmTwistWeightMultiplyNode}.input2Y", -0.5)
    cmds.connectAttr(f"{leftUpperArmTwistWeightMultiplyNode}.outputY", f"{leftUpperArmBendyCtrlConstraintNodes[1]}.rotateY")
    
    #Lower Arm Twist
    leftLowerArmTwistCtrlConstrainNodes = cmds.listRelatives("l_lowArmBeny_ctrls", c = True)
    TwistJoints.createTwistJointPointConstraints(leftLowerArmTwistCtrlConstrainNodes, leftArmDrvIKFKJoints[1], leftArmDrvIKFKJoints[2], pointConstraintWeights[0], pointConstraintWeights[1])

    for node in leftLowerArmTwistCtrlConstrainNodes:
        cmds.connectAttr(f"{leftArmDrvIKFKJoints[1]}.worldMatrix[0]", f"{node}.offsetParentMatrix")
        GeneralFunctions.clearTransformsSpecific([node], False, True, False)

    leftLowerArmTwistReferenceLocator = cmds.spaceLocator(name = "L_arm_lowerArmTwistReferenceLocator")[0]
    leftArmWristJointWorldMatrix = cmds.xform(leftArmDrvIKFKJoints[2], query = True, m = True, ws = True)
    cmds.xform(leftLowerArmTwistReferenceLocator, m = leftArmWristJointWorldMatrix, ws = True)
    cmds.select(clear=True)
    cmds.parent(leftLowerArmTwistReferenceLocator, leftArmDrvIKFKJoints[1])

    cmds.select(clear=True)
    leftLowerArmTwistFollowLocator = cmds.spaceLocator(name = "L_arm_lowerArmTwistFollowLocator")[0]
    cmds.xform(leftLowerArmTwistFollowLocator, m = leftArmWristJointWorldMatrix, ws = True)
    cmds.select(clear=True)
    cmds.parent(leftLowerArmTwistFollowLocator, leftArmDrvIKFKJoints[2])
    cmds.select(clear=True)
    
    leftLowerArmTwistFollowDecomposeWorldMatrixNode = cmds.createNode("decomposeMatrix", name = "L_arm_lowerArmTwistFollowDecomposeMatrix_fNode")
    leftLowerArmTwistReferenceDecomposeWorldMatrixNode = cmds.createNode("decomposeMatrix", name = "L_arm_lowerArmTwistReferenceDecomposeMatrix_fNode")
    cmds.connectAttr(f"{leftLowerArmTwistFollowLocator}.worldMatrix[0]", f"{leftLowerArmTwistFollowDecomposeWorldMatrixNode}.inputMatrix")
    cmds.connectAttr(f"{leftLowerArmTwistReferenceLocator}.worldMatrix[0]", f"{leftLowerArmTwistReferenceDecomposeWorldMatrixNode}.inputMatrix")

    leftLowerArmTwistQuatInvertNode = cmds.createNode("quatInvert", name = "L_arm_lowerArmTwistQuatInvers_fNode")
    for channel in "XYZW":
        cmds.connectAttr(f"{leftLowerArmTwistFollowDecomposeWorldMatrixNode}.outputQuat{channel}", f"{leftLowerArmTwistQuatInvertNode}.inputQuat{channel}")

    leftLowerArmTwistQuatMultNode = cmds.createNode("quatProd", name = "L_arm_lowerArmTwistQuatProduct_fNode")

    for channel in "XYZW":
        cmds.connectAttr(f"{leftLowerArmTwistReferenceDecomposeWorldMatrixNode}.outputQuat{channel}", f"{leftLowerArmTwistQuatMultNode}.input1Quat{channel}")
        cmds.connectAttr(f"{leftLowerArmTwistQuatInvertNode}.outputQuat{channel}", f"{leftLowerArmTwistQuatMultNode}.input2Quat{channel}")

    leftLowerArmTwistConverQuatToEulerNode = cmds.createNode("quatToEuler", name = "L_arm_lowerarmTwistQTEConvert_fNode")
    for channel in "XYZW":
        cmds.connectAttr(f"{leftLowerArmTwistQuatMultNode}.outputQuat{channel}", f"{leftLowerArmTwistConverQuatToEulerNode}.inputQuat{channel}")

    leftLowerArmTwistWeightMultiplyNode = cmds.createNode("multiplyDivide", name = "L_arm_lowerArmTwistWeightMulti_fNode")

    cmds.connectAttr(f"{leftLowerArmTwistConverQuatToEulerNode}.outputRotateY", f"{leftLowerArmTwistWeightMultiplyNode}.input1X")
    cmds.connectAttr(f"{leftLowerArmTwistConverQuatToEulerNode}.outputRotateY", f"{leftLowerArmTwistWeightMultiplyNode}.input1Y")
    cmds.setAttr(f"{leftLowerArmTwistWeightMultiplyNode}.input2X", -1)
    cmds.setAttr(f"{leftLowerArmTwistWeightMultiplyNode}.input2Y", -0.5)

    cmds.connectAttr(f"{leftLowerArmTwistWeightMultiplyNode}.outputX", f"{leftLowerArmTwistCtrlConstrainNodes[2]}.rotateY")
    cmds.connectAttr(f"{leftLowerArmTwistWeightMultiplyNode}.outputY", f"{leftLowerArmTwistCtrlConstrainNodes[1]}.rotateY")

    #connect Bendy Twist Ctrsl to twist Joints
    leftArmTwistctrlConstraintNodes = leftUpperArmBendyCtrlConstraintNodes + leftLowerArmTwistCtrlConstrainNodes
    leftArmTwistJoints = cmds.listRelatives("L_arm_deform", c = True)
    leftArmTwistJoints.pop(0)
    leftArmTwistCtrls = []

    for node in leftArmTwistctrlConstraintNodes:
        ctrl = cmds.listRelatives(node, c =True)[0]
        leftArmTwistCtrls.append(ctrl)

    log.info(f"left arm Twist ctrls: {leftArmTwistCtrls}")
    log.info(f"left arm Twist Joint: {leftArmTwistJoints}")

    for index, ctrl in enumerate(leftArmTwistCtrls):
        cmds.connectAttr(f"{ctrl}.worldMatrix[0]", f"{leftArmTwistJoints[index]}.offsetParentMatrix")
        GeneralFunctions.clearTransformsSpecific([leftArmTwistJoints[index]], True, True, True)
        for channel in "XYZ":
            cmds.setAttr(f"{leftArmTwistJoints[index]}.jointOrient{channel}", 0)

    #implement Arm Stretch
    log.info(f"ik joints: {leftArmIKJoints}")
    cmds.select(clear=True)
    leftArmStretchPinNodes, defaultLengthJoints = SimpleStretchSetup.BuildStretchSetupInternal(leftArmIKJoints, leftArmANCHOR, "l_armPV_ctrl", "l_wrist_IKCtrl")
    log.info(f"Left Arm StretchPin Nodes: {leftArmStretchPinNodes}")
    log.info(f"Left Arm default Length Joints: {defaultLengthJoints}")

    try:
        cmds.connectAttr(f"{leftArmStretchPinNodes[0]}.output", f"{leftArmIKJoints[1]}.translateY")
        cmds.connectAttr(f"{leftArmStretchPinNodes[1]}.output", f"{leftArmIKJoints[2]}.translateY")
    except:
        log.info("Couldnt Conncet stretch values to Joints!")

    cmds.select(clear=True)
    cmds.parent(defaultLengthJoints[0], leftArmIKFKSystems)
    cmds.select(clear=True)

    #create Arm Vines
    leftArmVineSystem = cmds.createNode("transform", name = f"{LEFT}_arm_VineSystem", parent = f"{LEFT}_arm_systems")
    leftArmVineDeformGroup = cmds.createNode("transform", name = f"{LEFT}_arm_VineDeformation", parent = f"{LEFT}_arm_deform")

    leftArmVineGuides = cmds.listRelatives("l_armVine_Guides_grp", c = True)
    log.info(f"All Vine Guides: {leftArmVineGuides}")

    #STORE THE VERTICAL VINES AS LIST
    leftArmVerticalVines = ["ArmVineB00, ArmVineE00, ArmVineP01"]

    #Create Vines
    for vineGuide in leftArmVineGuides:

        log.info(f"Current Vine Guide: {vineGuide}")
        baseNamePattern = r'_(.*?)_'
        baseName = utilityFunctions.getBaseName(baseNamePattern, vineGuide)
        
        if baseName:
            log.info(f"Current Vine Base Name: {baseName}")
        else:
            log.info(f"Base Name could not be found Check your Guides Naming Convention.")
        log.info(f"Current Vine Side: {LEFT}")

        isVertical = utilityFunctions.check_multiple_strings(vineGuide, leftArmVerticalVines)
        direction = 'Vertical' if isVertical else 'Horizontal'

        log.info(f"Current Vine Direction: {direction}")

        RibbonSetup.buildGuidedRibbon(LEFT, baseName, True, False, False, "", True, "sphere_blue", True, "diamond_blue", direction)

        cmds.select(clear=True)
        vineRigGroupName = f"{LEFT}_{baseName}_Rig_grp"
        cmds.parent(vineRigGroupName, leftArmVineSystem)

        vineLetter = baseName.replace("armVine", "")
        vineLetter = vineLetter[0]
        activationButton = f"l_armVine{vineLetter}_innerButton"

        ctrlRemapName = f"{activationButton}_ctrlVisRemap_fNode"
        tweakCtrlRemapName = f"{activationButton}_tweakCtrlVisRemap_fNode"


        vineRigTweakCtrlGroup = cmds.listRelatives(vineRigGroupName, c = True)[-1]

        vineRigDeformJoints = cmds.listRelatives(vineRigTweakCtrlGroup, c = True, ad =True, typ = "joint")
        vineRigDeformCtrls = cmds.listRelatives(vineRigTweakCtrlGroup, c = True, ad =True, typ = "transform")
        
        vineRigDeformCtrls = vineRigDeformCtrls[1::2]

        log.info(f"Vine Rig tweakCtrls: {vineRigDeformCtrls}")
        log.info(f"Vine Rig deformJointsList: {vineRigDeformJoints}")

        for ctrl in vineRigDeformJoints:
            log.info(f"Current Vine Deform Joints{ctrl}")


        for index, joint in enumerate(vineRigDeformJoints):
            cmds.connectAttr(f"{vineRigDeformCtrls[index]}.worldMatrix[0]", f"{joint}.offsetParentMatrix")
            

        cmds.select(clear=True)
        cmds.parent(vineRigDeformJoints, leftArmVineDeformGroup)
        cmds.select(clear=True)

        for joint in vineRigDeformJoints:
            GeneralFunctions.clearTransformsSpecific([joint])
            JointFunctions.ClearJointOrientValuesInternal([joint])
            log.info(f"currently Cleared Joint {joint}")




        if cmds.objExists(ctrlRemapName):
            cmds.connectAttr(f"{ctrlRemapName}.outValue",  f"{vineRigGroupName}.CtrlVisibility")
            cmds.connectAttr(f"{tweakCtrlRemapName}.outValue", f"{vineRigGroupName}.TweakCtrlVisibility")
        else:
            ctrlRemapNode = cmds.createNode("remapValue", name = ctrlRemapName)
            cmds.setAttr(f"{ctrlRemapNode}.inputMax", 3)
            cmds.setAttr(f"{ctrlRemapNode}.outputMax", 0.5)
            cmds.connectAttr(f"{activationButton}.translateX", f"{ctrlRemapNode}.inputValue")
            cmds.connectAttr(f"{ctrlRemapNode}.outValue",  f"{vineRigGroupName}.CtrlVisibility")
            
            tweakctrlRemapNode = cmds.createNode("remapValue", name = tweakCtrlRemapName)
            cmds.setAttr(f"{tweakctrlRemapNode}.inputMin", 3)
            cmds.setAttr(f"{tweakctrlRemapNode}.inputMax", 6)
            cmds.setAttr(f"{tweakctrlRemapNode}.outputMax", 0.5)
            cmds.connectAttr(f"{activationButton}.translateX", f"{tweakctrlRemapNode}.inputValue")
            cmds.connectAttr(f"{tweakctrlRemapNode}.outValue", f"{vineRigGroupName}.TweakCtrlVisibility")

        log.info(f"Vine ActivationButton: {activationButton}")


    

    return True

    

def buildRightArm():
    return True



