#Module Import
import maya.cmds as cmds

import logging
from tlpf_toolkit.utils import ZeroOffsetFunction
from tlpf_toolkit.ctrlShapes import utils
from tlpf_toolkit.utils import GeneralFunctions
from tlpf_toolkit import global_variables
from tlpf_toolkit.mtrx import MatrixZeroOffset
import os

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def MatrixSpaceSwitch():
    sel = cmds.ls(selection = True)

    #validate selection lenght 2 < len < 10
    if len(sel) < 2:
        raise Exception("There must be at lease One Target Selected")
    else:
        log.info(f"Current Selection Length: {len(sel)}")

    #filter main Ctrl
    mainCtrl = sel.pop(0)

    #get follow attribute from main ctrl
    mainFollowAttrString = mainCtrl + ".Follow"

    #Test if the follow attribute is on the mainCtrl
    try:
        mainFollowAttrValue = cmds.getAttr(mainFollowAttrString)
        log.info(f"The current Follow Attribute setting is: {mainFollowAttrValue}")
    except:
        raise Exception("There ther is no Follow Attribute!!")
    
    #get mult matrix output from Offset parent matirx input
    mainParentMatrixOffset = cmds.listConnections(mainCtrl, destination=False, source = True, type = "multMatrix")[0]

    #create blend matrix node
    blendMatrixNode = cmds.createNode("blendMatrix", name=mainCtrl + "_SpaceSwapBlendmtrx")

    #set input matrix on blend matrix node
    cmds.connectAttr(mainCtrl + ".offsetParentMatrix", blendMatrixNode + ".inputMatrix")
    cmds.disconnectAttr(mainCtrl + ".offsetParentMatrix", blendMatrixNode + ".inputMatrix")

    #disconnect offsetParent matrix on main ctrl
    cmds.disconnectAttr(mainParentMatrixOffset + ".matrixSum", mainCtrl + ".offsetParentMatrix")

    #connect blend matirx output to offsetParentMatrix on main ctrl
    cmds.connectAttr(blendMatrixNode + ".outputMatrix", mainCtrl + ".offsetParentMatrix")

    #list for all offset Positions
    offsetLocators = []

    #create locators for every target in sel
    for i in sel:
        newOffsetLocator = cmds.spaceLocator(name = mainCtrl + "_SpaceSwap_" + i)
        offsetLocators.append(newOffsetLocator)

    #match the locator to the main ctrl
    for i in offsetLocators:
        cmds.matchTransform(i, mainCtrl)

    #parent the locators there corresponding target ctrls
    for i in range(len(sel)):
        cmds.parent(offsetLocators[i], sel[i])

    #variable to store the mult matrix nodes later to be used s Target Spaces
    targetCtrlSpaces = [mainParentMatrixOffset]
    
    for i in offsetLocators:
        cmds.select(clear=True)
        cmds.select(i)

        #give all locators offset nodes 
        ZeroOffsetFunction.insertNodeBefore()

        log.info(f"Current OffsetLocator{i}, datatype of the locator {type(i)}")

        #convert offset nodes in matrix offsets 
        MatrixZeroOffset.createMatrixZeroOffset(i[0])

        targetCtrlSpaces.append(cmds.listConnections(i[0], destination=False, source = True, type = "multMatrix")[0])

    log.info(f"Target Spaces Nodes: {targetCtrlSpaces}")

    for i in range(len(targetCtrlSpaces)):

        #connect the mult matrix nodes to the blend matrix node
        cmds.connectAttr(targetCtrlSpaces[i] + ".matrixSum", blendMatrixNode + ".target[" + str(i) + "].targetMatrix")

        #create condition nodes for every target ctrl
        if i == 0:
            weightConditionNode = cmds.createNode("condition", name= mainCtrl + "_SpaceSwapCondition")
        else:
            weightConditionNode = cmds.createNode("condition", name= offsetLocators[i - 1][0] + "_SpaceSwapCondition")
        
        #connect the follow attribute to the condition nodes 
        cmds.connectAttr(mainFollowAttrString, weightConditionNode + ".firstTerm")

        #set the second term of the condition the index of the target ctrl
        cmds.setAttr(weightConditionNode + ".secondTerm", i)

        #set the true output R to 1 and all the false outputs to 0
        cmds.setAttr(weightConditionNode + ".colorIfTrueR", 1)
        for j in "RGB":
            cmds.setAttr(weightConditionNode + ".colorIfFalse" + j, 0)

        #connect true output r to the corresponding weight inputs on the blend Matrix node
        cmds.connectAttr(weightConditionNode + ".outColorR", blendMatrixNode + ".target[" + str(i) + "].weight")

    
    #delete the offset Locator
    for i in offsetLocators:
        cmds.delete(i)