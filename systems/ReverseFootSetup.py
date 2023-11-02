#Module Import
import maya.cmds as cmds

import logging
import os
from tlpf_toolkit.utils import ZeroOffsetFunction
from tlpf_toolkit.mtrx import MatrixZeroOffset
from tlpf_toolkit import global_variables
from tlpf_toolkit.ctrlShapes import utils

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

REV_JOINTCHAIN_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "rev_joints.json")

#=======================================
## Reverse Foot Function Setup 01
#=======================================

def BuildReverseFootSetup01(_footCtrl,
                             _footIKH,
                             _reverseJointChain,
                             _footIKJoint, 
                             _ikToeCtrl, 
                             _ikToeJoint,
                             setupName, 
                             _footRollBorderValue = 25):
    #save all inputs to internal variables
    footCtrl = _footCtrl
    footIKH = _footIKH
    reverseJointChain = _reverseJointChain
    footIKJoint = _footIKJoint
    ikToeCtrl = _ikToeCtrl
    ikToeJoint = _ikToeJoint
    footRollBorderValue = _footRollBorderValue

    try:
        bankInGrp = reverseJointChain[0]
        bankOutGrp = reverseJointChain[1]
        revHeelJoint = reverseJointChain[2]
        revBallSwivelJoint = reverseJointChain[3]
        revTipJoint = reverseJointChain[4]
        revBallJoint = reverseJointChain[5]
        revFootJoint = reverseJointChain[6]
    except:
        raise Exception(f"There must be at 7 objects in the Reverse joint chain. Current Length: {len(_reverseJointChain)}")
    
    #find multmatrix node of ikh and save it
    footIKHandleMultMatrix = cmds.listConnections(footIKH, destination=False, source = True, type = "multMatrix")[0]

    #disconnect FootCtrl from IKH Mult Matrix
    ikhMultMatrixInputSocketIndex = 0
    try:
        cmds.disconnectAttr(footCtrl + ".worldMatrix[0]", footIKHandleMultMatrix + ".matrixIn[0]")
        
    except:
        cmds.disconnectAttr(footCtrl + ".worldMatrix[0]", footIKHandleMultMatrix + ".matrixIn[1]")
        ikhMultMatrixInputSocketIndex = 1
        log.info(f"{ikhMultMatrixInputSocketIndex}")

    #connect revFootJoitn from ReverseJointChain world matrix output to ikh multmatrix
    cmds.connectAttr(revFootJoint + ".worldMatrix[0]", footIKHandleMultMatrix + ".matrixIn[" + str(ikhMultMatrixInputSocketIndex) + "]")

    #parent bankInGrp to footCtrl 
    cmds.parent(bankInGrp, footCtrl)

    #give offset node to top level input in reverseJointChain
    cmds.select(clear=True)
    cmds.select(bankInGrp)

    ZeroOffsetFunction.insertNodeBefore()
    
    #convert offset node to offsetParent matrix input
    MatrixZeroOffset.createMatrixZeroOffset(bankInGrp)

    #find constraint between footCtrl and ikFootJoint
    ikfootJointOrientConstraint = cmds.listConnections(footIKJoint, destination =True, source = False, type = "orientConstraint")[0]
    log.info(f"{ikfootJointOrientConstraint}")
    cmds.delete(ikfootJointOrientConstraint)

    #orientConstraint lowest level from ReverseJointChain with ikFootjoint
    cmds.orientConstraint(revFootJoint, footIKJoint)

    #add Foot attribute divider on FootCtrl
    cmds.addAttr(footCtrl, ln="FOOTATTR", at="enum", en="******", keyable=False)
    cmds.setAttr(footCtrl + ".FOOTATTR", cb=True)

    #add Roll Attribue 
    cmds.addAttr(footCtrl, ln = "Foot_Roll", at = "float", keyable = True)

    #add Bank Attribute
    cmds.addAttr(footCtrl, ln = "Foot_Bank", at = "float", keyable = True)

    #add Heel Swivel attribute
    cmds.addAttr(footCtrl, ln = "Heel_Swivel", at = "float", keyable = True)

    #add ballswivel attribute
    cmds.addAttr(footCtrl, ln = "Ball_Swivel", at = "float", keyable = True)

    #add tipswivel attribute
    cmds.addAttr(footCtrl, ln = "Tip_Swivel", at = "float", keyable = True)

    #Foot Roll Mechanism
    #Create main Condition node
    footRollMainCondition = cmds.createNode("condition", name = setupName + "_FootRollCondition")
    log.info(f"{footRollMainCondition}")

    #set Operation to 2 (greater Than)
    cmds.setAttr(footRollMainCondition + ".operation", 2)

    #set Color IF False G value to 0
    cmds.setAttr(footRollMainCondition + ".colorIfFalseG", 0)

    #set Color If False B value to 0
    cmds.setAttr(footRollMainCondition + ".colorIfFalseB", 0)

    #set second Term to footRollBorderValue
    cmds.setAttr(footRollMainCondition + ".secondTerm", footRollBorderValue)

    #connect Roll Value to First Term 
    cmds.connectAttr(footCtrl + ".Foot_Roll", footRollMainCondition + ".firstTerm")

    #connect Roll Value to Color is Fals R
    cmds.connectAttr(footCtrl + ".Foot_Roll", footRollMainCondition + ".colorIfFalseR")

    #create Ball Reverse Plus minus average 
    footRollReversePMA = cmds.createNode("plusMinusAverage", name=setupName + "_FootRollReversePMA")

    #set input ID 0 to FootRollBorder Value
    cmds.setAttr(footRollReversePMA + ".input1D[0]", _footRollBorderValue)

    #connect FootRoll Value to input ID 1
    cmds.connectAttr(footCtrl + ".Foot_Roll", footRollReversePMA + ".input1D[1]")

    #set Operation type to 2 (subtract)
    cmds.setAttr(footRollReversePMA + ".operation", 2)

    #create Foot Roll Subtract Plus minus average node
    footRollSubstractPMA = cmds.createNode("plusMinusAverage", name = setupName + "_footRollSubstactPMA")

    #connect Ball Revers pma to footRollsubtract pma input 1D 1
    cmds.connectAttr(footRollReversePMA + ".output1D", footRollSubstractPMA + ".input1D[1]")

    #set FootRoll subtract pma input 1D 0 to FootRollBorderValue
    cmds.setAttr(footRollSubstractPMA + ".input1D[0]", footRollBorderValue)

    #set FootRoll subtract pma operation type to 1 (sum)
    cmds.setAttr(footRollSubstractPMA + ".operation", 1)

    #connect FootRoll subtract pma Output 1D to Footroll condition Color if True R
    cmds.connectAttr(footRollSubstractPMA + ".output1D", footRollMainCondition + ".colorIfTrueR")

    #create FootRoll Clamp condition node
    footRollClampCondition = cmds.createNode("condition", name = setupName + "_footRollClampCondition")

    #set Opteration to 4 (less than)
    cmds.setAttr(footRollClampCondition + ".operation", 4)

    #connect FootRoll Main Condition outcolor R to clamp condition first term
    cmds.connectAttr(footRollMainCondition + ".outColorR", footRollClampCondition + ".firstTerm")

    #connect FootRollMain Condition outcolor R to clamp condition Color If False R
    cmds.connectAttr(footRollMainCondition + ".outColorR", footRollClampCondition + ".colorIfFalseR")

    #set clamp condtition Color If False G and B to 0
    cmds.setAttr(footRollClampCondition + ".colorIfFalseG", 0)
    cmds.setAttr(footRollClampCondition + ".colorIfFalseB", 0)

    #connect clamp condition outColor R to Reverse Foot JointRotate X
    cmds.connectAttr(footRollClampCondition + ".outColorR", revBallJoint + ".rotateX")

    #create FootRollTipMulti node (Multiply Divide)
    footRollTipMulti = cmds.createNode("multiplyDivide", name=setupName + "_FootRollTipMulti")

    #Set FootRollTipMulti operation type to Multiply (1)
    cmds.setAttr(footRollTipMulti + ".operation", 1)

    #connect FootRoll Reverse node Output 1D to FootRollTipMulti Input 1 X
    cmds.connectAttr(footRollReversePMA + ".output1D", footRollTipMulti + ".input1X")

    #set FootRollTipMulti input 2 X to -1
    cmds.setAttr(footRollTipMulti + ".input2X", -1)

    #connect FootRollTipMulti output X to FootRollMainCondition Color if True G
    cmds.connectAttr(footRollTipMulti + ".outputX", footRollMainCondition + ".colorIfTrueG")

    #connect FootRollMainCondition ColorOutput G to FootReverseTip Rotate X
    cmds.connectAttr(footRollMainCondition + ".outColorG", revTipJoint + ".rotateX")

    #create Heel Condition node 
    heelCondition = cmds.createNode("condition", name=setupName + "_heelCondition")

    #set Heel Condition node Operation to 4 (less than)
    cmds.setAttr(heelCondition + ".operation", 4)

    #set Color IF False RGB to 0
    for r in "RGB":
        cmds.setAttr(heelCondition + ".colorIfFalse" + r, 0)

    #connect FootRoll Value to Heel Condition Color If True R
    cmds.connectAttr(footCtrl + ".Foot_Roll", heelCondition + ".colorIfTrueR")

    #connect FootRoll Value to Heel Condition Term 1
    cmds.connectAttr(footCtrl + ".Foot_Roll", heelCondition + ".firstTerm")

    #connect Heel Condition Output Color R to Foot Rev Heel Rotation X
    cmds.connectAttr(heelCondition + ".outColorR", revHeelJoint + ".rotateX")

    #Banking
    #create Banking Condition Node 
    bankingCondition = cmds.createNode("condition", name=setupName + "_bankingCondition")
    
    #set Color IF False R and B to 0
    cmds.setAttr(bankingCondition + ".colorIfFalseR", 0)
    cmds.setAttr(bankingCondition + ".colorIfFalseB", 0)

    #set Opteration type to 4 (less then)
    cmds.setAttr(bankingCondition + ".operation", 4)

    #connect Foot Bank value to Condition node first Term
    cmds.connectAttr(footCtrl + ".Foot_Bank", bankingCondition + ".firstTerm")

    #connect Foot Bank value to COndition node Color IF True R
    cmds.connectAttr(footCtrl + ".Foot_Bank", bankingCondition + ".colorIfTrueR")

    #connect Foot Bank value to Condition node Color If False G
    cmds.connectAttr(footCtrl + ".Foot_Bank", bankingCondition + ".colorIfFalseG")

    #connect Condition Output R to Bank out grp rotation Z
    cmds.connectAttr(bankingCondition + ".outColorR", bankOutGrp + ".rotateZ")

    #connect Condition Output G to Bank in grp rotation Z
    cmds.connectAttr(bankingCondition + ".outColorG", bankInGrp + ".rotateZ")

    #Swivels
    #connect Heel Swivel Value to Reverse Heel Joint Rotate Y
    cmds.connectAttr(footCtrl + ".Heel_Swivel", revHeelJoint + ".rotateY")

    #connect Ball Swivel Value to Reverse BallSwivel Joint Rotate Y
    cmds.connectAttr(footCtrl + ".Ball_Swivel", revBallSwivelJoint + ".rotateY")

    #create Tip Swivel Reverse node (float Math)
    reverseTipSwivel = cmds.createNode("floatMath", name=setupName + "_revTipSwivel")

    #set TipSwivel Reverse to operation 2 (Multiply)
    cmds.setAttr(reverseTipSwivel + ".operation", 2)

    #set TipSwivel Reverse float B to -1
    cmds.setAttr(reverseTipSwivel + ".floatB", -1)

    #connect TipSwivel value to TipSwivel Reverse float A
    cmds.connectAttr(footCtrl + ".Tip_Swivel", reverseTipSwivel + ".floatA")

    #connect TipSwivelRverse Output Float to Reverse Tip Joint Rotate Y input
    cmds.connectAttr(reverseTipSwivel + ".outFloat", revTipJoint + ".rotateY")

    #Toe Ctrl Rotate Back 
    #disconnect Toe ik ctrl Output Rotate X value from Toe ikjnt rotate X input 
    cmds.disconnectAttr(ikToeCtrl + ".rotateX", ikToeJoint + ".rotateX")

    #create toesFootRollBackRotation plus minus average node 
    toesFootRollRotBack = cmds.createNode("plusMinusAverage", name = setupName + "_rotateToesBack")

    #connect Toe IK ctrl Output Rotate X value to toesFootRollbackrotation pma input 1D 0
    cmds.connectAttr(ikToeCtrl + ".rotateX", toesFootRollRotBack + ".input1D[0]")

    #connect FootRevBall output Rotate X to Toes Foot Roll Backrotation pma Input 1D 1
    cmds.connectAttr(revBallJoint + ".rotateX",  toesFootRollRotBack + ".input1D[1]")

    #connect Toes FootRollBackrotation pma Output 1D to toes ikJoint Input Rotate X
    cmds.connectAttr(toesFootRollRotBack + ".output1D", ikToeJoint + ".rotateX")

    #set PMA Operation to substract
    cmds.setAttr(toesFootRollRotBack + ".operation", 2)

    #group and name ReverseFoot jointChain
    cmds.group(bankInGrp, name=setupName + "rev_grp")


def updateRevFootUILabel(label):
    cmds.text(label, edit=True, label=cmds.ls(selection=True)[0])

def StoreRevChain(revChainLabel):

    #remove file if already existing
    try:
        os.remove(REV_JOINTCHAIN_PATH)
    except:
        pass
    
    # get user selection
    rev_jointChain = cmds.ls(selection = True)

    #store user Data as json
    utils.save_data(REV_JOINTCHAIN_PATH, rev_jointChain)

    #update label
    cmds.text(revChainLabel, edit=True, label="Chain Stored", backgroundColor = [0, .8, 0])

def loadRevFootChain():
    try:
        rev_chain = utils.load_data(REV_JOINTCHAIN_PATH)
    except:
        raise log.error("No joint Selection Found!!")
    
    os.remove(REV_JOINTCHAIN_PATH)

    rev_chain[0] = rev_chain[0].replace("|", "")

    return rev_chain

def revFootSetup01ConfigUI():
    configWindow = cmds.window(title = "RevFootSetup01", widthHeight=(200, 55), sizeable=True)

    #window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Build RevFoot Setup V1", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    #set Base system name
    baseNameLabel = cmds.text(label="Set System BaseName", height = 20, backgroundColor = [.8, .8, .8])

    #basename TextField
    setupName = cmds.textField()

    #Space Divider
    cmds.text(label="", height=10)

    #FootCtrl Input Label
    footCtrlLabel = cmds.text(label="Foot Ctrl", height = 30, backgroundColor = [.8, .8, .8])

    #foot Ctrl Button
    footCtrlButton = cmds.button(label="Store Selection", command = lambda _: updateRevFootUILabel(footCtrlLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #FootIK Handle Input Label
    footIKHLabel = cmds.text(label="FootIKH", height = 30, backgroundColor = [.8, .8, .8])

    footIKHButton = cmds.button(label="Store Selection", command = lambda _: updateRevFootUILabel(footIKHLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #FootIK Handle Input Label
    revJointChainLabel = cmds.text(label="RevJointChain", height = 30, backgroundColor = [.8, .8, .8])

    revJointChainButton = cmds.button(label="Store Chain", command = lambda _: StoreRevChain(revJointChainLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #FootIK Handle Input Label
    footIKJointLabel = cmds.text(label="Foot IK Joint", height = 30, backgroundColor = [.8, .8, .8])

    footIKJointButton = cmds.button(label="Store Selection", command = lambda _: updateRevFootUILabel(footIKJointLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #FootIK Handle Input Label
    toeIKJointLabel = cmds.text(label="Toe IK Joint", height = 30, backgroundColor = [.8, .8, .8])

    toeIKJointButton = cmds.button(label="Store Selection", command = lambda _: updateRevFootUILabel(toeIKJointLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #FootIK Handle Input Label
    toeIKCtrlLabel = cmds.text(label="Toe IK Ctrl", height = 30, backgroundColor = [.8, .8, .8])

    toeIKCtrlButton = cmds.button(label="Store Selection", command = lambda _: updateRevFootUILabel(toeIKCtrlLabel))

    #Build Button
    buildButton = cmds.button(label="Build revFoot Setup V01", command = lambda _: BuildReverseFootSetup01(cmds.text(footCtrlLabel, query = True, label=True),
                                                                                                           cmds.text(footIKHLabel, query = True, label=True),
                                                                                                           loadRevFootChain(),
                                                                                                           cmds.text(footIKJointLabel, query = True, label = True),
                                                                                                           cmds.text(toeIKCtrlLabel, query = True, label = True),
                                                                                                           cmds.text(toeIKJointLabel, query = True, label = True),
                                                                                                           cmds.textField(setupName, query = True, text = True)))

    #display window
    cmds.showWindow(configWindow)
#=======================================
## Reverse Foot Function - END
#=======================================
