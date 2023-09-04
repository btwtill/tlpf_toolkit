#Module Import
from tlpf_toolkit.utils import GeneralFunctions
import maya.cmds as cmds


#=======================================
## Simple Stetch Function
#=======================================
def SimpleStretchSetupConfigInterface():
    
    #basic Window creation
    configWindow = cmds.window(title="SamStretchSetup", iconName='SamStretch', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.rowColumnLayout( adjustableColumn=True )
    
    
    cmds.text( label='Inputs', font = "boldLabelFont", height=30)

    upperJointPos = buildUserInputGrp("Set upper Pos", "Not Defined", 30)

    midJointPos = buildUserInputGrp("Set mid Pos", "Not Defined", 30)

    lowerJointPos = buildUserInputGrp("Set lower Pos", "Not Defined", 30)

    anchor = buildUserInputGrp("Set anchor Pos", "Not Defined", 30)

    poleVector = buildUserInputGrp("Set polevector Pos", "Not Defined", 30)

    endCtrl = buildUserInputGrp("Set endCtrl Pos", "Not Defined", 30)

    cmds.button("Build Sam Stretch Setup", command=lambda _: BuildStretchSetup(upperJointPos, midJointPos, lowerJointPos, anchor, poleVector, endCtrl))

    #Display The window
    cmds.showWindow(configWindow)

def displayInput(_input):
    print(_input)

def displayUserInput(input):
    print(cmds.text(input, query=True, label=True))

def buildUserInputGrp(buttonLabel, displayLabelText, displayLabelHeight):
    cmds.text(label="", height=10, backgroundColor=[0.0,0.0,0.0])
    cmds.button(label=buttonLabel, height=40, command=lambda _: updateLabel(labelname, getFirstUserSelection()))
    labelname = cmds.text(label=displayLabelText, height=displayLabelHeight, backgroundColor=[1.0, 0.0, 0.0])
    return labelname

def getFirstUserSelection():
    sel = cmds.ls(selection=True)
    return sel[0]

def updateLabel(_label, _newLabelText):
    rgbColor = [0.2, 0.2, 0.2]
    cmds.text(_label, edit=True, label=_newLabelText, backgroundColor=rgbColor)

def getCharacterSideNamingConvention(context):
    leftFilterString = ["L_", "l_", "lf_", "LF_", "Left_", "left_"]
    rightFilterStrings = ["R_", "r_", "ri_", "RI_", "Right", "right"]

    rightEntrys = GeneralFunctions.filter_strings(context, rightFilterStrings)
    leftEntrys = GeneralFunctions.filter_strings(context, leftFilterString)

    if rightEntrys:
        return "_r_"
    elif leftEntrys:
        return "_l_"
    else:
        return "Not_Defined"
    
def getUserEntries(entries):
    entrieList = []
    for i in entries:
        newentry = cmds.text(i, query=True, label=True)
        entrieList.append(newentry)
    return entrieList
    
def getUserEntry(entry):
    return cmds.text(entry, query=True, label=True)

def getLimbType(target):
    if "Wrist_" in target or "wrist_" in target or "Hand_" in target or "hand_" in target:
        return "arm_"
    elif "Foot" in target or "foot" in target or "Ankle" in target or "ankle" in target:
        return "leg_"
    else:
        return "Not_Defined"

def createDefaultChain(_targetChain):
        return GeneralFunctions.removeOneAndPrefixName(GeneralFunctions.duplicateSelection(_targetChain), "def_")

def addStretchAttributes(targetObject, attributes):
        cmds.addAttr(targetObject, longName=attributes[0], attributeType="enum", keyable=True, enumName='*****')
        cmds.addAttr(targetObject, longName=attributes[1], attributeType="float", keyable=True, minValue=0, maxValue=1)
        cmds.addAttr(targetObject, longName=attributes[2], attributeType="float", keyable=True, minValue=0, maxValue=1)
        cmds.addAttr(targetObject, longName=attributes[3], attributeType="float", keyable=True)
        cmds.addAttr(targetObject, longName=attributes[4], attributeType="float", keyable=True, minValue=0, defaultValue=2)

def setupConnections(_End_ctrl, _PoleVector_ctrl, _anchor, _side, _DefaultIKChain, _stretchAttributes, _limbType, _IkJointList):

        #Anchor to Pole Vector
        upperLength = cmds.rename(cmds.createNode('distanceBetween'), _side + _limbType + "upper_lenght")

        cmds.connectAttr(_anchor + ".worldMatrix[0]", upperLength + ".inMatrix1")
        cmds.connectAttr(_PoleVector_ctrl + ".worldMatrix[0]", upperLength + ".inMatrix2")

        #Pole Vector to End

        lowerLength = cmds.rename(cmds.createNode('distanceBetween'), _side + _limbType +  "lower_lenght")

        cmds.connectAttr(_PoleVector_ctrl + ".worldMatrix[0]", lowerLength + ".inMatrix1")
        cmds.connectAttr(_End_ctrl + ".worldMatrix[0]", lowerLength + ".inMatrix2")

        #ChainLenght
        activeLenght = cmds.rename(cmds.createNode('distanceBetween'), _side + _limbType +  "lenght")

        cmds.connectAttr(_anchor + ".worldMatrix[0]", activeLenght + ".inMatrix1")
        cmds.connectAttr(_End_ctrl + ".worldMatrix[0]", activeLenght + ".inMatrix2")

        #Default Distance Calculation

        defaultUpperLenght = cmds.rename(cmds.createNode('distanceBetween'), _side + _limbType +  "default_upper_lenght")

        cmds.connectAttr(_DefaultIKChain[0] + '.worldMatrix[0]', defaultUpperLenght + ".inMatrix1")
        cmds.connectAttr(_DefaultIKChain[1] + '.worldMatrix[0]', defaultUpperLenght + ".inMatrix2")

        defaultLowerLenght = cmds.rename(cmds.createNode('distanceBetween'), _side + _limbType +  "default_lower_lenght")

        cmds.connectAttr(_DefaultIKChain[1] + '.worldMatrix[0]', defaultLowerLenght + ".inMatrix1")
        cmds.connectAttr(_DefaultIKChain[2] + '.worldMatrix[0]', defaultLowerLenght + ".inMatrix2")

        defaultLenght = cmds.rename(cmds.createNode('distanceBetween'), _side + _limbType +  "default_lenght")

        cmds.connectAttr(_DefaultIKChain[0] + '.worldMatrix[0]', defaultLenght + ".inMatrix1")
        cmds.connectAttr(_DefaultIKChain[2] + '.worldMatrix[0]', defaultLenght + ".inMatrix2")

        #calculate stretch value with active and default length values
        stretchValue = cmds.rename(cmds.createNode('floatMath'), _side + _limbType +  "stretch_value")

        cmds.connectAttr(activeLenght + ".distance", stretchValue + ".floatA")
        cmds.connectAttr(defaultLenght + ".distance", stretchValue + ".floatB")
        cmds.setAttr(stretchValue + ".operation", 3)

        #implement max stretch attribute with clamp node
        maxStretch = cmds.rename(cmds.createNode('clamp'), _side + _limbType +  "Max_Stretch")

        cmds.setAttr(maxStretch + ".minR", 1)

        cmds.connectAttr(stretchValue + ".outFloat", maxStretch + ".inputR")
        cmds.connectAttr(_End_ctrl + "." + _stretchAttributes[4], maxStretch + ".maxR")

        #implement do Stretch attribute with blend two attributes node
        doStretch = cmds.rename(cmds.createNode('blendTwoAttr'), _side + _limbType +  "DoStretch")

        cmds.connectAttr(maxStretch + ".outputR", doStretch + ".input[1]")
        cmds.connectAttr(_End_ctrl + "." + _stretchAttributes[1], doStretch + ".attributesBlender")
        cmds.setAttr(doStretch + ".input[0]", 1)

        #Multiply default upper and lower lenght with multiply value
        stretchMult = cmds.rename(cmds.createNode('multiplyDivide'), _side + _limbType +  "Stretch_Multiplication")

        cmds.connectAttr(doStretch + ".output", stretchMult + ".input2X")
        cmds.connectAttr(doStretch + ".output", stretchMult + ".input2Y")

        cmds.connectAttr(defaultUpperLenght + ".distance", stretchMult + ".input1X")
        cmds.connectAttr(defaultLowerLenght + ".distance", stretchMult + ".input1Y")

        #Implement nudge multiplication with nudge attribute
        nudgeMult = cmds.rename(cmds.createNode('multDoubleLinear'), _side + _limbType +  "Nudge_Multiplication")

        cmds.connectAttr(_End_ctrl + "." + _stretchAttributes[3], nudgeMult + ".input1")
        cmds.setAttr(nudgeMult + ".input2", 0.01)

        #add the nudge value on
        nudgeAddition = cmds.rename(cmds.createNode('plusMinusAverage'), _side + _limbType +  "Nudge_Addition")

        cmds.connectAttr(stretchMult + ".outputX", nudgeAddition + ".input2D[0].input2Dx")
        cmds.connectAttr(stretchMult + ".outputY", nudgeAddition + ".input2D[0].input2Dy")

        cmds.connectAttr(nudgeMult + ".output", nudgeAddition + ".input2D[1].input2Dx")
        cmds.connectAttr(nudgeMult + ".output", nudgeAddition + ".input2D[1].input2Dy")

        #implement knee pin with two blendtwoAttr nodes
        upperPin = cmds.rename(cmds.createNode('blendTwoAttr'), _side + _limbType +  "upper_pin_blend")
        lowerPin = cmds.rename(cmds.createNode('blendTwoAttr'), _side + _limbType +  "lower_pin_blend")

        cmds.connectAttr(nudgeAddition + ".output2Dx", upperPin + ".input[0]")
        cmds.connectAttr(nudgeAddition + ".output2Dy", lowerPin + ".input[0]")

        cmds.connectAttr(upperLength + ".distance", upperPin + ".input[1]")
        cmds.connectAttr(lowerLength + ".distance", lowerPin + ".input[1]")

        cmds.connectAttr(_End_ctrl + "." + _stretchAttributes[2], upperPin + ".attributesBlender")
        cmds.connectAttr(_End_ctrl + "." + _stretchAttributes[2], lowerPin + ".attributesBlender")

        #if right side add a multiplication with -1 to invert the number
        upperIKJointTranslateX = round(cmds.getAttr(_IkJointList[1] + ".translateX"), 3)
        lowerIKJointTranlateX = round(cmds.getAttr(_IkJointList[2] + ".translateX"), 3)

        upperPinOutput = round(cmds.getAttr(upperPin + ".output"), 3)
        lowerPinOutput = round(cmds.getAttr(lowerPin + ".output"), 3)

        #decide if the stretch values need to be inverted or not
        if upperIKJointTranslateX == (upperPinOutput * -1) and lowerIKJointTranlateX == (lowerPinOutput * -1):
             upperInvert = cmds.rename(cmds.createNode('floatMath'), _side + _limbType +  "invert_upper_Pin_Value")
             lowerInvert = cmds.rename(cmds.createNode('floatMath'), _side + _limbType +  "invert_lower_Pin_Value")

             cmds.setAttr(upperInvert + ".operation", 2)
             cmds.setAttr(lowerInvert + ".operation", 2)

             cmds.setAttr(upperInvert + ".floatB", -1)
             cmds.setAttr(lowerInvert + ".floatB", -1)

             cmds.connectAttr(upperPin + ".output", upperInvert + ".floatA")
             cmds.connectAttr(lowerPin + ".output", lowerInvert + ".floatA")

             cmds.connectAttr(upperInvert + ".outFloat", _IkJointList[1] + ".translateX")
             cmds.connectAttr(lowerInvert + ".outFloat", _IkJointList[2] + ".translateX")

        elif upperIKJointTranslateX == upperPinOutput and lowerIKJointTranlateX == lowerPinOutput:
             cmds.connectAttr(upperPin + ".output", _IkJointList[1] + ".translateX")
             cmds.connectAttr(lowerPin + ".output", _IkJointList[2] + ".translateX")
        else: 
             print("Your stretch values do not match up!!")
             return
             

        

        #connect to the actual ik joints

def BuildStretchSetup(_upperJointPos, _midJointPos, _lowerJointPos, _anchor, _poleVector, _endCtrl):

    UserJointsSelection = [_upperJointPos, _midJointPos, _lowerJointPos]

    IKJointList = getUserEntries(UserJointsSelection)

    endCtrl = getUserEntry(_endCtrl)

    anchor = getUserEntry(_anchor)

    poleVector = getUserEntry(_poleVector)

    SideNamingConvention = getCharacterSideNamingConvention(IKJointList)

    print(endCtrl, anchor, poleVector)

    limbType = getLimbType(endCtrl)

    if SideNamingConvention == "Not_Defined" or limbType == "Not_Defined" or anchor == "" or poleVector == "" or endCtrl == "":
        print(SideNamingConvention, limbType, anchor, endCtrl, poleVector)
        print("check youre Naming conventions")
        return
    
    if IKJointList == []:
        print("no Joints Selected")
        return
    
    defaultChain = createDefaultChain(IKJointList)
    GeneralFunctions.reparenting(defaultChain)

    stretchAttributes = ["Stretch_Ctrls", "Do_Stretch", "Pin", "Nudge", "Max_Stretch"]

    addStretchAttributes(endCtrl, stretchAttributes)

    setupConnections(endCtrl, poleVector, anchor, SideNamingConvention, defaultChain, stretchAttributes, limbType, IKJointList)

#=======================================
## Simple Stetch Function - END
#=======================================