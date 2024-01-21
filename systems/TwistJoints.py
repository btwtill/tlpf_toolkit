#Modules Import
import maya.cmds as cmds
import logging

from tlpf_toolkit.utils import ZeroOffsetFunction
from tlpf_toolkit.mtrx import MatrixZeroOffset

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

#=======================================
## Twist Joints Function
#=======================================
def twistSetupConfigInterface():
    #create window and store
    configWindow = cmds.window(title="TwistJoints", iconName="TwistJoints", widthHeight=(200, 55), sizeable=True)

    #set layout
    cmds.rowColumnLayout( adjustableColumn=True )

    #create label
    cmds.text(label="Select number of Twist Joints")

    #create visible variable to show how many joints will be created based on user input
    global label
    label = cmds.text(label="0")

    #create slider for twist joint amount selection by user
    slider = cmds.floatSlider(min=0, max=30, value=0, step=1, changeCommand=update_label)

    #Space Divider
    cmds.text(label="", height=10)

    setCustomCtrl = cmds.checkBox(label = "Custom Control Object", value = False, changeCommand = lambda _: toggleButtonState(customCtrlBtn))

    #Space Divider
    cmds.text(label="", height=10)

    customCtrlBtn = cmds.button(label="Set Custom Ctrl", height = 30, command = lambda _: updateButtonToSelection(customCtrlBtn), enable = False)

    #button for executing the function to build the twist joints
    cmds.button(label="Create Twist Joints", command=lambda _:createTwistSetup(cmds.floatSlider(slider, query=True, value=True),
                                                                               cmds.checkBox(setCustomCtrl, query = True, value = True),
                                                                               cmds.button(customCtrlBtn, query = True, label = True)))

    #build and show the window
    cmds.showWindow(configWindow)

def toggleButtonState(button):
    buttonState = cmds.button(button, query = True, enable = True)
    cmds.button(button, edit = True, enable = not buttonState)

def updateButtonToSelection(button):
    cmds.button(button, edit = True, label= cmds.ls(selection=True)[0], backgroundColor = [0, 0.5, 0])

#function to set the new user input into the label of how many twist joints are selected
def update_label(value):
    cmds.text(label, edit=True, label=str(int(value)))

#main function to order the creation of the twist joints
def createTwistSetup(_numberOfJoints, doCustomCtrl, ctrlObject):

    #store user selection number of twist joint in local variable
    numberOfJoints = int(_numberOfJoints)
    
    #get user selected joints
    sel = cmds.ls(selection=True)

    #store selection beginning and end into different variables
    p1 = sel[0]
    p2 = sel[1]

    #store parent name string
    name = "".join(p1)

    if doCustomCtrl:
        twistObj = createCtrls(name, p1, numberOfJoints, ctrlObject)
    else:
        #create the Individual twist joint and store there returned selector list in a variable
        twistObj = createJoints(numberOfJoints, name, p1)

    #create two lists with the different weight values to later drive the constraint nodes weights
    weights01 , weights02 = getWeights(numberOfJoints)

    #create the constraints for each twist joint
    createTwistJointPointConstraints(twistObj, p1, p2, weights01, weights02)

    #parent the twist joint under the Parent joint
    parentTwistJoints(twistObj, p1)

    return twistObj

def createCtrls(_name, _p1, _numberOfJoints, ctrlObject):
    twistCtrls = list()

    for ctrl in range(_numberOfJoints):
        newCtrl = cmds.duplicate(ctrlObject, name = _name + "_Twist_ctrl")[0]

        for channel in "XYZ":
                cmds.setAttr(f"{newCtrl}.translate{channel}", 0)
                cmds.setAttr(f"{newCtrl}.rotate{channel}", 0)
                cmds.setAttr(f"{newCtrl}.scale{channel}", 1)

        cmds.matchTransform(newCtrl, _p1)

        cmds.select(clear=True)
        cmds.select(newCtrl)

        constraintNode = ZeroOffsetFunction.insertNodeBefore(sfx = "_const")[0]

        cmds.select(clear=True)

        twistCtrls.append(constraintNode)

    return twistCtrls

#Function to parent a list of objects to a different given Object
def parentTwistJoints(_twistJoinst, _p1):
    for i in _twistJoinst:
        cmds.parent(i, _p1)

#Function to create the joints to function as twist joints
def createJoints(_numberOfJoints, _name, _p1):
    #return List of the selectors for later use
    twistJoints = []

    #joint creation
    for i in range(_numberOfJoints):
        cmds.select(clear=True)
        newJoint = cmds.rename(cmds.joint(), _name + "_Twist")

        #matching Transforms to parent
        cmds.matchTransform(newJoint, _p1)

        #freezing translations
        cmds.makeIdentity(newJoint, apply=True, rotate=True, translate=True, scale=True)

        #add joints to return List
        twistJoints.append(newJoint)

    #return Joint selector list
    return twistJoints
        
#Function taking a list of object, two parent objects and two weight lists
def createTwistJointPointConstraints(_twistJoints, _p1, _p2, _weights01, _weights02):
    for i in range(len(_twistJoints)):
        #create the constraints
        pointConstraint = cmds.pointConstraint(_p1, _p2, _twistJoints[i])

        #set weights for ech constraint
        cmds.setAttr(pointConstraint[0] + "." + _p1 + "W0", _weights02[i])
        cmds.setAttr(pointConstraint[0] + "." + _p2 + "W1", _weights01[i])

#Function to receive two list 
def getWeights(_numberOfJoints):

    #initilize two lists to store the weights
    weights01 = []
    weights02 = []

    
    for i in range(_numberOfJoints - 1):

        #caluculate the first list of weights
        weight = (i + 1) / (_numberOfJoints - 1)

        #push the weight into its corresponding list
        weights01.append(round(weight, 2))

    #set the last weight to be 0.95
    for i in range(len(weights01)):
        if weights01[i] == 1:
            weights01[i] = 0.95
    #set the lowest weight in the weight list
    weights01.insert(0, 0.05)

    #invert weights and put them into the weights2 list
    for i in weights01:
        weights02.append(round(abs(i - 1),2))
        
    #return both weight lists
    return weights01, weights02
#=======================================
## Twist Joints Function - ENd
#=======================================




#=======================================
## Twist Setup
#=======================================


def DefineTwistAxies(joint):
    if round(cmds.getAttr(joint + ".translateX"), 3) != 0:
        return "X"
    elif round(cmds.getAttr(joint + ".translateY"), 3) != 0:
        return "Y"
    elif round(cmds.getAttr(joint + ".translateZ"), 3) != 0:
        return "Z"
    else:
        return "No Twist"
        

def MatrixForwardTwistSetup():
    pass
    #get selection
    sel = cmds.ls(selection = True)

    #seperate main Joint from twist joint selection
    mainJoint = sel.pop(0)

    #validate selection length
    if len(sel) < 2:
        raise Exception("Not enough Twist joints Selected!!")
    else:
        log.info(f"Number of Twist Joints: {len(sel)}")

    #define Twist Axies through translation value from second twist joints
    twistAxies = DefineTwistAxies(sel[0])

    if twistAxies == "No Twist":
        raise Exception("The Selected Joint and the TwistJoint are in the same Position!!")
    else:
        log.info(f"The Twist Axies is: {twistAxies}")

    #get parent joint of main joint
    parentJoint = cmds.listRelatives(mainJoint, parent=True)[0]

    #create two locators and rename them
    referenceLocator = cmds.spaceLocator(name=mainJoint + "_TwistReferenceLoc")[0]
    followLocator =  cmds.spaceLocator(name = mainJoint + "_TwistFollowLoc")[0]

    #match follow locator to main joint and parent follow to main and reference to parent joint
    cmds.matchTransform(referenceLocator, mainJoint)
    cmds.matchTransform(followLocator, mainJoint)

    referenceLocator = cmds.parent(referenceLocator, parentJoint)
    followLocator = cmds.parent(followLocator, mainJoint)

    #give locators offset grp
    cmds.select(clear=True)
    cmds.select(referenceLocator,  add = True)
    cmds.select(followLocator, add=True)

    ZeroOffsetFunction.insertNodeBefore()
    
    cmds.select(clear=True)

    print(type(referenceLocator), type(followLocator))

    #convert offset grp to mtrx nodes

    cmds.select(referenceLocator)

    MatrixZeroOffset.createMatrixZeroOffset(cmds.ls(selection=True)[0])

    cmds.select(clear=True)

    cmds.select(followLocator)
    MatrixZeroOffset.createMatrixZeroOffset(cmds.ls(selection=True)[0])

    cmds.select(clear=True)

    #create mult matrix node
    multMatrixTwist = cmds.createNode("multMatrix", name=mainJoint + "_TwistmultMtrx")

    #connect follow locator world mtrx to mult matrix 
    log.info(f"{followLocator}, {type(followLocator)}")
    log.info(f"{multMatrixTwist}, {type(multMatrixTwist)}")

    cmds.connectAttr(followLocator[0] + ".worldMatrix[0]", multMatrixTwist + ".matrixIn[0]")

    #connect ref locator inv world matrx to mult matrix
    cmds.connectAttr(referenceLocator[0] + ".worldInverseMatrix[0]", multMatrixTwist + ".matrixIn[1]")
    
    #create decompose Matrix
    decomposeTwistMatrix = cmds.createNode("decomposeMatrix", name=mainJoint + "_dcmTwist")

    #connect mult matrix to decompose matrix
    cmds.connectAttr(multMatrixTwist + ".matrixSum", decomposeTwistMatrix + ".inputMatrix")

    #create quat to euler node
    quatToEulerTwistNode = cmds.createNode("quatToEuler", name=mainJoint + "_qteTwist")

    #connect decompse matrix twist axies und w to quat euler node
    cmds.connectAttr(decomposeTwistMatrix + ".outputQuatW", quatToEulerTwistNode + ".inputQuatW")
    cmds.connectAttr(decomposeTwistMatrix + ".outputQuat" + twistAxies, quatToEulerTwistNode + ".inputQuat" + twistAxies)

    #connect twist axies roation output to first twistjoint
    cmds.connectAttr(quatToEulerTwistNode + ".outputRotate" + twistAxies, sel[0] + ".rotate" + twistAxies)

    #calculate the weight the rotation needs to be multiplied with
    twistWeight = []
    invTwistWeight = []

    for i in range(len(sel) - 1):
        weight = (i + 1) / (len(sel) - 1)
        twistWeight.append(round(weight, 2))

    for i in range(len(twistWeight)):
        invTwistWeight.append(round(abs(twistWeight[i] - 1),2))

    twistWeight.pop()

    firstTwistJoint = sel.pop(0)
    lastTwistJoint = sel.pop()

    multiplyNodes = []

    log.info(f"list of effected Joints: {sel}")
    log.info(f"corresponding Twist Weights: {twistWeight}")
    log.info(f"corresponding inverse Twist Weights: {invTwistWeight}")

    for i in range(len(sel)):

        #create multiplier node
        multNode = cmds.createNode("floatMath", name=sel[i] + "_twistWeightMult")

        multiplyNodes.append(multNode)

        #set multiplier to multiply operation 
        cmds.setAttr(multNode + ".operation", 2)

        #set second float value of multiply node to twist weight value
        cmds.setAttr(multNode + ".floatB", invTwistWeight[i])

        #connect quatToEuler nodes twist rotation output to float value one input of multiplier
        cmds.connectAttr(quatToEulerTwistNode + ".outputRotate" + twistAxies, multNode + ".floatA")

        #connect multiplier node float output to joint twist rotation input
        cmds.connectAttr(multNode + ".outFloat", sel[i] + ".rotate" + twistAxies)

    #rotate the mainJoint by 45 degrees
    cmds.setAttr(mainJoint + ".rotate" + twistAxies, 45)

    #compare the rotation value of the first and the last Twist Joint
    if cmds.getAttr(sel[0] + ".rotate" + twistAxies) > cmds.getAttr(sel[-1] + ".rotate" + twistAxies):
        cmds.setAttr(mainJoint + ".rotate" + twistAxies, 0)
        cmds.disconnectAttr(quatToEulerTwistNode + ".outputRotate" + twistAxies,  firstTwistJoint + ".rotate" + twistAxies)
        cmds.connectAttr(quatToEulerTwistNode + ".outputRotate" + twistAxies, lastTwistJoint + ".rotate" + twistAxies)

        #if the first joint has more rotation then the last switch the order of how the weights are implemented
        for i in range(len(multiplyNodes)):
            cmds.setAttr(multiplyNodes[i] + ".floatB", twistWeight[i])
    else:
        #rotate the main joint back to original position
        cmds.setAttr(mainJoint + ".rotate" + twistAxies, 0)
    



    