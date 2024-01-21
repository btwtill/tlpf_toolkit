import maya.cmds as cmds

import logging
import os
import re
import subprocess
from tlpf_toolkit.builds.BabyGroot_rig import utilityFunctions
from tlpf_toolkit.joint import JointFunctions
from tlpf_toolkit.builds.BabyGroot_rig import spine

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

PROJ_PATH = cmds.workspace(query = True, rd = True)
BUILDFILE = "BabyGroot_Build_V001"
PUBLISHFILE = "BabyGroot_Publish_V001"
PUBLISHDIR = "scenes/RigBuildDir/Publish"
SOURCEDIR = f"{PROJ_PATH}scenes/RigBuildDir/Sources/"

CTRLFILENAME = "BabyGroot_Ctrl_Publish_V002.ma"
GUIDEFILENAME = "BabyGroot_Guides_Publish_V004.ma"
MODELFILENAME = "BabyGroot_Model_Publish_V001.ma"

def createRigHirachy():
    #Top Level Node
    topLevelNode = cmds.createNode("transform", name = f"BabyGroot_{HRC}")

    #right Arm Component
    leftArmComponent = cmds.createNode("transform", name = f"{LEFT}_arm_{COMPONENT}", parent = topLevelNode)
    # Arm Input Group
    leftArmComponentInput = cmds.createNode("transform", name = f"{LEFT}_arm_input", parent = leftArmComponent)
    # Arm Output Group
    leftArmComponentOutput = cmds.createNode("transform", name = f"{LEFT}_arm_output", parent = leftArmComponent)
    # Arm Ctrls Group
    leftArmComponentCtrls = cmds.createNode("transform", name = f"{LEFT}_arm_controls", parent = leftArmComponent)
    # Arm System Group
    leftArmSystems = cmds.createNode("transform", name = f"{LEFT}_arm_systems", parent = leftArmComponent)
    # Arm Deform Group
    leftArmDeform = cmds.createNode("transform", name = f"{LEFT}_arm_deform", parent = leftArmComponent)
    # Arm Driver Group
    leftArmDriver = cmds.createNode("transform", name = f"{LEFT}_arm_driver", parent = leftArmComponent)
    # Arm Subcomponents Group
    leftArmSubcomponents = cmds.createNode("transform", name = f"{LEFT}_arm_sub{COMPONENT}", parent = leftArmComponent)
    # Arm Hand Subcomponent 
    leftHandSubcomponent = cmds.createNode("transform", name = f"{LEFT}_hand_{COMPONENT}", parent = leftArmSubcomponents)
    # Arm Hand deform 
    leftHandSubcomponentDeform = cmds.createNode("transform", name = f"{LEFT}_hand_deform", parent = leftHandSubcomponent)

    #Right Arm Component
    rightArmComponent = cmds.createNode("transform", name = f"{RIGHT}_arm_{COMPONENT}", parent = topLevelNode)
    # Arm Input Group
    rightArmComponentInput = cmds.createNode("transform", name = f"{RIGHT}_arm_input", parent = rightArmComponent)
    # Arm Output Group
    rightArmComponentOutput = cmds.createNode("transform", name = f"{RIGHT}_arm_output", parent = rightArmComponent)
    # Arm Ctrls Group
    rightArmComponentCtrls = cmds.createNode("transform", name = f"{RIGHT}_arm_controls", parent = rightArmComponent)
    # Arm System Group
    rightArmSystems = cmds.createNode("transform", name = f"{RIGHT}_arm_systems", parent = rightArmComponent)
    # Arm Deform Group
    rightArmDeform = cmds.createNode("transform", name = f"{RIGHT}_arm_deform", parent = rightArmComponent)
    # Arm Driver Group
    rightArmDriver = cmds.createNode("transform", name = f"{RIGHT}_arm_driver", parent = rightArmComponent)
    # Arm Subcomponents Group
    rightArmSubcomponents = cmds.createNode("transform", name = f"{RIGHT}_arm_sub{COMPONENT}", parent = rightArmComponent)
    # Arm Hand Subcomponent 
    rightHandSubcomponent = cmds.createNode("transform", name = f"{RIGHT}_hand_{COMPONENT}", parent = rightArmSubcomponents)
    # Arm Hand deform 
    rightHandSubcomponentDeform = cmds.createNode("transform", name = f"{RIGHT}_hand_deform", parent = rightHandSubcomponent)

    #Left leg Component
    leftlegComponent = cmds.createNode("transform", name = f"{LEFT}_leg_{COMPONENT}", parent = topLevelNode)
    # leg Input Group
    leftlegComponentInput = cmds.createNode("transform", name = f"{LEFT}_leg_input", parent = leftlegComponent)
    # leg Output Group
    leftlegComponentOutput = cmds.createNode("transform", name = f"{LEFT}_leg_output", parent = leftlegComponent)
    # leg Ctrls Group
    leftlegComponentCtrls = cmds.createNode("transform", name = f"{LEFT}_leg_controls", parent = leftlegComponent)
    # leg System Group
    leftlegSystems = cmds.createNode("transform", name = f"{LEFT}_leg_systems", parent = leftlegComponent)
    # leg Deform Group
    leftlegDeform = cmds.createNode("transform", name = f"{LEFT}_leg_deform", parent = leftlegComponent)
    # leg Driver Group
    leftlegDriver = cmds.createNode("transform", name = f"{LEFT}_leg_driver", parent = leftlegComponent)

    #Right leg Component
    rightlegComponent = cmds.createNode("transform", name = f"{RIGHT}_leg_{COMPONENT}", parent = topLevelNode)
    # leg Input Group
    rightlegComponentInput = cmds.createNode("transform", name = f"{RIGHT}_leg_input", parent = rightlegComponent)
    # leg Output Group
    rightlegComponentOutput = cmds.createNode("transform", name = f"{RIGHT}_leg_output", parent = rightlegComponent)
    # leg Ctrls Group
    rightlegComponentCtrls = cmds.createNode("transform", name = f"{RIGHT}_leg_controls", parent = rightlegComponent)
    # leg System Group
    rightlegSystems = cmds.createNode("transform", name = f"{RIGHT}_leg_systems", parent = rightlegComponent)
    # leg Deform Group
    rightlegDeform = cmds.createNode("transform", name = f"{RIGHT}_leg_deform", parent = rightlegComponent)
    # leg Driver Group
    rightlegDriver = cmds.createNode("transform", name = f"{RIGHT}_leg_driver", parent = rightlegComponent)

    #Spine Component
    spineComponent = cmds.createNode("transform", name = f"{MID}_spine_{COMPONENT}", parent = topLevelNode)
    # spine Input Group
    spineComponentInput = cmds.createNode("transform", name = f"{MID}_spine_input", parent = spineComponent)
    # spine Output Group
    spineComponentOutput = cmds.createNode("transform", name = f"{MID}_spine_output", parent = spineComponent)
    # spine Ctrls Group
    spineComponentCtrls = cmds.createNode("transform", name = f"{MID}_spine_controls", parent = spineComponent)
    # spine System Group
    spineComponentSystems = cmds.createNode("transform", name = f"{MID}_spine_systems", parent = spineComponent)
    # spine Deform Group
    spineComponentDeform = cmds.createNode("transform", name = f"{MID}_spine_deform", parent = spineComponent)
    # spine Driver Group
    spineComponentDriver = cmds.createNode("transform", name = f"{MID}_spine_driver", parent = spineComponent)

    #head Component
    headComponent = cmds.createNode("transform", name = f"{MID}_head_{COMPONENT}", parent = topLevelNode)
    # Spine Input Group
    headComponentinput = cmds.createNode("transform", name = f"{MID}_head_input", parent = headComponent)
    # Spine Output Group
    headComponentoutput = cmds.createNode("transform", name = f"{MID}_head_output", parent = headComponent)
    # Spine Ctrls Group
    headComponentCtrls = cmds.createNode("transform", name = f"{MID}_head_controls", parent = headComponent)
    # Spine System Group
    headComponentSystems = cmds.createNode("transform", name = f"{MID}_head_systems", parent = headComponent)
    # Spine Deform Group
    headComponentDeform = cmds.createNode("transform", name = f"{MID}_head_deform", parent = headComponent)
    #  Subcomponents Group
    headSubcomponents = cmds.createNode("transform", name = f"{MID}_head_sub{COMPONENT}", parent = headComponent)
    #  Face Subcomponent
    faceSubcomponent = cmds.createNode("transform", name = f"{MID}_face_{COMPONENT}", parent = headSubcomponents)

    #main Component
    rootComponent = cmds.createNode("transform", name = f"{MID}_root_{COMPONENT}", parent = topLevelNode)
    # output Grouü
    rootComponentoutput = cmds.createNode("transform", name = f"{MID}_root_output", parent = rootComponent)
    # root Ctrls Group
    rootComponentCtrls = cmds.createNode("transform", name = f"{MID}_root_controls", parent = rootComponent)

    return True

def sortCtrlsHirarchy():
    #Sort Ctrls into Rig Hirarchy and Components

    oldRightArmCtrlHRC = "r_Arm_Controls_grp"
    oldLeftArmCtrlHRC = "l_Arm_Controls_grp"
    oldSpineCtrlHRC = "cn_spine_constrols"
    oldLeftLegCtrlHRC = "l_leg_controls"
    oldRightLegCtrlHRC = "r_leg_controls"
    oldMainCtrlHRC = "cn_main_ctrl"
    oldHeadCtrlHRC = "cn_head_controls"

    rightArmControlsContent = cmds.listRelatives(oldRightArmCtrlHRC, c = True)
    cmds.parent(rightArmControlsContent, f"{RIGHT}_arm_controls")

    leftArmControlsContent = cmds.listRelatives(oldLeftArmCtrlHRC, c = True)
    cmds.parent(leftArmControlsContent, f"{LEFT}_arm_controls")

    spineControlsContent = cmds.listRelatives(oldSpineCtrlHRC, c = True)
    cmds.parent(spineControlsContent, f"{MID}_spine_controls")

    leftLegControlsContent = cmds.listRelatives(oldLeftLegCtrlHRC, c = True)
    cmds.parent(leftLegControlsContent, f"{LEFT}_leg_controls")

    rightLegControlsContent = cmds.listRelatives(oldRightLegCtrlHRC, c = True)
    cmds.parent(rightLegControlsContent, f"{RIGHT}_leg_controls")

    cmds.parent(oldMainCtrlHRC, f"{MID}_root_controls")

    headControlsContent = cmds.listRelatives(oldHeadCtrlHRC, c = True)
    cmds.parent(headControlsContent, f"{MID}_head_controls")


    cmds.delete(oldRightArmCtrlHRC, 
                oldLeftArmCtrlHRC, 
                oldSpineCtrlHRC,
                oldLeftLegCtrlHRC,
                oldRightLegCtrlHRC,
                oldHeadCtrlHRC)


    return True

def buildBabyGrootSkeleton():
    #Build Driver Skeleton

    drivenSuffix = "_drvIkfk"

    #arm
    leftClavicleGuide = "L_clavicle_guide"
    leftArmGuide = "L_arm_guide"
    leftElbowGuide = "L_elbow_guide"
    leftWristGuide = "L_wrist_guide"
    
    leftArmGuideNameList = [leftClavicleGuide, leftArmGuide, leftElbowGuide, leftWristGuide]
    leftArmJoints = JointFunctions.convertGuidesToJointChain(leftArmGuideNameList, drivenSuffix)

    cmds.parent(leftArmJoints[0], f"{LEFT}_arm_driver")

    cmds.select(clear=True)
    #leg
    leftLegGuide = "L_Leg_guide"
    leftKneeGuide = "L_Knee_guide"
    leftFootGuide = "L_Foot_guide"

    leftLegGuideNameList = [leftLegGuide, leftKneeGuide, leftFootGuide]
    leftLegJoints = JointFunctions.convertGuidesToJointChain(leftLegGuideNameList, drivenSuffix)

    cmds.parent(leftLegJoints[0], f"{LEFT}_leg_driver")

    #spine
    spineGuides = cmds.listRelatives("M_Spine_guides")
    spineJoints = JointFunctions.convertGuidesToJointChain(spineGuides, drivenSuffix)

    cmds.parent(spineJoints[0], f"{MID}_spine_driver")

    #neck
    cmds.select(clear=True)
    neckGuide = "M_Neck_guide"
    headGuide = "M_Head_guide"

    headGuidesList = [neckGuide, headGuide]

    headJoints = JointFunctions.convertGuidesToJointChain(headGuidesList, drivenSuffix)

    cmds.parent(headJoints[0], f"{MID}_head_deform")

    cmds.select(clear=True)


    #Build Deformation Skeleton

    #fingers
    topLevelFinger = cmds.listRelatives("L_Finger_Guides", c = True)

    middleFingerGuides = cmds.listRelatives(topLevelFinger[0], c = True, ad =True, typ = 'transform')
    middleFingerGuides = list(reversed(middleFingerGuides))
    middleFingerGuides.insert(0, topLevelFinger[0])

    leftMiddleFingerJoints = JointFunctions.convertGuidesToJointChain(middleFingerGuides, "_skn")
    cmds.select(clear=True)
    
    pinkyFingerGuides = cmds.listRelatives(topLevelFinger[1], c = True, ad =True, typ = 'transform')
    pinkyFingerGuides = list(reversed(pinkyFingerGuides))
    pinkyFingerGuides.insert(0, topLevelFinger[1]) 

    leftPinkyFingerJoints = JointFunctions.convertGuidesToJointChain(pinkyFingerGuides, "_skn")
    cmds.select(clear=True)

    indexFingerGuides = cmds.listRelatives(topLevelFinger[2], c = True, ad =True, typ = 'transform')
    indexFingerGuides = list(reversed(indexFingerGuides))
    indexFingerGuides.insert(0, topLevelFinger[2])

    leftIndexFingerJoints = JointFunctions.convertGuidesToJointChain(indexFingerGuides, "_skn")
    cmds.select(clear=True)

    ringFingerGuides = cmds.listRelatives(topLevelFinger[3], c = True, ad =True, typ = 'transform')
    ringFingerGuides = list(reversed(ringFingerGuides))
    ringFingerGuides.insert(0, topLevelFinger[3])

    leftRingFingerJoints = JointFunctions.convertGuidesToJointChain(ringFingerGuides, "_skn")
    cmds.select(clear=True)

    thumbGuides = cmds.listRelatives(topLevelFinger[4], c = True, ad =True, typ = 'transform')
    thumbGuides = list(reversed(thumbGuides))
    thumbGuides.insert(0, topLevelFinger[4])

    leftThumbJoints = JointFunctions.convertGuidesToJointChain(thumbGuides, "_skn")
    cmds.select(clear=True)

    cmds.parent([leftMiddleFingerJoints[0], leftPinkyFingerJoints[0], leftIndexFingerJoints[0], leftRingFingerJoints[0], leftThumbJoints[0], f"{LEFT}_hand_deform"])

    cmds.select(clear=True)
    #Deformation Wrist Joint
    leftDeformWristJoint = cmds.duplicate(leftArmJoints[-1], name = leftArmJoints[-1].replace(drivenSuffix, "_jnt"))[0]
    cmds.parent(leftDeformWristJoint, f"{LEFT}_arm_deform")

    cmds.select(clear=True)
    #Deformation Foot Joint
    leftDeformFootJoint = cmds.duplicate(leftLegJoints[-1], name = leftLegJoints[-1].replace(drivenSuffix, "_jnt"))[0]
    cmds.parent(leftDeformFootJoint, f"{LEFT}_leg_deform")

    cmds.select(clear=True)
    #Mirror Joints
    #arms
    rightArmJoints = cmds.mirrorJoint(leftArmJoints[0],  mb = True, myz = True, sr = ('L_', 'R_'))
    cmds.parent(rightArmJoints[0], f"{RIGHT}_arm_driver")

    cmds.select(clear=True)
    rightDeformWristJoint = cmds.mirrorJoint(leftDeformWristJoint, mb = True, myz = True, sr = ('L_', 'R_'))
    cmds.parent(rightDeformWristJoint, f"{RIGHT}_arm_deform")

    cmds.select(clear=True)
    #legs
    rightLegJoints = cmds.mirrorJoint(leftLegJoints[0], mb = True, myz = True, sr = ('L_', 'R_'))
    cmds.parent(rightLegJoints[0], f"{RIGHT}_leg_driver")

    cmds.select(clear=True)
    rightDeformFootJoint = cmds.mirrorJoint(leftDeformFootJoint, mb = True, myz = True, sr = ('L_', 'R_'))
    cmds.parent(rightDeformFootJoint, f"{RIGHT}_leg_deform")

    cmds.select(clear=True)

    #finger
    rightMiddleFingerJoints = cmds.mirrorJoint(leftMiddleFingerJoints[0], mb = True, myz = True, sr = ('L_', 'R_'))
    rightPinkyFingerJoints = cmds.mirrorJoint(leftPinkyFingerJoints[0], mb = True, myz = True, sr = ('L_', 'R_'))
    rightIndexFingerJoints = cmds.mirrorJoint(leftIndexFingerJoints[0], mb = True, myz = True, sr = ('L_', 'R_'))
    rightRingFingerJoints = cmds.mirrorJoint(leftRingFingerJoints[0], mb = True, myz = True, sr = ('L_', 'R_'))
    rightThumbJoints = cmds.mirrorJoint(leftThumbJoints[0], mb = True, myz = True, sr = ('L_', 'R_'))

    cmds.parent([rightMiddleFingerJoints[0], rightPinkyFingerJoints[0], rightIndexFingerJoints[0], rightRingFingerJoints[0], rightThumbJoints[0]], f"{RIGHT}_hand_deform")

    cmds.select(clear=True)
    #connectDeform Joints
    deformJointPairs = [[leftArmJoints[-1], leftDeformWristJoint], 
                        [leftLegJoints[-1], leftDeformFootJoint], 
                        [rightArmJoints[-1], rightDeformWristJoint[0]], 
                        [rightLegJoints[-1], rightDeformFootJoint[0]]]
    
    log.info(f"Deform Joints paired: {deformJointPairs}")

    for pair in deformJointPairs:
        cmds.connectAttr(f"{pair[0]}.worldMatrix[0]", f"{pair[1]}.offsetParentMatrix")
        for channel in "XYZ":
            cmds.setAttr(f"{pair[1]}.translate{channel}", 0)
            cmds.setAttr(f"{pair[1]}.rotate{channel}", 0)
            cmds.setAttr(f"{pair[1]}.jointOrient{channel}", 0)


    #Twist Joints
    leftUpperArmTwistJoints = utilityFunctions.BuildTwistJoints(leftArmJoints[1], leftArmJoints[2], LEFT, drivenSuffix, "arm")
    leftLowerArmTwistJoints = utilityFunctions.BuildTwistJoints(leftArmJoints[2], leftArmJoints[3], LEFT, drivenSuffix, "arm")
    leftUpperLegTwistJoints = utilityFunctions.BuildTwistJoints(leftLegJoints[0], leftLegJoints[1], LEFT, drivenSuffix, "leg")
    leftLowerLegTwistJoints = utilityFunctions.BuildTwistJoints(leftLegJoints[1], leftLegJoints[2], LEFT, drivenSuffix, "leg")

    rightUpperArmTwistJoints = utilityFunctions.BuildTwistJoints(rightArmJoints[1], rightArmJoints[2], RIGHT, drivenSuffix, "arm")
    rightLowerArmTwistJoints = utilityFunctions.BuildTwistJoints(rightArmJoints[2], rightArmJoints[3], RIGHT, drivenSuffix, "arm")
    rightUpperLegTwistJoints = utilityFunctions.BuildTwistJoints(rightLegJoints[0], rightLegJoints[1], RIGHT, drivenSuffix, "leg")
    rightLowerLegTwistJoints = utilityFunctions.BuildTwistJoints(rightLegJoints[1], rightLegJoints[2], RIGHT, drivenSuffix, "leg")

    #cmds.connectAttr(f"{parentJoint}.worldMatrix[0]", f"{twistJoints[index]}.offsetParentMatrix")
        # for channel in "XYZ":
        #     cmds.setAttr(f"{twistJoints[index]}.jointOrient{channel}", 0)


    #torso Plate Joints
    torsoPlateGuides = cmds.listRelatives("M_torsoPlates_Guides", c = True)

    for guide in torsoPlateGuides:
        guideWorldMatrix = cmds.xform(guide, query = True, m = True, ws = True)
        cmds.select(clear=True)
        newJoint = cmds.joint(name = guide.replace("_guide", "_skn"))
        cmds.xform(newJoint, m = guideWorldMatrix, ws = True)
        cmds.parent(newJoint, f"{MID}_spine_deform")

    log.info(f"Left Arm Driver Joints: {leftArmJoints}")
    log.info(f"Right Arm Driver Joints: {rightArmJoints}")
    log.info(f"Left Leg Driver Joints: {leftLegJoints}")
    log.info(f"Right Leg Driver Joints: {rightLegJoints}")
    log.info(f"Finger Joints:")
    log.info(f"Thumb Joints: {leftThumbJoints, rightThumbJoints}")
    log.info(f"Index Finger Joints: {leftIndexFingerJoints, rightIndexFingerJoints}")
    log.info(f"Middle Finger Joints: {leftMiddleFingerJoints, rightMiddleFingerJoints}")
    log.info(f"Ring Finger Joints: {leftRingFingerJoints, rightRingFingerJoints}")
    log.info(f"Pinky Finger Joints: {leftPinkyFingerJoints, rightPinkyFingerJoints}")
    
    log.info(f"Upper Arm Twist Joints: {leftUpperArmTwistJoints, rightUpperArmTwistJoints}")
    log.info(f"Lower Arm Twist Joints: {leftLowerArmTwistJoints, rightLowerArmTwistJoints}")
    log.info(f"Upper Leg Twist Joints: {leftUpperLegTwistJoints, rightUpperLegTwistJoints}")
    log.info(f"Lower Leg Twist Joints: {leftLowerLegTwistJoints, rightLowerLegTwistJoints}")

    return True

def build_BabyGroot_Rig():

    #Start Building the Rig
    log.info("############")
    log.info("BabyGroot Rig Build Start!!!")
    log.info("############")

    #create Rig Hirarchy
    isRigHirarchyCreated = createRigHirachy()
    log.info(f"Current Workspace Direcotry: {PROJ_PATH}")
    log.info(f"Rig Hirarchy created: {isRigHirarchyCreated}")

    #Import Ctrl Rig
    CtrlRigFilePath = f"{SOURCEDIR}Ctrls/Publish/{CTRLFILENAME}"
    log.info(f"Ctrl Rig File Location: {CtrlRigFilePath}")
    cmds.file(f"{CtrlRigFilePath}", i = True)
    log.info(f"Successfully imported Rig Ctrls")

    #Import Mesh into scene
    ModelFilePath = f"{SOURCEDIR}Model/Publish/{MODELFILENAME}"
    cmds.file(f"{ModelFilePath}", i = True)
    log.info(f"Mesh File Location {ModelFilePath}")

    cmds.parent("BabyGroot_Mesh_hrc", "BabyGroot_hrc")

    #Sort Contorls into Rig Hirarchy
    isRigCtrlsSorted = sortCtrlsHirarchy()
    log.info(f"Rig Ctrl Sorting: {isRigCtrlsSorted}")
    
    #Import Guids into the scene
    rigGuidesFilePath = f"{SOURCEDIR}Guides/Publish/{GUIDEFILENAME}"
    log.info(f"Rig Guides file Location: {rigGuidesFilePath}")
    cmds.file(f"{rigGuidesFilePath}", i = True)
    log.info(f"Successfully imported Guides File")

    #build Skeleton From Guides
    isSkeletonBuild = buildBabyGrootSkeleton()
    log.info(f"Skeleton Build: {isSkeletonBuild}")

    #Build Spine
    spine.buildSpine()

    #Build Left Arm

    #Build Right Arm

    #Build Left Leg

    #Build Right Leg

    #Build Plate System

    #Build Face System

    #Skin Meshes

    