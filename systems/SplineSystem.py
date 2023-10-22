#Module import
import maya.cmds as cmds
from tlpf_toolkit.utils import GeneralFunctions
from tlpf_toolkit.ui import common
from tlpf_toolkit import global_variables
import logging
import os
from tlpf_toolkit.ctrlShapes import utils

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

IK_NECKJOINT_SELETION_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "IK_NeckJoints.json")
SPLINE_START_CTRL_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "SplineStartCtrl.json")
SPLINE_END_CTRL_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "SplineEndCtrl.json")

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

def BuildSpline(_baseJoints, _startCtrl, _endCtrl):
    startCtrl = _startCtrl[0]
    endCtrl = _endCtrl[0]

    

def FetchNeckSplineData():
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

    #remove the tmp files in the tmpData File directory

    os.remove(IK_NECKJOINT_SELETION_PATH)
    os.remove(SPLINE_START_CTRL_PATH)
    os.remove(SPLINE_END_CTRL_PATH)

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
    
    BuildSpline()


def NeckSplineIKConfigUI():

    configWindow = cmds.window(title="NeckSplineIK", iconName = "NeckSpline", widthHeight=(200, 300), sizeable=True)

    #window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Build Neck Spline IK System", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    #Define IK Joints Label
    jointSelectionLabel = cmds.text(label="Define IK Joints", height = 20, backgroundColor = [.8, .8, .8])

    #Define IK Joints Button
    jointSelectionButton = cmds.button(label="Store Neck Joints", command = lambda _: StoreNeckJoints(jointSelectionLabel))

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
    cmds.text(label="", height=20)

    #Create pairBlends Button
    buildNeckSpline = cmds.button(label = "Build Neck Spline", command = lambda _: FetchNeckSplineData())

    #display Window 
    cmds.showWindow(configWindow)