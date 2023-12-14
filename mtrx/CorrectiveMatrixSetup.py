import maya.cmds as cmds
from tlpf_toolkit.ctrls import CtrlColorFunction

#=======================================
## Ball Joint Corrective Tool 
#=======================================

def ballJointCorrectiveSystemUI():

    #basic Window creation
    configWindow = cmds.window(title="CorrectiveSystemV01", iconName='Corrective', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.columnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Corrective Setup Tool", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])

    followLabel = cmds.text(label ="Follow Object: ", width = 100)
    targetLabel = cmds.text(label ="Target Object: ", width = 100)
    parentLabel = cmds.text(label = "Parent Object: ", width = 100)
    
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])    

    followObjectBtn = cmds.button(label = "Set flw", width = 100, command = lambda _: toggleDefButton(followObjectBtn, [0, 0.5, 0], [targetObjectBtn, followObjectBtn, parentObjectBtn], 
                                                                                                      [forwardReferenceLocatorBtn, forwardCorrectedLocatorBtn, 
                                                                                                        backReferenceLocatorBtn, backCorrectedLocatorBtn,
                                                                                                        sideReferenceLocatorBtn, sideCorrectedLocatorBtn]))
    targetObjectBtn = cmds.button(label = "Set trg", width = 100, enable = False, command = lambda _: toggleDefButton(targetObjectBtn, [0, 0.5, 0], [targetObjectBtn, followObjectBtn, parentObjectBtn], 
                                                                                                                      [forwardReferenceLocatorBtn, forwardCorrectedLocatorBtn, 
                                                                                                                        backReferenceLocatorBtn, backCorrectedLocatorBtn,
                                                                                                                        sideReferenceLocatorBtn, sideCorrectedLocatorBtn]))
    parentObjectBtn = cmds.button(label = "Set par", width = 100, command = lambda _: toggleDefButton(parentObjectBtn, [0, 0.5, 0], [targetObjectBtn, followObjectBtn, parentObjectBtn], 
                                                                                                      [forwardReferenceLocatorBtn, forwardCorrectedLocatorBtn, 
                                                                                                       backReferenceLocatorBtn, backCorrectedLocatorBtn,
                                                                                                       sideReferenceLocatorBtn, sideCorrectedLocatorBtn]))
    
    
    cmds.setParent('..')

    cmds.columnLayout(adjustableColumn=True) 

    forwardPoseLabel = cmds.text(label="Forward Pose", height = 20, backgroundColor = [.3, .3, .3])
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])
    
    forwardReferenceLocatorLabel = cmds.text(label ="Reference Pos", width = 150)
    forwardCorrectionLocatorLabel = cmds.text(label = "Corrective Pos", width = 150)

    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])

    forwardReferenceLocatorBtn = cmds.button(label ="Set", width = 150, enable = False, command = lambda _: referenceLocatorButton(forwardReferenceLocatorBtn, 
                                                                                                                                cmds.button(targetObjectBtn, query = True, label = True),
                                                                                                                                cmds.button(parentObjectBtn, query = True, label = True),
                                                                                                                                "ForwardPose",
                                                                                                                                [0, 0.5, 0]))
    forwardCorrectedLocatorBtn = cmds.button(label ="Set", width = 150, enable = False, command = lambda _: correctionLocatorButton(forwardCorrectedLocatorBtn, 
                                                                                                                                cmds.button(targetObjectBtn, query = True, label = True),
                                                                                                                                cmds.button(followObjectBtn, query = True, label = True),
                                                                                                                                "ForwardPose",
                                                                                                                                [0, 0.5, 0]))

    cmds.setParent('..')

    #Space Divider
    cmds.text(label="", height=10)

    cmds.columnLayout(adjustableColumn=True) 

    backPoseLabel = cmds.text(label="Back Pose", height = 20, backgroundColor = [.3, .3, .3])
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])
    
    backReferenceLocatorLabel = cmds.text(label ="Reference Pos", width = 150)
    backCorrectionLocatorLabel = cmds.text(label = "Corrective Pos", width = 150)

    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])

    backReferenceLocatorBtn = cmds.button(label ="Set", width = 150, enable = False, command = lambda _: referenceLocatorButton(backReferenceLocatorBtn, 
                                                                                                                                cmds.button(targetObjectBtn, query = True, label = True),
                                                                                                                                cmds.button(parentObjectBtn, query = True, label = True),
                                                                                                                                "BackPose",
                                                                                                                                [0, 0.5, 0]))
    backCorrectedLocatorBtn = cmds.button(label ="Set", width = 150, enable = False, command = lambda _: correctionLocatorButton(backCorrectedLocatorBtn, 
                                                                                                                                cmds.button(targetObjectBtn, query = True, label = True),
                                                                                                                                cmds.button(followObjectBtn, query = True, label = True),
                                                                                                                                "BackPose",
                                                                                                                                [0, 0.5, 0]))
    cmds.setParent('..')

    #Space Divider
    cmds.text(label="", height=10)

    cmds.columnLayout(adjustableColumn=True) 

    backPoseLabel = cmds.text(label="Side Pose", height = 20, backgroundColor = [.3, .3, .3])
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])
    
    sideReferenceLocatorLabel = cmds.text(label ="Reference Pos", width = 150)
    sideCorrectionLocatorLabel = cmds.text(label = "Corrective Pos", width = 150)

    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])

    sideReferenceLocatorBtn = cmds.button(label ="Set", width = 150, enable = False, command = lambda _: referenceLocatorButton(sideReferenceLocatorBtn, 
                                                                                                                                cmds.button(targetObjectBtn, query = True, label = True),
                                                                                                                                cmds.button(parentObjectBtn, query = True, label = True),
                                                                                                                                "SidePose",
                                                                                                                                [0, 0.5, 0]))
    sideCorrectedLocatorBtn = cmds.button(label ="Set", width = 150, enable = False, command = lambda _: correctionLocatorButton(sideCorrectedLocatorBtn, 
                                                                                                                                cmds.button(targetObjectBtn, query = True, label = True),
                                                                                                                                cmds.button(followObjectBtn, query = True, label = True),
                                                                                                                                "SidePose",
                                                                                                                                [0, 0.5, 0]))
    cmds.setParent('..')

    #Space Divider
    cmds.text(label="", height=10)

    doVisibilityCtrl = cmds.checkBox(label = "Add Visibility Ctrl", value = False, changeCommand = lambda _: toggleVisibilityCtrlCheckBox(visibilityCtrlObjectBtn))

    visibilityCtrlObjectBtn = cmds.button(label = "Set Object", enable = False, command = lambda _: setVisibilityCtrlObject(visibilityCtrlObjectBtn))

    #Space Divider
    cmds.text(label="", height=10)

    doEnvelope = cmds.checkBox(label = "Add Global Ctrl", value = False, changeCommand = lambda _: toggleVisibilityCtrlCheckBox(envelopeCtrlAttrBtn))

    envelopeCtrlAttrBtn = cmds.button(label = "Set Object", enable = False, command = lambda _: setVisibilityCtrlObject(envelopeCtrlAttrBtn))

    #Build Ribbon Label
    buildCorrectiveSystemLabel = cmds.text(label="Create Corrective System", height = 20, backgroundColor = [.3, .3, .3])

    #create Guides Button
    buildSystemButton = cmds.button(label="Build System", height = 40, command = lambda _: buildBallJointCorrectiveSystem(
                                                                                                                 cmds.button(targetObjectBtn, query=True, label = True),
                                                                                                                 cmds.button(followObjectBtn, query = True, label = True),
                                                                                                                 cmds.button(parentObjectBtn, query = True, label = True),
                                                                                                                 cmds.button(forwardReferenceLocatorBtn, query = True, label = True),
                                                                                                                 cmds.button(forwardCorrectedLocatorBtn, query = True, label = True),
                                                                                                                 cmds.button(backReferenceLocatorBtn, query = True, label = True),
                                                                                                                 cmds.button(backCorrectedLocatorBtn, query = True, label = True),
                                                                                                                 cmds.button(sideReferenceLocatorBtn, query = True, label = True),
                                                                                                                 cmds.button(sideCorrectedLocatorBtn, query = True, label = True),
                                                                                                                 [cmds.checkBox(doVisibilityCtrl, query = True, value = True), cmds.button(visibilityCtrlObjectBtn, query = True, label = True)],
                                                                                                                 [cmds.checkBox(doEnvelope, query = True, value = True), cmds.button(envelopeCtrlAttrBtn, query = True, label = True)]))
 
    
    #show Window
    cmds.showWindow(configWindow)

def referenceLocatorButton(button, name, parentObject, poseName, color):
    sel = cmds.ls(selection = True)[0]
    posMatrix = cmds.xform(sel, query = True, ws=True, m = True)

    newLoc = cmds.spaceLocator(name = f"{name}_{poseName}ReferenceLocator")[0]

    cmds.xform(newLoc, m = posMatrix, ws = True)
    cmds.parent(newLoc, parentObject)
    cmds.button(button, edit = True, backgroundColor = color)
    cmds.button(button, edit = True, label = newLoc)

def correctionLocatorButton(button, name, parentObject, poseName, color):
    sel = cmds.ls(selection = True)[0]
    posMatrix = cmds.xform(sel, query = True, ws=True, m = True)

    newLoc = cmds.spaceLocator(name = f"{name}_{poseName}CorrectedLocator")[0]

    cmds.xform(newLoc, m = posMatrix, ws = True)
    cmds.parent(newLoc, parentObject)
    cmds.button(button, edit = True, backgroundColor = color)
    cmds.button(button, edit = True, label = newLoc)

    cmds.select(clear=True)
    cmds.select(newLoc)
    CtrlColorFunction.setCtrlShapeColorAttribute(color, False)

def getButtonColor(button):

    buttonColor = cmds.button(button, query = True, backgroundColor= True)
    buttonColorR = round(buttonColor[0], 1)
    buttonColorG = round(buttonColor[1], 1)
    buttonColorB = round(buttonColor[2], 1)

    buttonColorRound = [buttonColorR, buttonColorG, buttonColorB]

    return buttonColorRound

def togglePoseButton(buttons, targetButtons):

    firstButtonColor = getButtonColor(buttons[0])

    if firstButtonColor != [0, 0.5, 0]:
        return
    else:
        secondButtonColor = getButtonColor(buttons[1])
       
        if secondButtonColor != [0, 0.5, 0]:
            return
        else:
            thirdButtonColor = getButtonColor(buttons[2])

            if thirdButtonColor != [0, 0.5, 0]:
                return
            else:
                for i in targetButtons:
                    cmds.button(i, edit = True, enable = True)

def toggleDefButton(button, color, evalButtons, activationButtons):
    
    sel = cmds.ls(selection = True)[0]

    print(cmds.button(button, query = True, label = True))

    if cmds.button(button, query = True, label = True) == "Set flw":
        cmds.button(evalButtons[0], edit = True, enable = True)

    if cmds.button(button, query = True, label = True) == "Set trg":
        createBrokenLocator(sel, evalButtons[1])

    cmds.button(button, edit = True, label = sel)
    cmds.button(button, edit = True, backgroundColor = color)

    togglePoseButton(evalButtons, activationButtons)

def createBrokenLocator(name, follow):
    newLoc = cmds.spaceLocator(name = f"{name}_Broken")[0]
    posMatrix = cmds.xform(name, query = True, m = True, ws = True)

    cmds.parent(newLoc, cmds.button(follow, query = True, label =True))

    cmds.xform(newLoc, m = posMatrix, ws = True)
    cmds.select(clear=True)
    cmds.select(newLoc)
    CtrlColorFunction.setCtrlShapeColorAttribute([1, 0, 0], False)
    cmds.select(clear=True)

def toggleVisibilityCtrlCheckBox(button):
    buttonState = cmds.button(button, query = True, enable  = True)
    cmds.button(button, edit = True, enable = not buttonState)

def setVisibilityCtrlObject(button):
    sel = cmds.ls(selection = True)[0]
    cmds.button(button, edit = True, label = sel)
    cmds.button(button, edit = True, backgroundColor = [0, 0.5, 0])

def buildBallJointCorrectiveSystem(targetObject, followObject, parentObject, forwardPoseReferenceLoc, forwardPoseCorrectedLoc, backPoseReferenceLoc, backPoseCorrectedLoc, sidePoseReferenceLoc, sidePoseCorrectedLoc, visibilityCtrl, globalCtrl):
    forwardDistance = cmds.createNode("distanceBetween", name = f"{forwardPoseReferenceLoc}_{targetObject}_Broken_Distance")

    cmds.connectAttr(f"{forwardPoseReferenceLoc}.worldMatrix[0]", f"{forwardDistance}.inMatrix1")
    cmds.connectAttr(f"{targetObject}_Broken.worldMatrix[0]", f"{forwardDistance}.inMatrix2")

    backDistance = cmds.createNode("distanceBetween", name = f"{backPoseReferenceLoc}_{targetObject}_Broken_Distance")

    cmds.connectAttr(f"{backPoseReferenceLoc}.worldMatrix[0]", f"{backDistance}.inMatrix1")
    cmds.connectAttr(f"{targetObject}_Broken.worldMatrix[0]", f"{backDistance}.inMatrix2")

    sideDistance = cmds.createNode("distanceBetween", name = f"{sidePoseReferenceLoc}_{targetObject}_Broken_Distance")

    cmds.connectAttr(f"{sidePoseReferenceLoc}.worldMatrix[0]", f"{sideDistance}.inMatrix1")
    cmds.connectAttr(f"{targetObject}_Broken.worldMatrix[0]", f"{sideDistance}.inMatrix2")

    remapValueRange = cmds.createNode("setRange", name = f"{targetObject}_remapDistanceValues")

    cmds.connectAttr(f"{forwardDistance}.distance", f"{remapValueRange}.valueX")
    cmds.connectAttr(f"{backDistance}.distance", f"{remapValueRange}.valueY")
    cmds.connectAttr(f"{sideDistance}.distance", f"{remapValueRange}.valueZ")

    forwardMax = cmds.getAttr(f"{forwardDistance}.distance")
    backMax = cmds.getAttr(f"{backDistance}.distance")
    sideMax = cmds.getAttr(f"{sideDistance}.distance")

    cmds.setAttr(f"{remapValueRange}.oldMaxX", forwardMax)
    cmds.setAttr(f"{remapValueRange}.oldMaxY", backMax)
    cmds.setAttr(f"{remapValueRange}.oldMaxZ", sideMax)

    cmds.setAttr(f"{remapValueRange}.maxX", 1)
    cmds.setAttr(f"{remapValueRange}.maxY", 1)
    cmds.setAttr(f"{remapValueRange}.maxZ", 1)

    reverse = cmds.createNode("reverse", name = f"{targetObject}_reverseRemapedValue")

    cmds.connectAttr(f"{remapValueRange}.outValueX", f"{reverse}.inputX")
    cmds.connectAttr(f"{remapValueRange}.outValueY", f"{reverse}.inputY")
    cmds.connectAttr(f"{remapValueRange}.outValueZ", f"{reverse}.inputZ")

    blendMatrix = cmds.createNode("blendMatrix", name = f"{targetObject}_CorrectiveBlendMatrix")

    cmds.connectAttr(f"{targetObject}_Broken.xformMatrix", f"{blendMatrix}.inputMatrix")

    cmds.connectAttr(f"{forwardPoseCorrectedLoc}.xformMatrix", f"{blendMatrix}.target[0].targetMatrix")
    cmds.connectAttr(f"{reverse}.outputX", f"{blendMatrix}.target[0].weight")

    cmds.connectAttr(f"{backPoseCorrectedLoc}.xformMatrix", f"{blendMatrix}.target[1].targetMatrix")
    cmds.connectAttr(f"{reverse}.outputY", f"{blendMatrix}.target[1].weight")

    cmds.connectAttr(f"{sidePoseCorrectedLoc}.xformMatrix", f"{blendMatrix}.target[2].targetMatrix")
    cmds.connectAttr(f"{reverse}.outputZ", f"{blendMatrix}.target[2].weight")


    cmds.connectAttr(f"{blendMatrix}.outputMatrix", f"{targetObject}.offsetParentMatrix", force = True)

    for i in "XYZ":
        cmds.setAttr(f"{targetObject}.translate{i}", 0)
        cmds.setAttr(f"{targetObject}.rotate{i}", 0)
        cmds.setAttr(f"{targetObject}.scale{i}", 1)


    if visibilityCtrl[0]:
        cmds.addAttr(f"{visibilityCtrl[1]}", at = "enum", ln = f"{targetObject}_CorrectiveSystem", enumName = "OFF:ON")
        cmds.setAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", cb = True)

        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{forwardPoseReferenceLoc}.visibility")
        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{forwardPoseCorrectedLoc}.visibility")

        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{backPoseReferenceLoc}.visibility")
        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{backPoseCorrectedLoc}.visibility")

        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{sidePoseReferenceLoc}.visibility")
        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{sidePoseCorrectedLoc}.visibility")

        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{targetObject}_Broken.visibility")

    if globalCtrl[0]:
        cmds.connectAttr(f"{globalCtrl[1]}.CorrectiveSystem", f"{blendMatrix}.envelope")

#=======================================
## Ball Joint Corrective Tool - END
#=======================================

#=======================================
## Hinge Joint Corrective Tool 
#=======================================

def hingeJointCorrectiveSystemUI():

    #basic Window creation
    configWindow = cmds.window(title="CorrectiveSystemV01", iconName='Corrective', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.columnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Corrective Setup Tool", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])

    followLabel = cmds.text(label ="Follow Object: ", width = 100)
    targetLabel = cmds.text(label ="Target Object: ", width = 100)
    parentLabel = cmds.text(label = "Parent Object: ", width = 100)
    
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 3, columnWidth3 = [100, 100, 100])    

    followObjectBtn = cmds.button(label = "Set flw", width = 100, command = lambda _: toggleDefButton(followObjectBtn, [0, 0.5, 0], [targetObjectBtn, followObjectBtn, parentObjectBtn], 
                                                                                                      [backReferenceLocatorBtn, backCorrectedLocatorBtn,]))
    targetObjectBtn = cmds.button(label = "Set trg", width = 100, enable = False, command = lambda _: toggleDefButton(targetObjectBtn, [0, 0.5, 0], [targetObjectBtn, followObjectBtn, parentObjectBtn], 
                                                                                                                      [backReferenceLocatorBtn, backCorrectedLocatorBtn]))
    parentObjectBtn = cmds.button(label = "Set par", width = 100, command = lambda _: toggleDefButton(parentObjectBtn, [0, 0.5, 0], [targetObjectBtn, followObjectBtn, parentObjectBtn], 
                                                                                                      [ backReferenceLocatorBtn, backCorrectedLocatorBtn]))
    
    
    cmds.setParent('..')

    #Space Divider
    cmds.text(label="", height=10)

    cmds.columnLayout(adjustableColumn=True) 

    backPoseLabel = cmds.text(label="Back Pose", height = 20, backgroundColor = [.3, .3, .3])
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])
    
    backReferenceLocatorLabel = cmds.text(label ="Reference Pos", width = 150)
    backCorrectionLocatorLabel = cmds.text(label = "Corrective Pos", width = 150)

    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])

    backReferenceLocatorBtn = cmds.button(label ="Set", width = 150, enable = False, command = lambda _: referenceLocatorButton(backReferenceLocatorBtn, 
                                                                                                                                cmds.button(targetObjectBtn, query = True, label = True),
                                                                                                                                cmds.button(parentObjectBtn, query = True, label = True),
                                                                                                                                "BackPose",
                                                                                                                                [0, 0.5, 0]))
    backCorrectedLocatorBtn = cmds.button(label ="Set", width = 150, enable = False, command = lambda _: correctionLocatorButton(backCorrectedLocatorBtn, 
                                                                                                                                cmds.button(targetObjectBtn, query = True, label = True),
                                                                                                                                cmds.button(followObjectBtn, query = True, label = True),
                                                                                                                                "BackPose",
                                                                                                                                [0, 0.5, 0]))
    cmds.setParent('..')

    #Space Divider
    cmds.text(label="", height=10)

    doVisibilityCtrl = cmds.checkBox(label = "Add Visibility Ctrl", value = False, changeCommand = lambda _: toggleVisibilityCtrlCheckBox(visibilityCtrlObjectBtn))

    visibilityCtrlObjectBtn = cmds.button(label = "Set Object", enable = False, command = lambda _: setVisibilityCtrlObject(visibilityCtrlObjectBtn))

    #Space Divider
    cmds.text(label="", height=10)

    doEnvelope = cmds.checkBox(label = "Add Global Ctrl", value = False, changeCommand = lambda _: toggleVisibilityCtrlCheckBox(envelopeCtrlAttrBtn))

    envelopeCtrlAttrBtn = cmds.button(label = "Set Object", enable = False, command = lambda _: setVisibilityCtrlObject(envelopeCtrlAttrBtn))

    #Build Ribbon Label
    buildCorrectiveSystemLabel = cmds.text(label="Create Corrective System", height = 20, backgroundColor = [.3, .3, .3])

    #create Guides Button
    buildSystemButton = cmds.button(label="Build System", height = 40, command = lambda _: buildHingeJointCorrectiveSystem(
                                                                                                                 cmds.button(targetObjectBtn, query=True, label = True),
                                                                                                                 cmds.button(followObjectBtn, query = True, label = True),
                                                                                                                 cmds.button(parentObjectBtn, query = True, label = True),
                                                                                                                 cmds.button(backReferenceLocatorBtn, query = True, label = True),
                                                                                                                 cmds.button(backCorrectedLocatorBtn, query = True, label = True),
                                                                                                                 [cmds.checkBox(doVisibilityCtrl, query = True, value = True), cmds.button(visibilityCtrlObjectBtn, query = True, label = True)],
                                                                                                                 [cmds.checkBox(doEnvelope, query = True, value = True), cmds.button(envelopeCtrlAttrBtn, query = True, label = True)]))
 
    
    #show Window
    cmds.showWindow(configWindow)

def buildHingeJointCorrectiveSystem(targetObject, followObject, parentObject, backPoseReferenceLoc, backPoseCorrectedLoc, visibilityCtrl, globalCtrl):

    backDistance = cmds.createNode("distanceBetween", name = f"{backPoseReferenceLoc}_{targetObject}_Broken_Distance")

    cmds.connectAttr(f"{backPoseReferenceLoc}.worldMatrix[0]", f"{backDistance}.inMatrix1")
    cmds.connectAttr(f"{targetObject}_Broken.worldMatrix[0]", f"{backDistance}.inMatrix2")

    remapValueRange = cmds.createNode("setRange", name = f"{targetObject}_remapDistanceValues")

    cmds.connectAttr(f"{backDistance}.distance", f"{remapValueRange}.valueY")

    backMax = cmds.getAttr(f"{backDistance}.distance")

    cmds.setAttr(f"{remapValueRange}.oldMaxY", backMax)

    cmds.setAttr(f"{remapValueRange}.maxY", 1)

    reverse = cmds.createNode("reverse", name = f"{targetObject}_reverseRemapedValue")

    cmds.connectAttr(f"{remapValueRange}.outValueY", f"{reverse}.inputY")


    blendMatrix = cmds.createNode("blendMatrix", name = f"{targetObject}_CorrectiveBlendMatrix")

    cmds.connectAttr(f"{targetObject}_Broken.xformMatrix", f"{blendMatrix}.inputMatrix")

    cmds.connectAttr(f"{backPoseCorrectedLoc}.xformMatrix", f"{blendMatrix}.target[1].targetMatrix")
    cmds.connectAttr(f"{reverse}.outputY", f"{blendMatrix}.target[1].weight")


    cmds.connectAttr(f"{blendMatrix}.outputMatrix", f"{targetObject}.offsetParentMatrix", force = True)

    for i in "XYZ":
        cmds.setAttr(f"{targetObject}.translate{i}", 0)
        cmds.setAttr(f"{targetObject}.rotate{i}", 0)
        cmds.setAttr(f"{targetObject}.scale{i}", 1)


    if visibilityCtrl[0]:
        cmds.addAttr(f"{visibilityCtrl[1]}", at = "enum", ln = f"{targetObject}_CorrectiveSystem", enumName = "OFF:ON")
        cmds.setAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", cb = True)

        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{backPoseReferenceLoc}.visibility")
        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{backPoseCorrectedLoc}.visibility")

        cmds.connectAttr(f"{visibilityCtrl[1]}.{targetObject}_CorrectiveSystem", f"{targetObject}_Broken.visibility")

    if globalCtrl[0]:
        cmds.connectAttr(f"{globalCtrl[1]}.CorrectiveSystem", f"{blendMatrix}.envelope")

#=======================================
## Hinge Joint Corrective Tool - END
#=======================================