#Module Import
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


DRIVER_SELECTION_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "Drivers.json")

TARGET_SELECTION_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "Targets.json")

def storeDriverSelection():
    #remove file if already existing
        try:
            os.remove(DRIVER_SELECTION_PATH)
        except:
            pass
        
        # get user selection
        driver = cmds.ls(selection = True)

        #store user Data as json
        utils.save_data(DRIVER_SELECTION_PATH, driver)

def storeTargetSelection():
    #remove file if already existing
        try:
            os.remove(TARGET_SELECTION_PATH)
        except:
            pass
        
        # get user selection
        targets = cmds.ls(selection = True)

        #store user Data as json
        utils.save_data(TARGET_SELECTION_PATH, targets)

def matrixConstraintToJointsBuild(drivers, targets):
    for index, driver in enumerate(drivers):
        try:
            targetParent = cmds.listRelatives(targets[index], parent=True)[0]
            print(targetParent)
        except:
            targetParent = None


        jointOrientValues = cmds.getAttr(f"{targets[index]}.jointOrient")[0]

        jointOrientMatrix = cmds.createNode("composeMatrix", name = f"{targets[index]}_jointOrient_cm_fNode")
        for j, channel in enumerate("XYZ"):
            cmds.setAttr(f"{jointOrientMatrix}.inputRotate{channel}", jointOrientValues[j])


        if targetParent == None:
            targetParent = cmds.createNode("composeMatrix", name = f"{targets[index]}_identityMtx_cm_fNode")
            targetParentIdentity = True
        else:
            targetParentIdentity = False

        translateScaleMmtxMulti = cmds.createNode("multMatrix", name = f"{targets[index]}_stmmtx_fNode")
        cmds.connectAttr(f"{driver}.worldMatrix[0]", f"{translateScaleMmtxMulti}.matrixIn[0]")

        if targetParentIdentity == True:
            cmds.connectAttr(f"{targetParent}.outputMatrix", f"{translateScaleMmtxMulti}.matrixIn[1]")
        else:
            cmds.connectAttr(f"{targetParent}.worldInverseMatrix[0]", f"{translateScaleMmtxMulti}.matrixIn[1]")
            
        translateScaleDecomposeMtx = cmds.createNode("decomposeMatrix", name = f"{targets[index]}_stdcm_fNode")
        cmds.connectAttr(f"{translateScaleMmtxMulti}.matrixSum", f"{translateScaleDecomposeMtx}.inputMatrix")
        cmds.connectAttr(f"{driver}.rotateOrder", f"{translateScaleDecomposeMtx}.inputRotateOrder")
            
        orientMmtxMulti = cmds.createNode("multMatrix", name = f"{targets[index]}_jointOrientMmtx_fNode")
        cmds.connectAttr(f"{jointOrientMatrix}.outputMatrix", f"{orientMmtxMulti}.matrixIn[0]")

        if targetParentIdentity == True:
            cmds.connectAttr(f"{targetParent}.outputMatrix", f"{orientMmtxMulti}.matrixIn[1]")
        else:
            cmds.connectAttr(f"{targetParent}.worldMatrix[0]", f"{orientMmtxMulti}.matrixIn[1]")
                
        orientMmtxMultiInvers = cmds.createNode("inverseMatrix", name = f"{targets[index]}_jointOrientInversMatrix_fNode")
        cmds.connectAttr(f"{orientMmtxMulti}.matrixSum", f"{orientMmtxMultiInvers}.inputMatrix")
            
        rotationMmtx = cmds.createNode("multMatrix", name = f"{targets[index]}_rotationMmtx_fNode")
        cmds.connectAttr(f"{driver}.worldMatrix[0]", f"{rotationMmtx}.matrixIn[0]")
        cmds.connectAttr(f"{orientMmtxMultiInvers}.outputMatrix", f"{rotationMmtx}.matrixIn[1]")
            
        rotationDecomposemtx = cmds.createNode("decomposeMatrix", name = f"{targets[index]}_rdcm_fNode")
        cmds.connectAttr(f"{driver}.rotateOrder", f"{rotationDecomposemtx}.inputRotateOrder")
        cmds.connectAttr(f"{rotationMmtx}.matrixSum", f"{rotationDecomposemtx}.inputMatrix")
            
        for channel in "XYZ":
            cmds.connectAttr(f"{translateScaleDecomposeMtx}.outputTranslate{channel}", f"{targets[index]}.translate{channel}")
            cmds.connectAttr(f"{translateScaleDecomposeMtx}.outputScale{channel}", f"{targets[index]}.scale{channel}")
            cmds.connectAttr(f"{rotationDecomposemtx}.outputRotate{channel}", f"{targets[index]}.rotate{channel}")

            
def fetchUserSelectionData():
    # read IK Joints Selection to list
    try:
        drivers = utils.load_data(DRIVER_SELECTION_PATH)
    except:
        raise log.error("No Drivers Selected!!")
    
    # read FK Joints Selection to list
    try:
        targets = utils.load_data(TARGET_SELECTION_PATH)
    except:
        raise log.error("No Targets Selected!!")

    os.remove(DRIVER_SELECTION_PATH)
    os.remove(TARGET_SELECTION_PATH)

    matrixConstraintToJointsBuild(drivers, targets)

def matrixConstraintsToJointsUI():
    #window
    configWindow = cmds.window(title="MatrixConstraintToJoint", iconName = "mtxConst", widthHeight=(200, 300), sizeable=True)

    #window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Create Matrix Constraints to Joints", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    #Define drivers Button
    driverObjects = cmds.button(label="Set Driver", command = lambda _: storeDriverSelection())

    #SpaceDivider
    cmds.text(label="", height=10)

    #Define targets Button
    targetObjects= cmds.button(label="Set Targets", command = lambda _: storeTargetSelection())

    #SpaceDivider
    cmds.text(label="", height=10)

    #Create constraints Button
    matrixConstraintToJointsBuild = cmds.button(label = "Create pair blends", command = lambda _: fetchUserSelectionData())

    #display Window 
    cmds.showWindow(configWindow)






