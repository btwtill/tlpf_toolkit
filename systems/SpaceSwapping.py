#Module Import
import maya.cmds as cmds

from tlpf_toolkit.ctrlShapes import utils
from tlpf_toolkit.utils import GeneralFunctions
from tlpf_toolkit import global_variables
import os

TARGETSPACES_SELECTION = os.path.join(global_variables.DATA_LIBRARY_PATH, "TargetSpaces.json")


def StoreSelectedTarget():
    print("Stored")


def TargetSpaceInputGroup(index):
    targetSpaces = utils.load_data(TARGETSPACES_SELECTION)

    targetSpaceLabel = cmds.text(label=f"Target Space {targetSpaces}")

def StoreTargetSpace():
    #remove file if already existing
    try:
        os.remove(TARGETSPACES_SELECTION)
    except:
        pass

    targetSpaces = cmds.ls(selection = True)

    utils.save_data(TARGETSPACES_SELECTION, targetSpaces)

    for i in range(len(targetSpaces)):
        TargetSpaceInputGroup(i)

    

def MatrixSpaceSwappingConfigUI():
    #config Window
    configWindow = cmds.window(title = "MatrixSpaceSwap", sizeable = True, resizeToFitChildren = True)

    #Window Layout
    windowLayout = cmds.rowColumnLayout(adjustableColumn = True)

    #window Title Label
    titleLabel = cmds.text(label="Create Matrix Space Switch", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    #Slider Label
    sliderLabel = cmds.text(label="Amount of Spaces:")

    #Slider Group Label
    spaceTargetSliderLabel = cmds.text(label="0")

    #Add Target Spaces Button
    addTargetSpacesButton = cmds.button(label="Add Target Space", command = lambda _: StoreTargetSpace())


    #show window 
    cmds.showWindow(configWindow)


