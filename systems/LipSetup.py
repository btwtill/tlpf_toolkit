#Module Import
import maya.cmds as cmds
import os
import logging

from tlpf_toolkit import global_variables
from tlpf_toolkit.ctrlShapes import utils
from tlpf_toolkit.utils import GeneralFunctions
from tlpf_toolkit.utils import ZeroOffsetFunction

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


#=======================================
## Sam Lip Setup
#=======================================
#
## TODO Build Automatic Ctrls into the system
#       Add automatic seal and Jaw Follow Attributes to the jaw with attribut blends
#
def SimpleStretchSetupConfigInterface():
    
    #basic Window creation
    configWindow = cmds.window(title="SamLipSetup", iconName='SamLips', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.rowColumnLayout( adjustableColumn=True )
    
    
    cmds.text( label='Inputs', font = "boldLabelFont", height=30)

    headJoint = buildUserInputGrp("Set Head Joint", "Not Defined", 30)

    JawJoint = buildUserInputGrp("Set Jaw Joint", "Not Defined", 30)

    JawCtl = buildUserInputGrp("Set Jaw Ctrl", "Not Defined", 30)

    cmds.button("Build Sam Lip Setup", command=lambda _: BuildSamLipSetup(headJoint, JawJoint))

    #Display The window
    cmds.showWindow(configWindow)

def buildUserInputGrp(buttonLabel, displayLabelText, displayLabelHeight):
    cmds.text(label="", height=10, backgroundColor=[0.0,0.0,0.0])
    cmds.button(label=buttonLabel, height=40, command=lambda _: updateLabel(labelname, getFirstUserSelection()))
    labelname = cmds.text(label=displayLabelText, height=displayLabelHeight, backgroundColor=[0.6, 0.1, 0.1])
    return labelname

def getFirstUserSelection():
    sel = cmds.ls(selection=True)
    return sel[0]

def updateLabel(_label, _newLabelText):
    rgbColor = [0.3, 0.8, 0.2]
    cmds.text(_label, edit=True, label=_newLabelText, backgroundColor=rgbColor)

def getUserEntry(entry):
    return cmds.text(entry, query=True, label=True)


def BuildSamLipSetup(_headJoint, _jawJoint):
    
    headName = getUserEntry(_headJoint)
    jawName = getUserEntry(_jawJoint)

    # work on full selection
    # Select the joints for the lip
    sel = cmds.ls(sl = True)

    for node in sel:
        jntName = node
        print(jntName)

        # Create Nodes
        upTgt = cmds.createNode('transform', n = jntName + '_upFol')
        loTgt = cmds.createNode('transform', n = jntName + '_loFol')
        cn = cmds.createNode('transform', n = jntName + '_cn')
        inv = cmds.createNode('transform', n = jntName + '_inv')
        drv = cmds.createNode('transform', n = jntName + '_drv')
        
        # match to our joint
        cmds.matchTransform(upTgt, jntName)
        cmds.matchTransform(loTgt, jntName)
        cmds.matchTransform(inv, jntName)
        cmds.matchTransform(drv, jntName)
        cmds.matchTransform(cn, jntName)

        # constraint tragets to head / jaw bones
        cmds.parent(upTgt, headName)
        cmds.parent(loTgt, jawName)
        
        # make cn, invert, driven, jnt hierarchy
        cmds.parent(drv, inv)
        cmds.parent(inv, cn)
        
        # get the jnt parent (ZERO NODE?)
        jntParent = cmds.listRelatives(jntName, p = True)[0]
        cmds.parent(cn, jntParent)


        # add jawFollow attr
        cmds.addAttr(jntName, ln = 'jawFollow', at = 'double', min = 0, max = 1, k = True)
        cmds.addAttr(jntName, ln = 'seal', at = 'double', min = 0, max = 1, k = True)
            
        # add constraint
        paCN = cmds.parentConstraint(upTgt, loTgt, cn, mo = False, st = 'none', sr = 'none')[0]
        cmds.setAttr(paCN + ".interpType", 2)
        
        #create the blendnode
        sealB2a = cmds.createNode('blendTwoAttr', n = jntName + '_seal_b2a')
        cmds.setAttr(sealB2a + '.input[1]', 0.5)
        cmds.connectAttr(jntName + '.seal', sealB2a + '.attributesBlender', f = True)
        cmds.connectAttr(jntName + '.jawFollow', sealB2a + '.input[0]', f = True)
        cmds.connectAttr(sealB2a + '.output', paCN + '.target[0].targetWeight', f = True)

        
        # create a reverse node for the other constraint target
        sealRev = cmds.createNode('reverse', n = jntName + '_jawRev')
        cmds.connectAttr(sealB2a + '.output', sealRev + '.inputX', f = True)
        cmds.connectAttr(sealRev + '.outputX', paCN + '.target[1].targetWeight', f = True)

        # parent jnt to drv node
        #cmds.matchTransform(jntName, drv)
        cmds.parent(jntName, drv)
        
        # Right side control will get inverted...
        if jntName.startswith('r_'):
            cmds.setAttr(inv + '.sx', -1)
            cmds.setAttr(inv + '.sy', -1)
            cmds.setAttr(inv + '.sz', -1)

#=======================================
## Sam Lip Setup -END
#=======================================





#=======================================
## Lip Setup Arturo Coso
#=======================================


#global Naming Variables

MID_LIP_POS = os.path.join(global_variables.DATA_LIBRARY_PATH, "Mid_Lip_Pos.json")
CORNER_LIP_POS = os.path.join(global_variables.DATA_LIBRARY_PATH, "Corner_Lip_Pos.json")
UPPER_LEFT_LIP_POS = os.path.join(global_variables.DATA_LIBRARY_PATH, "Upper_left_Lip_Pos.json")
UPPER_RIGHT_LIP_POS = os.path.join(global_variables.DATA_LIBRARY_PATH, "Upper_right_Lip_Pos.json")
LOWER_LEFT_LIP_POS = os.path.join(global_variables.DATA_LIBRARY_PATH, "Lower_left_Lip_Pos.json")
LOWER_RIGHT_LIP_POS = os.path.join(global_variables.DATA_LIBRARY_PATH, "Lower_right_Lip_Pos.json")

GROUP = "grp"
JOINTS = "jnt"
GUIDE = "guide"
JAW = "jaw"
SKIN = "skn"


LEFT = "l"
RIGHT = "r"
CENTER = "cn"

def createArturoCosoLipSetupUI():

    configWindow = cmds.window(title = "ArturoLipSetup", widthHeight=(200, 55), sizeable=True)

    #window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Arturo Coso Lip Setup", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    #Guides Label
    guidesLabel = cmds.text(label="Guides", height = 30, backgroundColor = [.8, .8, .8])

    #Guide amountSlider Label
    guidesLabel = cmds.text(label="0", height = 30, backgroundColor = [.8, .8, .8], align = "center")

    #Guide amountSlider
    guideAmountSlider = cmds.floatSlider(min=0, max=200, value=0, step=1, dragCommand = lambda _: guideAmountSliderUpdate(guidesLabel, guideAmountSlider))

    #create Guides Button
    createGuidesBtn = cmds.button(label="Create Guides", command = lambda _: createGuides(int(cmds.floatSlider(guideAmountSlider, query = True, value = True))))

    #Space Divider
    cmds.text(label="", height=10)

    #def Mid Lip pos
    midLipPosLabel = cmds.text(label = "MidLipPos", height = 30, backgroundColor = [.8, .8, .8])
    midLipPosBtn = cmds.button(label = "Define Mid Lip Pos", command = lambda _: StoreMidLipPos(midLipPosLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #def Corner Lip pos
    cornerLipPosLabel = cmds.text(label = "CornerLipPos", height = 30, backgroundColor = [.8, .8, .8])
    cornerLipPosBtn = cmds.button(label = "Define Corner Lip Pos", command = lambda _: StoreCornerLipPos(cornerLipPosLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #def UpperRight Lip pos
    upperRightLipPosLabel = cmds.text(label = "UpperRightLipPos", height = 30, backgroundColor = [.8, .8, .8])
    upperRightLipPosBtn = cmds.button(label = "Define Upper Right Lip Pos", command = lambda _: StoreUpperRightLipPos(upperRightLipPosLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #def upperLeft Lip pos
    upperLeftLipPosLabel = cmds.text(label = "UpperLeftLipPos", height = 30, backgroundColor = [.8, .8, .8])
    upperLeftLipPosBtn = cmds.button(label = "Define Upper Left Lip Pos", command = lambda _: StoreUpperLeftLipPos(upperLeftLipPosLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #def lowerRight Lip pos
    lowerRightLipPosLabel = cmds.text(label = "LowerRightLipPos", height = 30, backgroundColor = [.8, .8, .8])
    lowerRightLipPosBtn = cmds.button(label = "Define Lower Right Lip Pos", command = lambda _: StoreLowerRightLipPos(lowerRightLipPosLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #def lowerLeft Lip pos
    lowerLeftLipPosLabel = cmds.text(label = "LowerLeftLipPos", height = 30, backgroundColor = [.8, .8, .8])
    lowerLeftLipPosBtn = cmds.button(label = "Define Lower Left Lip Pos", command = lambda _: StoreLowerLeftLipPos(lowerLeftLipPosLabel))

    #Space Divider
    cmds.text(label="", height=10)

    #create Guides Button
    createGuidesFromVerteciesBtn = cmds.button(label="Create Guides", command = lambda _: createGuidesFromVertecies())

    #Space Divider
    cmds.text(label="", height=10)

    #Setup Label
    setupLabel = cmds.text(label="Setup", height = 30, backgroundColor = [.8, .8, .8])

    createSetupBtn = cmds.button(label="Create Lip Setup", command = lambda _: buildArturoCosoLipSetup())

    cmds.showWindow(configWindow)

def StoreMidLipPos(midlipPosLabel):
    #remove file if already existing
    try:
        os.remove(MID_LIP_POS)
    except:
        pass
    
    # get user selection
    midLipPos = cmds.ls(os=True, flatten=True)

    #store user Data as json
    utils.save_data(MID_LIP_POS, midLipPos)

    #update label
    cmds.text(midlipPosLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def StoreCornerLipPos(cornerLipPosLabel):
    #remove file if already existing
    try:
        os.remove(CORNER_LIP_POS)
    except:
        pass
    
    # get user selection
    cornerLipPos = cmds.ls(os=True, flatten=True)

    #store user Data as json
    utils.save_data(CORNER_LIP_POS, cornerLipPos)

    #update label
    cmds.text(cornerLipPosLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def StoreUpperLeftLipPos(upperLeftLipPosLabel):
    #remove file if already existing
    try:
        os.remove(UPPER_LEFT_LIP_POS)
    except:
        pass
    
    # get user selection
    upperLeftLipPos = cmds.ls(os=True, flatten=True)

    #store user Data as json
    utils.save_data(UPPER_LEFT_LIP_POS, upperLeftLipPos)

    #update label
    cmds.text(upperLeftLipPosLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def StoreUpperRightLipPos(upperRightLipPosLabel):
    #remove file if already existing
    try:
        os.remove(UPPER_RIGHT_LIP_POS)
    except:
        pass
    
    # get user selection
    upperRightLipPos = cmds.ls(os=True, flatten=True)

    #store user Data as json
    utils.save_data(UPPER_RIGHT_LIP_POS, upperRightLipPos)

    #update label
    cmds.text(upperRightLipPosLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def StoreLowerLeftLipPos(lowerLeftLipPosLabel):
    #remove file if already existing
    try:
        os.remove(LOWER_LEFT_LIP_POS)
    except:
        pass
    
    # get user selection
    lowerLeftLipPos = cmds.ls(os=True, flatten=True)

    #store user Data as json
    utils.save_data(LOWER_LEFT_LIP_POS, lowerLeftLipPos)

    #update label
    cmds.text(lowerLeftLipPosLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def StoreLowerRightLipPos(lowerRightLipPosLabel):
    #remove file if already existing
    try:
        os.remove(LOWER_RIGHT_LIP_POS)
    except:
        pass
    
    # get user selection
    lowerRightLipPos = cmds.ls(os=True, flatten=True)

    #store user Data as json
    utils.save_data(LOWER_RIGHT_LIP_POS, lowerRightLipPos)

    #update label
    cmds.text(lowerRightLipPosLabel, edit=True, label="Stored", backgroundColor = [0, .8, 0])

def FetchLipVerteciePos():
     
    try:
        midLipPos = utils.load_data(MID_LIP_POS)
    except:
        raise log.error("No MidLipPositions Found!!")
    
    try:
        CornerLipPos = utils.load_data(CORNER_LIP_POS)
    except:
        raise log.error("No Corner Lip Posistions Found!!")

    try:
        upperLeftLipPos = utils.load_data(UPPER_LEFT_LIP_POS)
    except:
        raise log.error("No Upper Left Lip Positions Found")
    
    try:
        upperRightLipPos = utils.load_data(UPPER_RIGHT_LIP_POS)
    except:
        raise log.error("No Upper Right Lip Pos Found!!")
    
    try:
        lowerLeftLipPos = utils.load_data(LOWER_LEFT_LIP_POS)
    except:
        raise log.error("No Lower Left Lip Pos Found!!")
    
    try:
        lowerRightLipPos = utils.load_data(LOWER_RIGHT_LIP_POS)
    except:
        raise log.error("No Lower Right Lip Pos Found!!")

    #remove the tmp files in the tmpData File directory
    os.remove(MID_LIP_POS)
    os.remove(CORNER_LIP_POS)
    os.remove(UPPER_LEFT_LIP_POS)
    os.remove(UPPER_RIGHT_LIP_POS)
    os.remove(LOWER_LEFT_LIP_POS)
    os.remove(LOWER_RIGHT_LIP_POS)

    #append all Positions to one List
    allPos = midLipPos + CornerLipPos + upperLeftLipPos + upperRightLipPos + lowerLeftLipPos + lowerRightLipPos
    log.info(f"{allPos}")

    return midLipPos, CornerLipPos, upperLeftLipPos, upperRightLipPos, lowerLeftLipPos, lowerRightLipPos

#create Guides based on Selected Vertecies
def createGuidesFromVertecies():

    midLipPos, CornerLipPos, upperLeftLipPos, upperRightLipPos, lowerLeftLipPos, lowerRightLipPos = FetchLipVerteciePos()

    midLipLoc = GeneralFunctions.convertVerteciePositionsToLacators(midLipPos)
    CornerLipLoc = GeneralFunctions.convertVerteciePositionsToLacators(CornerLipPos)
    upperLeftLipLoc = GeneralFunctions.convertVerteciePositionsToLacators(upperLeftLipPos)
    upperRightLipLoc = GeneralFunctions.convertVerteciePositionsToLacators(upperRightLipPos)
    lowerLeftLipLoc = GeneralFunctions.convertVerteciePositionsToLacators(lowerLeftLipPos)
    lowerRightLipLoc = GeneralFunctions.convertVerteciePositionsToLacators(lowerRightLipPos)

    #Rename Locators 
    midLipLoc[0] = cmds.rename(midLipLoc[0], f"{CENTER}_{JAW}_Upperlip_{GUIDE}")
    midLipLoc[1] = cmds.rename(midLipLoc[1], f"{CENTER}_{JAW}_Lowerlip_{GUIDE}")

    CornerLipLoc[0] = cmds.rename(CornerLipLoc[0], f"{RIGHT}_{JAW}Corner_lip_{GUIDE}")
    CornerLipLoc[1] = cmds.rename(CornerLipLoc[1], f"{LEFT}_{JAW}Corner_lip_{GUIDE}")

    for i in range(len(upperLeftLipLoc)):
        upperLeftLipLoc[i] = cmds.rename(upperLeftLipLoc[i], f"l_{JAW}_lipUpper_{i+1}_{GUIDE}")

    for i in range(len(upperRightLipLoc)):
        upperRightLipLoc[i] = cmds.rename(upperRightLipLoc[i], f"r_{JAW}_lipUpper_{i+1}_{GUIDE}")

    for i in range(len(lowerLeftLipLoc)):
        lowerLeftLipLoc[i] = cmds.rename(lowerLeftLipLoc[i], f"l_{JAW}_lipLower_{i+1}_{GUIDE}")
    
    for i in range(len(lowerRightLipLoc)):
        lowerRightLipLoc[i] = cmds.rename(lowerRightLipLoc[i], f"r_{JAW}_lipLower_{i+1}_{GUIDE}")

    #arrange Full Lip Locator List Ordered
    lipLocators = list()

    lipLocators.append(midLipLoc[0])
    lipLocators.extend(upperLeftLipLoc)
    lipLocators.extend(upperRightLipLoc)
    lipLocators.append(midLipLoc[1])
    lipLocators.extend(lowerLeftLipLoc)
    lipLocators.extend(lowerRightLipLoc)
    lipLocators.append(CornerLipLoc[1])
    lipLocators.append(CornerLipLoc[0])

    log.info(f"List of the all Lip Locators ordere for further Processing: {lipLocators}")

    #create Structure groups to organize the Guides

    #main Guide Group
    jawGuideGrp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_{GUIDE}_{GROUP}")
    locsGrp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_Locator_{GUIDE}_{GROUP}", parent = jawGuideGrp)

    #main grp Containing Locators
    lipLocGrp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_lip_{GUIDE}_{GROUP}", parent = locsGrp)

    cmds.parent(lipLocators, lipLocGrp)

def guideAmountSliderUpdate(sliderLabel, slider):
    cmds.text(sliderLabel, edit = True, label = str(int(cmds.floatSlider(slider, query = True, value = True))))

#jaw Build Function
def buildArturoCosoLipSetup():

    createLipJointHirarchy()
    createLipSkinJoints()
    createMechanismJoints()
    createJawBaseJoints()
    constraintMechanismJoints()

    log.info(f"Lookup Dictionary: {getLipParts()}")
    log.info(f"Upper Lip Part: {lipPart('Upper')}")
    log.info(f"Lower Lip Part: {lipPart('Lower')}")

    createSealTransforms("Upper")
    createSealTransforms("Lower")

    createJawAttr()
    createSkinJointConstraints()
    createInitalValues("Upper", 1.3)
    createInitalValues("Lower", 1.3)

    connectSearAttr("Upper")
    connectSearAttr("Lower")


#Function to create Guides based on an Input number
def createGuides(number = 5):

    #create Structure groups to organize the Guides

    #main Guide Group
    jawGuideGrp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_{GUIDE}_{GROUP}")
    locsGrp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_Locator_{GUIDE}_{GROUP}", parent = jawGuideGrp)

    #main grp Containing Locators
    lipLocGrp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_lip_{GUIDE}_{GROUP}", parent = locsGrp)

    #split guideCreation into Upper and Lower
    for part in ["upper", "lower"]:

        #get directional vector indication if current locator is upper or lower for y axies offset
        partNum = 1 if part == "upper" else -1

        #create vector with y axis offset Values
        midData = (0, partNum, 0)

        #create locator positioned at the center of the lips
        midLoc = cmds.spaceLocator(name = f"{CENTER}_{JAW}_{part}lip_{GUIDE}")[0]

        #parent the locator to the lips locator grp
        cmds.parent(midLoc, lipLocGrp)

        #split Locator creation into left and right side
        for side in [LEFT, RIGHT]:
            for i in range(number):

                #get offset value depending on the side the locator
                multiplier = i+1 if side == LEFT else -(i+1)
                locData = (multiplier, partNum, 0)

                #create the locator
                loc = cmds.spaceLocator(name = f"{side}_{JAW}_lip{part}_{i+1}_{GUIDE}")[0]

                #parent it under the lip locator grp
                cmds.parent(loc, lipLocGrp)

                #apply the offset value to the locators translate values
                cmds.setAttr(f"{loc}.translate", *locData)

        #apply the offset value to the mid locator translate values
        cmds.setAttr(f"{midLoc}.translate", *midData)

    #create Left and Right Corner Locators of the lips
    leftCornerLoc = cmds.spaceLocator(name= f"{LEFT}_{JAW}Corner_lip_{GUIDE}")[0]
    rightCornerLoc = cmds.spaceLocator(name= f"{RIGHT}_{JAW}Corner_lip_{GUIDE}")[0]

    #parent both to the lip locator Grp
    cmds.parent(leftCornerLoc, lipLocGrp)
    cmds.parent(rightCornerLoc, lipLocGrp)

    #apply the translate offset to the locators
    cmds.setAttr(f"{leftCornerLoc}.translate", *(number+1, 0, 0))
    cmds.setAttr(f"{rightCornerLoc}.translate", *(-( number + 1), 0, 0))

    #clear selection
    cmds.select(clear = True)

    #create group to hold the jaw and inverse jaw Locators
    jawBaseGuideGrp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_base_{GUIDE}_{GROUP}", parent = jawGuideGrp)

    #create Jaw and inverse Jaw
    jawGuide = cmds.spaceLocator(name= f"{CENTER}_{JAW}_{GUIDE}")[0]
    inverseJawGuide = cmds.spaceLocator(name= f"{CENTER}_{JAW}_inverse_{GUIDE}")[0]

    #set Offset Values to translate values of the Locators
    cmds.setAttr(f"{jawGuide}.translate",  *(0, -1, -number))
    cmds.setAttr(f"{inverseJawGuide}.translate",  *(0, 1, -number))

    #parent Locators to the base grp
    cmds.parent(jawGuide, jawBaseGuideGrp)
    cmds.parent(inverseJawGuide, jawBaseGuideGrp)

    #clear selection
    cmds.select(clear = True)


    print(get_lip_guides())
    print(get_jaw_guides())

#function to return the Lip Locator guides
def get_lip_guides():

    grp = f"{CENTER}_{JAW}_lip_{GUIDE}_{GROUP}"

    return [loc for loc in cmds.listRelatives(grp) if cmds.objExists(grp)]

#functino to return the Jaw Locator Guides
def get_jaw_guides():

    grp = f"{CENTER}_{JAW}_base_{GUIDE}_{GROUP}"

    return [loc for loc in cmds.listRelatives(grp) if cmds.objExists(grp)]

#functino to set up the Hirarchy for the Joints
def createLipJointHirarchy():
    #Main Group
    mainGrp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_rig_{GROUP}")

    #lip Grp holding all items regaring the lips
    lipGrp = cmds.createNode("transform", name= f"{CENTER}_{JAW}lip_{GROUP}", parent = mainGrp)

    #base joints Grp
    baseGrp = cmds.createNode("transform", name = f"{CENTER}_{JAW}Base_{GROUP}", parent = mainGrp)

    #create lip SkinJoints Grp
    lipSkinGrp = cmds.createNode("transform", name= f"{CENTER}_{JAW}lipSkinJnt_{GROUP}", parent = lipGrp)

    #create lip MechanismJoints Grp
    lipMchGrp = cmds.createNode("transform", name= f"{CENTER}_{JAW}lipMchJnt_{GROUP}", parent = lipGrp)

    #clear selection
    cmds.select(clear = True)

#create skn Joints
def createLipSkinJoints():

    #list to store created Joints
    skinJoints = list()

    #loop over lip Guides 
    for guide in get_lip_guides():

        #get Guide position
        guideMatrix = cmds.xform(guide, query = True, matrix = True, worldSpace = True)

        #create Joint
        newLipJoint = cmds.joint(name = guide.replace(GUIDE, SKIN))

        #reduce Joint Radius for Visual aid
        cmds.setAttr( f"{newLipJoint}.radius", 0.5)

        #set Joint Worldspace Position Matrix
        cmds.xform(newLipJoint, matrix = guideMatrix, worldSpace = True)

        #parent The joints
        cmds.parent(newLipJoint, f"{CENTER}_{JAW}lipSkinJnt_{GROUP}")

#create Mechanism Joints
def createMechanismJoints():

    #create Joints
    upperJnt = cmds.joint(name=f"{CENTER}_{JAW}_mchUpper_{JOINTS}")
    cmds.select(clear=True)
    lowerJnt = cmds.joint(name=f"{CENTER}_{JAW}_mchLower_{JOINTS}")
    cmds.select(clear=True)
    leftJnt = cmds.joint(name=f"{LEFT}_{JAW}_mchCorner_{JOINTS}")
    cmds.select(clear=True)
    rightJnt = cmds.joint(name=f"{RIGHT}_{JAW}_mchCorner_{JOINTS}")

    #parent Joints into hirarchy
    cmds.parent([upperJnt, lowerJnt, leftJnt, rightJnt], f"{CENTER}_{JAW}lipMchJnt_{GROUP}")

    #get Guide Positions
    upperPos = cmds.xform(f"{CENTER}_{JAW}_Upperlip_{GUIDE}", q=True, ws=True, m=True)
    lowerPos = cmds.xform(f"{CENTER}_{JAW}_Lowerlip_{GUIDE}", q=True, ws=True, m=True)
    leftPos = cmds.xform(f"{LEFT}_{JAW}Corner_lip_{GUIDE}", q=True, ws=True, m=True)
    rightPos = cmds.xform(f"{RIGHT}_{JAW}Corner_lip_{GUIDE}", q=True, ws=True, m=True)

    #set Joint Positions
    cmds.xform(upperJnt, m=upperPos)
    cmds.xform(lowerJnt, m=lowerPos)
    cmds.xform(leftJnt, m=leftPos)
    cmds.xform(rightJnt, m=rightPos)

    cmds.select(clear=True)

#create Jaw Joints
def createJawBaseJoints():
    #create Joints
    jawJnt = cmds.joint(name=f"{CENTER}_{JAW}_{SKIN}")
    cmds.select(clear=True)
    jawInvJnt = cmds.joint(name=f"{CENTER}_{JAW}Inverse_{JOINTS}")
    cmds.select(clear=True)

    #get Matrix Pos
    jawMtrx = cmds.xform(get_jaw_guides()[0], q=True, ws=True, m=True)
    jawInverseMtrx = cmds.xform(get_jaw_guides()[1], q=True, ws=True, m=True)

    #set Matrix Pos
    cmds.xform(jawJnt, m=jawMtrx)
    cmds.xform(jawInvJnt, m=jawInverseMtrx)

    #parent Joints to Hirarchy
    cmds.parent([jawJnt, jawInvJnt], f"{CENTER}_{JAW}Base_{GROUP}")

    #create offset for Base Joints
    cmds.select(clear=True)
    cmds.select(cmds.listRelatives(f"{CENTER}_{JAW}Base_{GROUP}"))
    ZeroOffsetFunction.insertNodeBefore(sfx = "_AUTO")
    cmds.select(clear=True)

    #create AUTO OFFset for Base Joints
    cmds.select(clear=True)
    cmds.select(cmds.listRelatives(f"{CENTER}_{JAW}Base_{GROUP}"))
    ZeroOffsetFunction.insertNodeBefore(sfx = "_OFF")
    cmds.select(clear=True)

#Create Constraints for MechanismJoints
def constraintMechanismJoints():

    #get Base joints and Mechanism Joints
    jawJnt = f"{CENTER}_{JAW}_{SKIN}"
    jawInvJnt = f"{CENTER}_{JAW}Inverse_{JOINTS}"

    mchUpperJnt = f"{CENTER}_{JAW}_mchUpper_{JOINTS}"
    mchLowerJnt = f"{CENTER}_{JAW}_mchLower_{JOINTS}"
    mchLeftJnt = f"{LEFT}_{JAW}_mchCorner_{JOINTS}"
    mchRightJnt = f"{RIGHT}_{JAW}_mchCorner_{JOINTS}"

    #create Offset Nodes
    cmds.select(clear=True)
    cmds.select(mchUpperJnt)
    mchUpperJntOffset = ZeroOffsetFunction.insertNodeBefore()

    cmds.select(clear=True)
    cmds.select(mchLowerJnt)
    mchLowerJntOffset = ZeroOffsetFunction.insertNodeBefore()

    cmds.select(clear=True)
    cmds.select(mchLeftJnt)
    mchLeftJntOffset = ZeroOffsetFunction.insertNodeBefore()

    cmds.select(clear=True)
    cmds.select(mchRightJnt)
    mchRightJntOffset = ZeroOffsetFunction.insertNodeBefore()

    cmds.select(clear=True)

    #create Constraints
    cmds.parentConstraint(jawJnt, mchLowerJntOffset, mo=True)
    cmds.parentConstraint(jawInvJnt, mchUpperJntOffset, mo=True)

    cmds.parentConstraint(mchUpperJntOffset, mchLowerJntOffset, mchRightJntOffset, mo=True)
    cmds.parentConstraint(mchUpperJntOffset, mchLowerJntOffset, mchLeftJntOffset, mo=True)

    cmds.select(clear=True)

#get Lookup Dictionary of the Lip Parts and relations
def getLipParts():

    #define nameing Tokens
    upperToken = "Upper"
    lowerToken = "Lower"
    cornerToken = "Corner"

    #get Mechanism Joints
    mchUpperJnt = f"{CENTER}_{JAW}_mchUpper_{JOINTS}"
    mchLowerJnt = f"{CENTER}_{JAW}_mchLower_{JOINTS}"
    mchLeftJnt = f"{LEFT}_{JAW}_mchCorner_{JOINTS}"
    mchRightJnt = f"{RIGHT}_{JAW}_mchCorner_{JOINTS}"

    lipJnts = cmds.listRelatives(f"{CENTER}_{JAW}lipSkinJnt_{GROUP}", allDescendents=True)

    lookup = {'C_Upper': {}, 'C_Lower': {},
              'L_Upper': {}, 'L_Lower': {},
              'R_Upper': {}, 'R_Lower': {},
              'L_Corner': {}, 'R_Corner': {}}
    
    #sort joints into lookup dictionary
    for jnt in lipJnts:

        if cmds.objectType(jnt) != "joint":
            continue


        if jnt.startswith(CENTER) and upperToken in jnt:
            lookup['C_Upper'][jnt] = [mchUpperJnt]
        
        if jnt.startswith(CENTER) and lowerToken in jnt:
            lookup['C_Lower'][jnt] = [mchLowerJnt]

        if jnt.startswith(LEFT) and upperToken in jnt:
            lookup['L_Upper'][jnt] = [mchUpperJnt, mchLeftJnt]

        if jnt.startswith(LEFT) and lowerToken in jnt:
            lookup['L_Lower'][jnt] = [mchLowerJnt, mchLeftJnt]

        if jnt.startswith(RIGHT) and upperToken in jnt:
            lookup['R_Upper'][jnt] = [mchUpperJnt, mchRightJnt]

        if jnt.startswith(RIGHT) and lowerToken in jnt:
            lookup['R_Lower'][jnt] = [mchLowerJnt, mchRightJnt]

        if jnt.startswith(LEFT) and cornerToken in jnt:
            lookup['L_Corner'][jnt] = [mchLeftJnt]

        if jnt.startswith(RIGHT) and cornerToken in jnt:
            lookup['R_Corner'][jnt] = [mchRightJnt]

    return lookup

#get individual Lip Parts
def lipPart(part):

    #filter the Dictionary for the given part of the lip
    lipParts = [reversed(getLipParts()[f"L_{part}"].keys()), getLipParts()[f"C_{part}"].keys(), getLipParts()[f"R_{part}"].keys()]

    return [jnt for jnt in lipParts for jnt in jnt]

#create all seal Transform Objects
def createSealTransforms(part):

    #create parent grp for seal Transforms
    sealGrpName = f"{CENTER}_seal_{GROUP}"

    #check if parent grp exists and Create on if not
    sealParent = sealGrpName if cmds.objExists(sealGrpName) else cmds.createNode("transform", name = sealGrpName, parent= f"{CENTER}_{JAW}_rig_{GROUP}")
    partGrp = cmds.createNode("transform", name = sealGrpName.replace("seal", f"seal_{part}"), parent = sealParent)

    l_corner = f"{LEFT}_{JAW}_mchCorner_{JOINTS}"
    r_corner = f"{RIGHT}_{JAW}_mchCorner_{JOINTS}"

    #amount of joint in a lip Part
    jntAmount = len(lipPart(part))

    #create Trnafroms and Constrain them
    for index, jnt  in enumerate(lipPart(part)):
        node = cmds.createNode("transform", name = jnt.replace(SKIN, f"{part}_SEAL"), parent = partGrp)
        mtrx = cmds.xform(jnt, q=True, ws=True, m=True)
        cmds.xform(node, m=mtrx, ws=True)

        constraint = cmds.parentConstraint(l_corner, r_corner, node, mo=True)[0]
        cmds.setAttr(f"{constraint}.interpType", 2)

        rCornerValue = float(index) / float(jntAmount - 1)

        lCornerValue = 1 - rCornerValue

        lCornerAttr= f"{constraint}.{l_corner}W0"
        rCornerAttr = f"{constraint}.{r_corner}W1"

        cmds.setAttr(lCornerAttr, lCornerValue)
        cmds.setAttr(rCornerAttr, rCornerValue)

        cmds.select(clear=True)

#create Jaw Attribute Transfrom node and Attributes
def createJawAttr():

    #create transform node to hold the Attributes for the lip weights
    node = cmds.createNode("transform", name ="jaw_attributes", parent = f"{CENTER}_{JAW}_rig_{GROUP}")
    log.info(f"Debug: {list(getLipParts()['C_Upper'].keys())[0]}")

    #add the Upper attribute
    cmds.addAttr(node, ln=list(getLipParts()['C_Upper'].keys())[0], min = 0, max = 1, dv = 0)
    cmds.setAttr(f"{node}.{list(getLipParts()['C_Upper'].keys())[0]}",  lock = 1)

    #add all upper lip joint attributes
    for upper in getLipParts()['L_Upper'].keys():
        cmds.addAttr(node, ln= upper, min=0, max = 1, dv = 0)

    #add Corner lip joint attributes
    cmds.addAttr(node, ln = list(getLipParts()['L_Corner'].keys())[0], min = 0, max = 1, dv = 0)
    cmds.setAttr(f"{node}.{list(getLipParts()['L_Corner'].keys())[0]}",  lock = 1)

    #add Lower Lip joint attributes
    for lower in list(getLipParts()['L_Lower'].keys())[::-1]:
        cmds.addAttr(node, ln= lower, min=0, max = 1, dv = 0)

    #add Center lower lip joint attributes
    cmds.addAttr(node, ln=list(getLipParts()['C_Lower'].keys())[0], min = 0, max = 1, dv = 0)
    cmds.setAttr(f"{node}.{list(getLipParts()['C_Lower'].keys())[0]}", lock = 1)

    createJawOffsetFollowAttr()
    addSealAttrs()

#create all the constraint to the skinned joints
def createSkinJointConstraints():

    #get the relation from the lookup Dictionary
    for value in getLipParts().values():
        for lipJnt, mchJnt in value.items():

            #define for current lipjnt if upper or lower to receive the right seal tranfrom for constraint
            sealToken = "Upper_SEAL" if "Upper" in lipJnt else "Lower_SEAL"
            lipSeal = lipJnt.replace(SKIN, sealToken)

            log.info(f"All the lip seals: {lipSeal}")
            
            #if the lip seal could not be defined the current joint is a center joint and will be constraint only to the upper and lower mch jnt
            if not cmds.objExists(lipSeal):
                const = cmds.parentConstraint(mchJnt, lipJnt, mo=True)[0]
                cmds.setAttr(f"{const}.interpType", 2)
                continue
            
            #create the constraint between the mch joints plus lip seal transform to the skinjoint
            const = cmds.parentConstraint(mchJnt, lipSeal, lipJnt, mo=True)[0]
            cmds.setAttr(f"{const}.interpType", 2)

            #when the skinjoint is only associated with one mch joint it is a corner or mid joint and will only get one reverse node to invert the follow attr value
            if len(mchJnt) == 1:
                sealAttr = f"{const}.{lipSeal}W1"
                rev = cmds.createNode('reverse', name = lipJnt.replace(SKIN, "Rev"))
                cmds.connectAttr(sealAttr, f"{rev}.inputX")
                cmds.connectAttr(f"{rev}.outputX", f"{const}.{mchJnt[0]}W0")
                cmds.setAttr(sealAttr, 0)

            #for skinjoints between 2 mch joints the seal attribute multiplies the reversed follow attr value to create the seal effect
            if len(mchJnt) == 2:
                sealAttr = f"{const}.{lipSeal}W2"
                cmds.setAttr(sealAttr, 0)

                sealRev = cmds.createNode('reverse', name = lipJnt.replace(SKIN, "seal_Rev"))
                jawAttrRev = cmds.createNode("reverse", name = lipJnt.replace(SKIN, "jawAttr_Rev"))
                sealMult = cmds.createNode("multiplyDivide", name = lipJnt.replace(SKIN, "seal_Mult"))

                cmds.connectAttr(sealAttr, f"{sealRev}.inputX")
                cmds.connectAttr(f"{sealRev}.outputX", f"{sealMult}.input2X")
                cmds.connectAttr(f"{sealRev}.outputX", f"{sealMult}.input2Y")

                cmds.connectAttr(f"jaw_attributes.{lipJnt.replace(lipJnt[0], 'l', 1)}", f"{sealMult}.input1Y")
                cmds.connectAttr(f"jaw_attributes.{lipJnt.replace(lipJnt[0], 'l', 1)}", f"{jawAttrRev}.inputX")
                cmds.connectAttr(f"{jawAttrRev}.outputX", f"{sealMult}.input1X" )

                cmds.connectAttr(f"{sealMult}.outputX", f"{const}.{mchJnt[0]}W0")
                cmds.connectAttr(f"{sealMult}.outputY", f"{const}.{mchJnt[1]}W1")

#create the initial interpolation values for the jaw attribte follow values         
def createInitalValues(part, multiplier = 1.3):

    #get all the jaw attributes on the jaw attribute tranform object 
    jawAttr = [lipAttrName for lipAttrName in lipPart(part) if not lipAttrName.startswith('c') and not lipAttrName.startswith('r')]
    log.info(f"Returned Lip Attributes: {jawAttr}")

    #get Lenght of the lip attribute names stored
    lipAttrLength = len(jawAttr)

    #loop over all the attribues, calculate the interpolation value and set the attribute on the Jaw attribute transform object
    for index, attrName in enumerate(reversed(jawAttr)):
        attr = f"jaw_attributes.{attrName}"

        linearInterpValue = float(index) / float(lipAttrLength - 1)
        divValue = linearInterpValue / multiplier
        finalValue = divValue * divValue

        cmds.setAttr(attr, finalValue)

#create Follow Attributes for Jaw Movement
def createJawOffsetFollowAttr():

    jawAttr = "jaw_attributes"
    jawJnt = f"{CENTER}_{JAW}_{SKIN}"
    jawOff = f"{CENTER}_{JAW}_{SKIN}_AUTO"

    cmds.addAttr(jawAttr, ln="follow_ty", min= -10, max = 10, dv = 0)
    cmds.addAttr(jawAttr, ln="follow_tz", min= -10, max = 10, dv = 0)

    remapY = cmds.createNode("remapValue", name = f"{CENTER}_{JAW}_followY_remap")
    cmds.setAttr(f"{remapY}.inputMax", 10)

    remapZ = cmds.createNode("remapValue", name = f"{CENTER}_{JAW}_followZ_remap")
    cmds.setAttr(f"{remapZ}.inputMax", 10)

    mult_y = cmds.createNode("multDoubleLinear", name = f"{CENTER}_{JAW}_followY_mult")
    cmds.setAttr(f"{mult_y}.input2", -1)
    
    cmds.connectAttr(f"{jawJnt}.rx", f"{remapY}.inputValue")
    cmds.connectAttr(f"{jawJnt}.rx", f"{remapZ}.inputValue")

    cmds.connectAttr(f"{jawAttr}.follow_ty", f"{remapY}.outputMax")
    cmds.connectAttr(f"{jawAttr}.follow_tz", f"{remapZ}.outputMax")
    cmds.connectAttr(f"{mult_y}.output", f"{jawOff}.translateY")

    cmds.connectAttr(f"{remapY}.outValue", f"{mult_y}.input1")
    cmds.connectAttr(f"{remapZ}.outValue", f"{jawOff}.translateZ")

#add seal Attribues on attributes transform
def addSealAttrs():

    jaw_attr = "jaw_attributes"

    cmds.addAttr(jaw_attr, at="double", ln = "L_seal", min = 0, max = 10, dv= 0)
    cmds.addAttr(jaw_attr, at="double", ln = "R_seal", min = 0, max = 10, dv= 0)

    cmds.addAttr(jaw_attr, at="double", ln = "L_sealWeight", min = 0, max = 10, dv= 4)
    cmds.addAttr(jaw_attr, at="double", ln = "R_sealWeight", min = 0, max = 10, dv= 4)

#create the seal interpolation
def connectSearAttr(part):

    sealToken = f"{part}_SEAL"
    jawAttr = "jaw_attributes"

    lipJnts = lipPart(part)
    lipJntsAmount = len(lipJnts)
    sealDriverNode = cmds.createNode("lightInfo", name = f"{CENTER}_{sealToken}_DRV")

    log.info(f"debug: Name of the sealDriverNode: {sealDriverNode}")
    log.info(f"debug: Amount of {part} targets: {lipJntsAmount}")

    trigger = { 'l': list(), 'r': list() }

    for side in "lr":
        #fallOff
        delaySubName = f"{side}_{sealToken}_delay_SUB"
        delaySubNode = cmds.createNode("plusMinusAverage", name = delaySubName)

        log.info(f"debug name: {delaySubName}")

        #set DelaySub Nodes Operation and values, connect jawseal delay attribute to delay sub node
        cmds.setAttr(f"{delaySubNode}.operation", 2)
        cmds.setAttr(f"{delaySubNode}.input1D[0]", 10)
        cmds.connectAttr(f"{jawAttr}.{side.capitalize()}_sealWeight", f"{delaySubNode}.input1D[1]")

        #calc linear interp value
        lerp = 1 / float(lipJntsAmount - 1)
        log.info(f"lerp Value: {lerp}")

        #create DelayDivision node and set its attributes, connect delaySub out to delayDivision
        delayDivName = f"{side}_{sealToken}_delay_DIV"
        delayDivNode = cmds.createNode("multDoubleLinear", name = delayDivName)
        cmds.setAttr(f"{delayDivNode}.input2", lerp)
        cmds.connectAttr(f"{delaySubNode}.output1D", f"{delayDivNode}.input1")

        log.info(f"debug name: {delayDivName}")

        multTrigger = list()
        subTrigger = list()

        trigger[side].append(multTrigger)
        trigger[side].append(subTrigger)

        for index in range(lipJntsAmount):

            indexName = f"jaw{index : 02d}"

            #create delayMultiplication Node and set its attributes and connect divsion node to multiply divide node
            delayMultName = f"{indexName}_{side}_{sealToken}_delay_Mult"
            delayMultNode = cmds.createNode("multDoubleLinear", name=delayMultName)
            cmds.setAttr(f"{delayMultNode}.input1", index)
            cmds.connectAttr(f"{delayDivNode}.output", f"{delayMultNode}.input2")

            log.info(f"debug name: {delayMultName}")

            multTrigger.append(delayMultNode)

            #create delaySubNode and connect the delay mult and jaw attribute to the delay sub node
            delaySubName = f"{indexName}_{side}_{sealToken}_delay_SUB"
            delaySubNode = cmds.createNode("plusMinusAverage", name = delaySubName)
            cmds.connectAttr(f"{delayMultNode}.output", f"{delaySubNode}.input1D[0]")
            cmds.connectAttr(f"{jawAttr}.{side.capitalize()}_sealWeight", f"{delaySubNode}.input1D[1]")

            subTrigger.append(delaySubNode)

    #get Constraints
    constTargets = list()

    for jnt in lipJnts:
        attrs = cmds.listAttr(f"{jnt}_parentConstraint1", ud=True)
        for attr in attrs:
            if "SEAL" in attr:
                constTargets.append(f"{jnt}_parentConstraint1.{attr}")
        
    log.info(f"Target Constraints: {constTargets}")

    for leftIndex, target in enumerate(constTargets):
        rightIndex = lipJntsAmount - leftIndex - 1
        indexName = f"{sealToken}_{leftIndex}"

        lMultTrigger, lSubTrigger = trigger["l"][0][leftIndex], trigger["l"][1][leftIndex]
        rMultTrigger, rSubTrigger = trigger["r"][0][rightIndex], trigger["r"][1][rightIndex]

        #left
        lRemapName = f"l_{sealToken}_{indexName}_Remap"
        lRemapNode = cmds.createNode("remapValue", name = lRemapName)
        cmds.setAttr(f"{lRemapNode}.outputMax", 1)
        cmds.setAttr(f"{lRemapNode}.value[0].value_Interp", 2)

        cmds.connectAttr(f"{lMultTrigger}.output", f"{lRemapNode}.inputMin")
        cmds.connectAttr(f"{lSubTrigger}.output1D", f"{lRemapNode}.inputMax")

        #seal Attribute to input of l remap
        cmds.connectAttr(f"{jawAttr}.L_seal", f"{lRemapNode}.inputValue")

        #right
        rSubName = f"r{sealToken}_offset_{indexName}_Sub"
        rSubNode = cmds.createNode("plusMinusAverage", name= rSubName)
        cmds.setAttr(f"{rSubNode}.operation", 2)
        cmds.setAttr(f"{rSubNode}.input1D[0]", 1)

        cmds.connectAttr(f"{lRemapNode}.outValue", f"{rSubNode}.input1D[1]")

        rRemapName = f"r{sealToken}_{indexName}_Remap"
        rRemapNode = cmds.createNode("remapValue", name = rRemapName)
        cmds.setAttr(f"{rRemapNode}.outputMax", 1)
        cmds.setAttr(f"{rRemapNode}.value[0].value_Interp", 2)
        
        cmds.connectAttr(f"{rMultTrigger}.output", f"{rRemapNode}.inputMin")
        cmds.connectAttr(f"{rSubTrigger}.output1D", f"{rRemapNode}.inputMax")

        #seal Attribute to inpout of r Remap
        cmds.connectAttr(f"{jawAttr}.R_seal", f"{rRemapNode}.inputValue")

        cmds.connectAttr(f"{rSubNode}.output1D", f"{rRemapNode}.outputMax")

        #add Both sides

        plusName = f"{indexName}_Sum"
        plusNode = cmds.createNode("plusMinusAverage", name = plusName)

        log.info(f"{plusName}")
        
        cmds.connectAttr(f"{lRemapNode}.outValue", f"{plusNode}.input1D[0]")
        cmds.connectAttr(f"{rRemapNode}.outValue", f"{plusNode}.input1D[1]")

        clampName = f"{indexName}_clamp"
        clampNode = cmds.createNode("remapValue", name = clampName)

        cmds.connectAttr(f"{plusNode}.output1D", f"{clampNode}.inputValue")

        cmds.addAttr(sealDriverNode, at="double", ln=indexName, min=0, max = 1, dv = 0)
        cmds.connectAttr(f"{clampNode}.outValue", f"{sealDriverNode}.{indexName}")

        cmds.connectAttr(f"{sealDriverNode}.{indexName}", target)

    
#=======================================
## Lip Setup Arturo Coso - END
#=======================================
