import maya.cmds as cmds

import logging
import os
import re
import subprocess

from tlpf_toolkit.joint import JointFunctions


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

CTRLFILENAME = "BabyGroot_Ctrl_Publish_V001.ma"
GUIDEFILENAME = "BabyGroot_Guides_Publish_V002.ma"

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
    # Arm Subcomponents Group
    leftArmSubcomponents = cmds.createNode("transform", name = f"{LEFT}_arm_sub{COMPONENT}", parent = leftArmComponent)
    # Arm Hand Subcomponent 
    leftHandSubcomponent = cmds.createNode("transform", name = f"{LEFT}_hand_{COMPONENT}", parent = leftArmSubcomponents)

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
    #Build Left Arm Skeleton

    #Left Arm Guides
    leftClavicleGuide = "L_clavicle_guide"
    leftArmGuide = "L_arm_guide"
    leftElbowGuide = "L_elbow_guide"
    leftWristGuide = "L_wrist_guide"
    
    leftArmGuideNameList = [leftClavicleGuide, leftArmGuide, leftElbowGuide, leftWristGuide]

    leftClavicleWorldMatrix = cmds.xform(leftClavicleGuide, query = True, m = True, ws = True)
    leftArmWorldMatrix = cmds.xform(leftArmGuide, query = True, m = True, ws = True)
    leftElbowWorldMatrix = cmds.xform(leftElbowGuide, query = True, m = True, ws = True)
    leftWristWorldMatrix = cmds.xform(leftWristGuide, query = True, m = True, ws = True)

    leftArmWorldMatrixList = [leftClavicleWorldMatrix, leftArmWorldMatrix, leftElbowWorldMatrix, leftWristWorldMatrix]
    leftArmJointsList = []

    for index, matrix in enumerate(leftArmWorldMatrixList):
        if index == 0:
            newJoint = cmds.joint(name = leftArmGuideNameList[index].replace("_guide", "_skn"))
        else:
            newJoint = cmds.joint(name = leftArmGuideNameList[index].replace("_guide", "_jnt"))

        cmds.select(clear = True)
        cmds.xform(newJoint, m = matrix, ws = True)
        leftArmJointsList.append(newJoint)

    JointFunctions.buildForwardJointChain(leftArmJointsList, True)

    cmds.parent(leftArmJointsList[0], f"{LEFT}_arm_deform")

    if len(leftArmJointsList) != 0:
        return True
    else:
        return False

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