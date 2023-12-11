import maya.cmds as cmds
import maya.internal.common.cmd.base
from tlpf_toolkit.mtrx import MatrixZeroOffset
from tlpf_toolkit.utils import ZeroOffsetFunction

def createPlatesHirarchy():
    mainGrp = cmds.createNode("transform", name = "cn_TorsoPlates_Rig_grp")

    ctrlGrp = cmds.createNode("transform", name = "torsoPlates_Controls_grp", parent = mainGrp)
    pinGrp = cmds.createNode("transform",  name = "torsoPlates_Pins_grp", parent = mainGrp)
    jointsGrp = cmds.createNode("transform",  name = "torsoPlates_joints_grp", parent = mainGrp)

def createPinLocators(guides):
    pins = []
    for index, guide in enumerate(guides):
        pin = cmds.spaceLocator(name = f"{guide.replace('_guide', '_outPin')}")[0]
        print(pin)
        guidePos = cmds.xform(guide, query = True, m = True, ws = True)
        cmds.xform(pin, m = guidePos, ws = True)
        cmds.parent(pin, "torsoPlates_Pins_grp")
        pins.append(pin)

    print(pins)
    return pins

def createPlateCtrls(pins):
    ctrls = []
    offsets = []

    for pin in pins:
        newCtrl = cmds.duplicate("diamond", name = f"{pin.replace('_outPin', '_ctrl')}")[0]

        for channel in "XYZ":
            cmds.setAttr(f"{newCtrl}.translate{channel}", 0)
            cmds.setAttr(f"{newCtrl}.rotate{channel}", 0)
            cmds.setAttr(f"{newCtrl}.scale{channel}", 1)

        pinPos = cmds.xform(pin, query=True, m = True, ws = True)
        cmds.xform(newCtrl, m = pinPos, ws = True)

        ctrls.append(newCtrl)

        cmds.parent(newCtrl, pin)
        cmds.select(clear=True)
        cmds.select(newCtrl)
        zroNode = ZeroOffsetFunction.insertNodeBefore(sfx = "zro")
        cmds.select(clear=True)
        cmds.select(newCtrl)
        offsetNode = ZeroOffsetFunction.insertNodeBefore(sfx = "off")[0]

        offsets.append(offsetNode)
        cmds.select(clear=True)
        cmds.select(offsetNode)
        MatrixZeroOffset.createMatrixZeroOffset(offsetNode)
    
    cmds.parent(offsets, "torsoPlates_Controls_grp")
    return ctrls

def createJoints(ctrls):

    plateJoints = []

    for ctrl in ctrls:
        cmds.select(clear=True)
        print(ctrl)
        newJnt = cmds.joint(name = ctrl.replace("ctrl", "skn"))
        pinPos = cmds.xform(ctrl, query = True, m = True, ws = True)
        cmds.xform(newJnt, m = pinPos, ws = True)
        cmds.parent(newJnt, ctrl)
        cmds.select(clear=True)
        plateJoints.append(newJnt)

        cmds.select(newJnt)
        zroNode = ZeroOffsetFunction.insertNodeBefore(sfx = "zro")

        cmds.select(clear=True)
        cmds.select(newJnt)
        MatrixZeroOffset.createMatrixZeroOffset(newJnt)

    cmds.parent(plateJoints, "torsoPlates_joints_grp")
    return plateJoints

def createProximityPin(baseModel):
    pins = cmds.listRelatives("torsoPlates_Pins_grp")

    cmds.select(clear=True)
    cmds.select(baseModel, add=True)
    for pin in pins:
        cmds.select(pin, add=True)

    maya.internal.common.cmd.base.executeCommand('proximitypin.cmd_create')

def platesInput():

    guideGrp = "cn_torsoPlates_guides_grp"
    baseModel = "Model_V004:cn_base_geo"

    createPlatesHirarchy()

    guides = cmds.listRelatives(guideGrp)

    pinList = createPinLocators(guides)
    print("Successfully created pin Locators")

    ctrls = createPlateCtrls(pinList)

    plateJoints = createJoints(ctrls)
    print("Successfully created joints")

    createProximityPin(baseModel)



    

# cmds.select(clear = True)
# cmds.select(plateJoints)
# ZeroOffsetFunction.insertNodeBefore()
# cmds.select(clear = True)
# cmds.select(plateJoints)
# MatrixZeroOffset.iterateCreateMatrixZeroOffset()
# cmds.parent(plateJoints, "torsoPlates_joints_grp")
