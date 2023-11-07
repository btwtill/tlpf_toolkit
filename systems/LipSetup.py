#Module Import
import maya.cmds as cmds


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

GROUP = "grp"
JOINTS = "jnt"
GUIDE = "guide"
JAW = "jaw"

LEFT = "l"
RIGHT = "r"
CENTER = "cn"


def createGuides(number = 5):

    jaw_guide_grp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_{GUIDE}_{GROUP}")

    locs_grp = cmds.createNode("transform", name = f"{CENTER}_{JAW}_{GUIDE}_{GROUP}", parent = jaw_guide_grp)

    lip_loc_grp = cmds.createNode("transform", name = f"{CENTER}_lip_{GUIDE}_{GROUP}", parent = locs_grp)

    for part in ["upper", "lower"]:

        partNum = 1 if part == "upper" else -1

        mid_data = (0, partNum, 0)

        mid_loc = cmds.spaceLocator(name = f"{CENTER}_{JAW}_{part}lip_{GUIDE}")[0]

        cmds.parent(mid_loc, lip_loc_grp)

        for side in [LEFT, RIGHT]:
            for i in range(number):
                multiplier = i+1 if side == LEFT else -(i+1)
                loc_data = (multiplier, partNum, 0)
                loc = cmds.spaceLocator(name = f"{side}_{JAW}_lip{part}_{i+1}")[0]
                cmds.parent(loc, lip_loc_grp)

                cmds.setAttr(f"{loc}.translate", *loc_data)
        
        cmds.setAttr(f"{mid_loc}.translate", *mid_data)

    
        







#=======================================
## Lip Setup Arturo Coso - END
#=======================================
