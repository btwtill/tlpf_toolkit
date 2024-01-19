import maya.cmds as cmds

import logging
import os
import re
import subprocess


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

CTRLFILENAME = "BabyGroot_Ctrl_Publish_V001.ma"

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
    cmds.parent(oldHeadCtrlHRC, f"{MID}_head_controls")

    cmds.delete(oldRightArmCtrlHRC, 
                oldLeftArmCtrlHRC, 
                oldSpineCtrlHRC,
                oldLeftLegCtrlHRC,
                oldRightLegCtrlHRC,
                oldMainCtrlHRC,
                oldHeadCtrlHRC)


    return True

def build_BabyGroot_Rig():
    #create Rig Hirarchy
    isRigHirarchyCreated = createRigHirachy()
    log.info(f"Current Workspace Direcotry: {PROJ_PATH}")
    log.info(f"Rig Hirarchy created: {isRigHirarchyCreated}")

    #Import Ctrl Rig
    log.info(f"Ctrl Rig File Location: {PROJ_PATH}scenes/RigBuildDir/Sources/Ctrls/Publish/{CTRLFILENAME}")
    isRigCtrlsImported = cmds.file(f"{PROJ_PATH}scenes/RigBuildDir/Sources/Ctrls/Publish/{CTRLFILENAME}", i = True)
    log.info(f"Imported Rig Ctrls: {isRigCtrlsImported}")

    #Sort Contorls into Rig Hirarchy
    isRigCtrlsSorted = sortCtrlsHirarchy()
    log.info(f"Rig Ctrl Sorting: {isRigCtrlsSorted}")
    