import maya.cmds as cmds
import maya.internal.common.cmd.base

def createPlatesHirarchy():
    mainGrp = cmds.createNode("transform", name = "cn_TorsoPlates_Rig_grp")

    ctrlGrp = cmds.createNode("transform", name = "torsoPlates_Controls_grp", parent = mainGrp)
    pinGrp = cmds.createNode("transform",  name = "trosoPates_Pins_grp", parent = mainGrp)
    jointsGrp = cmds.createNode("transform",  name = "trosoPates_joints_grp", parent = mainGrp)

def createPlatePins(meshTargetList):
    locators = []
    for index, i in enumerate(meshTargetList):
        cmds.select(clear=True)
        cmds.select(i)
        sel = cmds.ls(sl = True, dag = True, type = "mesh")[0]
        vtxList = cmds.ls("{}.vtx[:]".format(sel), fl = True)
        cmds.select(clear=True)
        # Initialize our cntr_pos variable to "0" to start, these 3 values represent XYZ positions
        cntr_pos = [0.0, 0.0, 0.0]

        # Loop through each selection and add it's XYZ position to cntr_pos
        for j in range(0, len(vtxList)):
            # Check if node is a transform/joint OR a component vertex/CV
            # If a transform, we'll use the "piv" flag in the xform command for accuracy
            if "transform" in cmds.nodeType(vtxList[j]) or "jojnt" in cmds.nodeType(vtxList[j]):
               
                pos = cmds.xform(vtxList[j], query=True, worldSpace=True, piv=True)

            # Otherwise, we'll use the "translation" flag for all else, including components
            else:
               
                pos = cmds.xform(vtxList[j], query=True, worldSpace=True, translation=True)

            cntr_pos[0] = pos[0] + cntr_pos[0]
            cntr_pos[1] = pos[1] + cntr_pos[1]
            cntr_pos[2] = pos[2] + cntr_pos[2]

        # Now divide the sum of all the positions by the number of selected items
        cntr_pos[0] = cntr_pos[0] / len(vtxList)
        cntr_pos[1] = cntr_pos[1] / len(vtxList)
        cntr_pos[2] = cntr_pos[2] / len(vtxList)

        # Create a locator and set it's position to the final cntr_pos value
        loc = cmds.spaceLocator(p=[0, 0, 0], name = f"{i}_outPin")
        locators.append(loc)
        cmds.setAttr(loc[0] + ".translate", cntr_pos[0], cntr_pos[1], cntr_pos[2])
        cmds.parent(loc, "trosoPates_Pins_grp")
    
    return locators

def createJoints(pins):

    plateJoints = []

    for pin in pins():
        cmds.select(clear=True)
        newJnt = cmds.joint(name = pin.replace("outPin", "skn"))
        pinPos = cmds.xform(pin, query = True, m = True, ws = True)
        cmds.xform(newJnt, m = pinPos, ws = True)
        cmds.parent(newJnt, pin)
        cmds.select(clear=True)
    
    return plateJoints

def platesInput():
    plateGroup = ["Model_V004:front_plates_grp", "Model_V004:side_plates_grp", "Model_V004:back_plates_grp"]

    createPlatesHirarchy()

    pinList = []

    for grp in plateGroup:
        meshList = cmds.listRelatives(grp)
        locators = createPlatePins(meshList)
        pinList.append(locators)

    plateJoints = createJoints(pinList)


#maya.internal.common.cmd.base.executeCommand('proximitypin.cmd_create')
    

