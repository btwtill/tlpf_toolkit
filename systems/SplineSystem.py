#Module import
import maya.cmds as cmds
from tlpf_toolkit.utils import GeneralFunctions
from tlpf_toolkit.ui import common
from tlpf_toolkit import global_variables
from tlpf_toolkit.utils import ZeroOffsetFunction
from tlpf_toolkit.mtrx import MatrixZeroOffset
import re
import logging
import os
from tlpf_toolkit.ctrlShapes import utils

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

IK_NECKJOINT_SELETION_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "IK_NeckJoints.json")
SPLINE_START_CTRL_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "SplineStartCtrl.json")
SPLINE_END_CTRL_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "SplineEndCtrl.json")
SPLINE_CURVE_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "SplineCurve.json")

#=======================================
## IK Spline Neck System
#=======================================

def StoreNeckJoints(jointSelectionLabel):

    #remove file if already existing
    try:
        os.remove(IK_NECKJOINT_SELETION_PATH)
    except:
        pass
    
    # get user selection
    joints = cmds.ls(selection = True)

    #store user Data as json
    utils.save_data(IK_NECKJOINT_SELETION_PATH, joints)

    #update label
    cmds.text(jointSelectionLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def StoreStartCtrl(startCtrlLabel):

    #remove file if already existing
    try:
        os.remove(SPLINE_START_CTRL_PATH)
    except:
        pass
    
    # get user selection
    startCtrl = cmds.ls(selection = True)

    #store user Data as json
    utils.save_data(SPLINE_START_CTRL_PATH, startCtrl)

    #update label
    cmds.text(startCtrlLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def StoreEndCtrl(endCtrlLabel):
    #remove file if already existing
    try:
        os.remove(SPLINE_END_CTRL_PATH)
    except:
        pass
    
    # get user selection
    endCtrl = cmds.ls(selection = True)

    #store user Data as json
    utils.save_data(SPLINE_END_CTRL_PATH, endCtrl)

    #update label
    cmds.text(endCtrlLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def StoreSplineCurve(splineCurveLabel):
    #remove file if already existing
    try:
        os.remove(SPLINE_CURVE_PATH)
    except:
        pass
    
    # get user selection
    splineCurve = cmds.ls(selection = True)

    #store user Data as json
    utils.save_data(SPLINE_CURVE_PATH, splineCurve)

    #update label
    cmds.text(splineCurveLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def BuildSpline(_baseJoints, _startCtrl, _endCtrl, _splineCurve, baseName):

    #store List items as strings
    startCtrl = _startCtrl[0]
    endCtrl = _endCtrl[0]
    splineCurve = _splineCurve[0]

    #duplicate Joint selection and parent to world
    splineJoints = GeneralFunctions.duplicateSelection(_baseJoints)

    #rparent the joint into the right hirarchy
    GeneralFunctions.reparenting(splineJoints)
    
    log.info(f"{splineJoints}")

    #rename Joints
    for i in range(len(splineJoints)):

        nameMatch = re.match(r"^.*(_)", splineJoints[i][0])

        splineJoints[i] = cmds.rename(splineJoints[i][0], nameMatch.group() + "sik")

    #debug
    for i in splineJoints:
        log.info(f"{i}")

    #sperate start and end joint 
    startSplineJoint = splineJoints[0]
    endSplineJoint = splineJoints[-1]

    log.info(f"{startSplineJoint}")
    log.info(f"{endSplineJoint}")

    log.info(f"Curve: {splineCurve} Type: {type(splineCurve)}")

    ikhandleNamePattern = re.match(r"^.*(_)", startSplineJoint)

    #create SplineIKHandle
    ikSplineHandle = cmds.ikHandle(sol="ikSplineSolver", 
                                   ccv = False, 
                                   pcv = False, 
                                   startJoint = startSplineJoint, 
                                   endEffector = endSplineJoint, 
                                   curve = splineCurve,
                                   name = ikhandleNamePattern.group() + "sikh")
    
    #duplicate start and endJoint
    ctrlJoints = [startSplineJoint, endSplineJoint]
    ctrlJoints = GeneralFunctions.duplicateSelection(ctrlJoints)

    log.info(f"{ctrlJoints}")

    #rename ctrl Joints 
    ctrlJointNamePattern = re.match(r"^.*(_)", ctrlJoints[0][0])
    startCtrlJoint = cmds.rename(ctrlJoints[0], ctrlJointNamePattern.group() + "ctrlJnt")

    ctrlJointNamePattern = re.match(r"^.*(_)", ctrlJoints[1][0])
    endCtrlJoint = cmds.rename(ctrlJoints[1], ctrlJointNamePattern.group() + "ctrlJnt")

    #skin ctrl joints to spline Curve
    splineCurveSkinCluster = cmds.skinCluster(splineCurve, [startCtrlJoint, endCtrlJoint], bm = 0)

    #parent ctrl Joint to ctrl 
    cmds.parent(startCtrlJoint, startCtrl)
    cmds.parent(endCtrlJoint, endCtrl)

    cmds.select(clear = True)
    cmds.select(startCtrlJoint)
    cmds.select(endCtrlJoint, add=True)

    ZeroOffsetFunction.insertNodeBefore()

    cmds.select(clear = True)
    cmds.select(startCtrlJoint)

    MatrixZeroOffset.createMatrixZeroOffset(startCtrlJoint)

    #clear out Joint Orientation
    for i in "XYZ":
        cmds.setAttr(startCtrlJoint + ".jointOrient" + i, 0)

    cmds.select(clear=True)
    cmds.select(endCtrlJoint)

    MatrixZeroOffset.createMatrixZeroOffset(endCtrlJoint)

    #clear out Joint Orientationq
    for i in "XYZ":
        cmds.setAttr(endCtrlJoint + ".jointOrient" + i, 0)


    #group spline System
    splinegrp = cmds.group(empty = True, name= "cn_" + baseName + "_grp")
    cmds.parent(splineJoints[0], splinegrp)
    cmds.parent(ikSplineHandle, splinegrp)
    cmds.parent(startCtrlJoint, splinegrp)
    cmds.parent(endCtrlJoint, splinegrp)





def FetchNeckSplineData(baseName):
     # read IK Joints Selection to list
    try:
        joints = utils.load_data(IK_NECKJOINT_SELETION_PATH)
    except:
        raise log.error("No joint Selection Found!!")
    
    # read FK Joints Selection to list
    try:
        startCtrl = utils.load_data(SPLINE_START_CTRL_PATH)
    except:
        raise log.error("No start Ctrl Found")

    # read Target Joints Selection to list 
    try:
        endCtrl = utils.load_data(SPLINE_END_CTRL_PATH)
    except:
        raise log.error("No end Ctrl Found")
    
    try:
        splineCurve = utils.load_data(SPLINE_CURVE_PATH)
    except:
        raise log.error("No joint Selection Found!!")

    #remove the tmp files in the tmpData File directory

    os.remove(IK_NECKJOINT_SELETION_PATH)
    os.remove(SPLINE_START_CTRL_PATH)
    os.remove(SPLINE_END_CTRL_PATH)
    os.remove(SPLINE_CURVE_PATH)

    if len(joints) < 2:
        raise Exception(f"There must be at least 3 joints in the Joints selection, current selection length {len(joints)}")
    else:
        jointSelectionString = "".join(joints)
        log.info("Your joint Selection: {}".format(jointSelectionString))

    if len(startCtrl) > 1:
        raise Exception("There cannot be more than one startCtrl")
    else:
        log.info("Start Ctrl: {}".format(startCtrl[0]))

    if len(endCtrl) > 1:
        raise Exception("There cannot be more than one endCtrl")
    
    if len(splineCurve) > 1:
        raise Exception("There cannot be more than one Spline Curve!!")
    
    BuildSpline(joints, startCtrl, endCtrl, splineCurve, baseName)


def NeckSplineIKConfigUI():

    configWindow = cmds.window(title="SimpleSplineIK", iconName = "SimpleSpline", widthHeight=(200, 300), sizeable=True)

    #window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Build Spline IK System", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    #set Base system name
    baseNameLabel = cmds.text(label="Set System BaseName", height = 20, backgroundColor = [.8, .8, .8])

    #basename TextField
    baseName = cmds.textField()

    #Space Divider
    cmds.text(label="", height=10)

    #Define IK Joints Label
    jointSelectionLabel = cmds.text(label="Define IK Joints", height = 20, backgroundColor = [.8, .8, .8])

    #Define IK Joints Button
    jointSelectionButton = cmds.button(label="Store Joints", command = lambda _: StoreNeckJoints(jointSelectionLabel))

    #SpaceDivider
    cmds.text(label="", height=10)

    #Define FK Joitns Label
    startCtrlLabel = cmds.text(label="Define start Ctrl", height = 20, backgroundColor = [.8, .8, .8])

    #Define FK Joints Button
    startCtrlButton = cmds.button(label="Save startCtrl", command = lambda _: StoreStartCtrl(startCtrlLabel))

    #SpaceDivider
    cmds.text(label="", height=10)

    #Define FK Joints Label
    endCtrlLabel = cmds.text(label="Define End Ctrl", height = 20, backgroundColor = [.8, .8, .8])

    #Define FK Joints Button
    endCtrlButton = cmds.button(label="Save endCtrl", command = lambda _: StoreEndCtrl(endCtrlLabel))

    #SpaceDivider
    cmds.text(label="", height=10)

    #Define FK Joints Label
    splineCurveLabel = cmds.text(label="Define Spline Curve", height = 20, backgroundColor = [.8, .8, .8])

    #Define FK Joints Button
    splineCurveButton = cmds.button(label="Save Spline Curve", command = lambda _: StoreSplineCurve(splineCurveLabel))

    #SpaceDivider
    cmds.text(label="", height=20)

    #Create pairBlends Button
    buildNeckSpline = cmds.button(label = "Build Neck Spline", command = lambda _: FetchNeckSplineData(cmds.textField(baseName, query = True, text=True)))

    #display Window 
    cmds.showWindow(configWindow)