#Module import
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


IK_JOINT_SELECTION_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "IKJoints.json")
FK_JOINT_SELECTION_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "FKJoints.json")
TARGET_JOINT_SELECTION_PATH = os.path.join(global_variables.DATA_LIBRARY_PATH, "TargetJoints.json")


#=======================================
## IkFk Switch Function
#=======================================
def IKFKSwitch(doParentJointCreation, _selectionList):
        selectionList = _selectionList
                
        def createIKChain(targetChain):
            cmds.select(targetChain[0], targetChain[len(targetChain) - 1])
            IkHanldeName = "".join(targetChain[len(targetChain) - 1]) + "_IK_Handle"
            cmds.ikHandle(targetChain[0], targetChain[len(targetChain) - 1], name=IkHanldeName)

        def createIKFKSwitch(iKChain, fKChain, targetChain):
            for i in range(len(targetChain)):
                currentBlendNode = cmds.pairBlend(node=targetChain[i], attribute=["tx", "ty", "tz", "rx", "ry", "rz"])
                
                ikNodeTranslationX = iKChain[i] + ".translateX"
                ikNodeTranslationY = iKChain[i] + ".translateY"
                ikNodeTranslationZ = iKChain[i] + ".translateZ"
                
                ikNodeRotationX = iKChain[i] + ".rotateX"
                ikNodeRotationY = iKChain[i] + ".rotateY"
                ikNodeRotationZ = iKChain[i] + ".rotateZ"
                
                fkNodeTranslationX = fKChain[i] + ".translateX"
                fkNodeTranslationY = fKChain[i] + ".translateY"
                fkNodeTranslationZ = fKChain[i] + ".translateZ"
                
                fkNodeRotationX = fKChain[i] + ".rotateX"
                fkNodeRotationY = fKChain[i] + ".rotateY"
                fkNodeRotationZ = fKChain[i] + ".rotateZ"
                
                currentBlendNodeTranslateX1 = currentBlendNode + ".inTranslateX1"
                currentBlendNodeTranslateY1 = currentBlendNode + ".inTranslateY1"
                currentBlendNodeTranslateZ1 = currentBlendNode + ".inTranslateZ1"
                
                currentBlendNodeRotationX1 = currentBlendNode + ".inRotateX1"
                currentBlendNodeRotationY1 = currentBlendNode + ".inRotateY1"
                currentBlendNodeRotationZ1 = currentBlendNode + ".inRotateZ1"
                
                
                currentBlendNodeTranslateX2 = currentBlendNode + ".inTranslateX2"
                currentBlendNodeTranslateY2 = currentBlendNode + ".inTranslateY2"
                currentBlendNodeTranslateZ2 = currentBlendNode + ".inTranslateZ2"
                
                currentBlendNodeRotationX2 = currentBlendNode + ".inRotateX2"
                currentBlendNodeRotationY2 = currentBlendNode + ".inRotateY2"
                currentBlendNodeRotationZ2 = currentBlendNode + ".inRotateZ2"
                
                cmds.connectAttr(ikNodeTranslationX, currentBlendNodeTranslateX1)
                cmds.connectAttr(ikNodeTranslationY, currentBlendNodeTranslateY1)
                cmds.connectAttr(ikNodeTranslationZ, currentBlendNodeTranslateZ1)
                
                cmds.connectAttr(ikNodeRotationX, currentBlendNodeRotationX1)
                cmds.connectAttr(ikNodeRotationY, currentBlendNodeRotationY1)
                cmds.connectAttr(ikNodeRotationZ, currentBlendNodeRotationZ1)
                
                cmds.connectAttr(fkNodeTranslationX, currentBlendNodeTranslateX2)
                cmds.connectAttr(fkNodeTranslationY, currentBlendNodeTranslateY2)
                cmds.connectAttr(fkNodeTranslationZ, currentBlendNodeTranslateZ2)
                
                cmds.connectAttr(fkNodeRotationX, currentBlendNodeRotationX2)
                cmds.connectAttr(fkNodeRotationY, currentBlendNodeRotationY2)
                cmds.connectAttr(fkNodeRotationZ, currentBlendNodeRotationZ2)

##Check if Joints are Selected
        if len(selectionList) >= 2:
            
            ##Create the Chains

            #FK Joints
            fkArray = GeneralFunctions.duplicateSelection(selectionList)
            fkArray = GeneralFunctions.removeOneAndPrefixName(fkArray, "FK_")

            #IK Joints
            ikArray = GeneralFunctions.duplicateSelection(selectionList)
            ikArray = GeneralFunctions.removeOneAndPrefixName(ikArray, "IK_")

            #Reparent the individual Joints into Chains
            GeneralFunctions.reparenting(fkArray)
            GeneralFunctions.reparenting(ikArray)

            #Create IK System
            createIKChain(ikArray)

            #Build the Switch
            createIKFKSwitch(ikArray, fkArray, selectionList)

            if doParentJointCreation:
                CreateANCORParent(selectionList, ikArray, fkArray)
       
        else:
            print("Select Joints")


##Create an IKFK Attribute for switching between ik and fk
def createIKFKAttribute(IKFKattributeName):
    attribute = cmds.spaceLocator()
    cmds.select(attribute)
    addedAttributeName = "".join(cmds.pickWalk(direction="down")) + "." + IKFKattributeName
    cmds.addAttr(longName=IKFKattributeName, minValue=0, maxValue=1, defaultValue=0)
    cmds.setAttr(addedAttributeName, keyable=True)
    cmds.rename("iKfK")


##Create Anchor and Parent Bone for IKFK Chain
def CreateANCORParent(_selectionForAnchor, _ikArray, _fkArray):

    selectionList = _selectionForAnchor

    #selet target Joint
    cmds.select(selectionList[0])
    parentJoint = cmds.pickWalk(direction="up")

    #create list to keep track of the names
    tmpParentingChainList = [parentJoint]

    #duplicate target joint rename it and add it to the list
    targetDuplicate = cmds.duplicate(parentJoint, parentOnly=True)
    targetDuplicateName = "".join(targetDuplicate)
    targetDuplicateName = "IKFK_" + targetDuplicateName.replace("1", "") 
    targetDuplicate = cmds.rename(targetDuplicate, targetDuplicateName)
    tmpParentingChainList.append(targetDuplicateName)

    #unparent it
    cmds.parent(targetDuplicate, world=True)

    #constrain it back to tha target joint
    cmds.parentConstraint(tmpParentingChainList[0], tmpParentingChainList[1])

    #parent the IK FK Chains to the IKFK Parent Joint
    cmds.parent(_ikArray[0], tmpParentingChainList[1])
    cmds.parent(_fkArray[0], tmpParentingChainList[1])

    #store pos for Anchor
    ChainPos = cmds.xform(selectionList[0], query=True, worldSpace=True, translation=True)

    #create, move and parent the Anchor
    Anchor = cmds.spaceLocator(name=selectionList[0] + "_ACNHOR")
    cmds.xform(Anchor, worldSpace=True, translation=ChainPos)
    cmds.parent(Anchor, tmpParentingChainList[0])

##Function to connect an attribute to multiple pair blend Weight attributes  
def ConnectPairBlend(_attribute_name):

    selectionList = cmds.ls(selection=True)
    
    for i in range(len(selectionList)):
        weightOutPut = ""
        if i == 0:
            weightOutput = selectionList[i]
            weightOutput = weightOutput + "." + _attribute_name
        else:
            input = selectionList[i] + ".weight"
            cmds.connectAttr(weightOutput, input)



##build function deciding what will be executed
def BuildSwitch(args, parentJointCreation, attributeShapeCreation, switchCreation):
    
    selectionList = cmds.ls(selection=True)

    if attributeShapeCreation:
        createIKFKAttribute(args)
    if switchCreation:
        IKFKSwitch(parentJointCreation, selectionList)
    
       
#Open Dialogue to Create the IKFK Switch
def IKFKConfigurationInterface():
    
    #basic Window creation
    configWindow = cmds.window(title="IKFKSwitch", iconName='IKFK', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.rowColumnLayout( adjustableColumn=True )
    
    #Label
    cmds.text( label='Attribute_Name' )
    
    #Input Field Sotring the Stirng value
    name = cmds.textField()
    
    #Bool If the Attribute Shape should be created
    doCreateAttributeShape = cmds.checkBox(label="Create Attribute Shape")
    
    #Bool to enable creating the parent joint for the IK FK Switch Joints
    doCreateParentJoint = cmds.checkBox(label="ParnetJoint")
    
    #Bool to create the switch
    doCreateSwitch = cmds.checkBox(label="Create Switch", value=True)
    
    #Building the switch execution button
    cmds.button( label='Build Swtich', command=lambda _: BuildSwitch(cmds.textField(name, query=True, text=True), cmds.checkBox(doCreateParentJoint, query=True, value=True), cmds.checkBox(doCreateAttributeShape, query=True, value=True), cmds.checkBox(doCreateSwitch, query=True, value=True)))
    
    #Input Field to determin which Attribute should be connected to the weight inputs on the pair blend Nodes
    ikfkAttributeName = cmds.textField()

    #execution button to connect the ikfk Attribute with the blend Nodes
    cmds.button( label='ConnectPairBlends', command=lambda _: ConnectPairBlend(cmds.textField(ikfkAttributeName, query=True, text=True)))

    #Display The window
    cmds.showWindow(configWindow)
    
#=======================================
## IkFk Switch Function - END
#=======================================


#=======================================
## IkFk PairBlend Connect Sinlge Joint
#=======================================
#Select First either IK or FK Joint and last the Skinned Joint and run the Script
def CreateSinlgeIKFKBlend():
    sel = cmds.ls(selection=True)

    newPairBlend = cmds.rename(cmds.createNode("pairBlend"), sel[0] +  "_" + sel[1] + "_ikfk_blend")

    for i in "XYZ":
        cmds.connectAttr(sel[0] + ".rotate" + i, newPairBlend + ".inRotate" + i + "1")
        
    for i in "XYZ":
        cmds.connectAttr(sel[0] + ".translate" + i, newPairBlend + ".inTranslate" + i + "1")
        
    for i in "XYZ":
        cmds.connectAttr(sel[1] + ".rotate" + i, newPairBlend + ".inRotate" + i + "2")
        
    for i in "XYZ":
        cmds.connectAttr(sel[1] + ".translate" + i, newPairBlend + ".inTranslate" + i + "2")
        
    for i in "XYZ":
        cmds.connectAttr(newPairBlend + ".outRotate" + i, sel[2] + ".rotate" + i)
        
    for i in "XYZ":
        cmds.connectAttr(newPairBlend + ".outTranslate" + i, sel[2] + ".translate" + i)
#=======================================
## IkFk PairBlend Connect Sinlge Joint - END
#=======================================


#=======================================
## IkFk Multi PairBlend Connect 
#=======================================


def StoreIKJointsSelection(ikJointsLabel):

    #remove file if already existing
    try:
        os.remove(IK_JOINT_SELECTION_PATH)
    except:
        pass
    
    # get user selection
    ikJoints = cmds.ls(selection = True)

    #store user Data as json
    utils.save_data(IK_JOINT_SELECTION_PATH, ikJoints)

    #update label
    cmds.text(ikJointsLabel, edit=True, label="IK Joints Stored", backgroundColor = [0, .8, 0])


def StoreFKJointsSelection(fkJointsLabel):

    #remove file if already existing
    try:
        os.remove(FK_JOINT_SELECTION_PATH)
    except:
        pass
    
    # get user selection
    fkJoints = cmds.ls(selection = True)

    #store user Data as json
    utils.save_data(FK_JOINT_SELECTION_PATH, fkJoints)

    #update label
    cmds.text(fkJointsLabel, edit=True, label="FK Joints Stored", backgroundColor = [0, .8, 0])

def StoreTargetJointsSelection(targetJointsLabel):

    #remove file if already existing
    try:
        os.remove(TARGET_JOINT_SELECTION_PATH)
    except:
        pass
    
    # get user selection
    targetJoints = cmds.ls(selection = True)

    #store user Data as json
    utils.save_data(TARGET_JOINT_SELECTION_PATH, targetJoints)

    #update label
    cmds.text(targetJointsLabel, edit=True, label="Target Joints Stored", backgroundColor = [0, .8, 0])


def CreateSinglePairBlend(ikJoint, fkJoint, targtJoint):

    pairBlend = cmds.createNode("pairBlend", name = ikJoint + "_" + fkJoint + "_" + "Blend")

    for i in "XYZ":
        cmds.connectAttr(ikJoint + ".rotate" + i, pairBlend + ".inRotate" + i + "1")
    
    for i in "XYZ":
        cmds.connectAttr(ikJoint + ".translate" + i, pairBlend + ".inTranslate" + i + "1")
        
    for i in "XYZ":
        cmds.connectAttr(fkJoint + ".rotate" + i, pairBlend + ".inRotate" + i + "2")
        
    for i in "XYZ":
        cmds.connectAttr(fkJoint + ".translate" + i, pairBlend + ".inTranslate" + i + "2")
        
    for i in "XYZ":
        cmds.connectAttr(pairBlend + ".outRotate" + i, targtJoint + ".rotate" + i)
        
    for i in "XYZ":
        cmds.connectAttr(pairBlend + ".outTranslate" + i, targtJoint + ".translate" + i)

    

def CreateMultiPairBlends():
    # read IK Joints Selection to list
    try:
        ikJoints = utils.load_data(IK_JOINT_SELECTION_PATH)
    except:
        raise log.error("There is no IK Joint Selection!!")
    
    # read FK Joints Selection to list
    try:
        fkJoints = utils.load_data(FK_JOINT_SELECTION_PATH)
    except:
        raise log.error("There is no FK Joint Selection!!")

    # read Target Joints Selection to list 
    try:
        targetJoints = utils.load_data(TARGET_JOINT_SELECTION_PATH)
    except:
        raise log.error("There is no target Joint Selection!!")

    #log.info("ik List {}, fk List {}, targetList {}".format(ikJoints[0], fkJoints[0], targetJoints[0]))
    os.remove(IK_JOINT_SELECTION_PATH)
    os.remove(FK_JOINT_SELECTION_PATH)
    os.remove(TARGET_JOINT_SELECTION_PATH)

    # compare List lengths 
    if len(ikJoints) == len(fkJoints) and len(fkJoints) == len(targetJoints):
        print(len(ikJoints))
    else:
        raise log.error("All selections need to have the same length!!")

    # create pair Blend
    for i in range(len(targetJoints)):
        CreateSinglePairBlend(ikJoints[i], fkJoints[i], targetJoints[i])





def CreateMultiIKFKBlendUI():
    #window
    configWindow = cmds.window(title="Multi_IKFK_Blend", iconName = "MultiBlend", widthHeight=(200, 300), sizeable=True)

    #window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Create Multi IKFK pairBlends", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    #Define IK Joints Label
    ikJointsLabel = cmds.text(label="Define IK Joints", height = 20, backgroundColor = [.8, .8, .8])

    #Define IK Joints Button
    ikJointsButton = cmds.button(label="Store IK Joints", command = lambda _: StoreIKJointsSelection(ikJointsLabel))

    #SpaceDivider
    cmds.text(label="", height=10)

    #Define FK Joitns Label
    fkJointsLabel = cmds.text(label="Define FK Joints", height = 20, backgroundColor = [.8, .8, .8])

    #Define FK Joints Button
    fkJointsButton = cmds.button(label="Store FK Joints", command = lambda _: StoreFKJointsSelection(fkJointsLabel))

    #SpaceDivider
    cmds.text(label="", height=10)

    #Define FK Joints Label
    targetJointsLabel = cmds.text(label="Define Target Joints", height = 20, backgroundColor = [.8, .8, .8])

    #Define FK Joints Button
    fkJointsButton = cmds.button(label="Store Target Joints", command = lambda _: StoreTargetJointsSelection(targetJointsLabel))

    #SpaceDivider
    cmds.text(label="", height=20)

    #Create pairBlends Button
    createPairBlendsButton = cmds.button(label = "Create pair blends", command = lambda _: CreateMultiPairBlends())

    #display Window 
    cmds.showWindow(configWindow)






#=======================================
## IkFk Multi PairBlend Connect - END
#=======================================


#=======================================
## Add Soft IK Function - Credit to Tim Colman and Martin Lanton From CGMA For most of the Code
#=======================================
def SoftIKConfigInterface():
    configwindow = cmds.window(title="AddSoftIK", widthHeight= (220, 50), sizeable=True)

    cmds.rowColumnLayout( adjustableColumn = True)


    ikHandleName = common.buildUserInputGrp("set IKHandle ", "Not Jet Set", 30)
    ikLocatorName = common.buildUserInputGrp("set IKLocator ", "Not Jet Set", 30)

    label = cmds.text(label="Leg Name: ")
    name = cmds.textField()

    cmds.button(label="Add Soft IK", command=lambda _: add_softIK(cmds.text(ikHandleName, query=True, label=True), cmds.text(ikLocatorName, query=True, label=True), cmds.textField(name, query=True, text=True)))

    cmds.showWindow(configwindow)

def get_aim_axis(joint_name):
    """Returns the axis pointed down the chain as a string

    Args:
        joint_name:  Name of joint to check for primary axis

    Example:
        get_aim_axis('joint4')
        # Result: 'y' #
    """
    child_joint = cmds.listRelatives(joint_name, c=True)

    if not child_joint:
        log.exception(
            "{0} does not have any children to check the aim axis".format(joint_name)
        )
        return False

    else:
        # Get translate values for child joint
        tx = cmds.getAttr("{}.translateX".format(child_joint[0]))
        ty = cmds.getAttr("{}.translateY".format(child_joint[0]))
        tz = cmds.getAttr("{}.translateZ".format(child_joint[0]))

        # Absolute translate values (basically always gives you a positive value
        atx = abs(tx)
        aty = abs(ty)
        atz = abs(tz)

        # Max function returns the largest value of the input values
        axis_tmp_val = max(atx, aty)
        axis_val = max(axis_tmp_val, atz)

        axes = ["x", "y", "z"]
        trans = [tx, ty, tz]
        abs_trans = [atx, aty, atz]

        # Loop through abs translate values -
        # compare max trans value with each trans axis value
        for i in range(len(abs_trans)):
            if axis_val == abs_trans[i]:
                # if our highest trans axis value matches the current trans value
                # then we've found our axis, next determine if that axis is
                # positive or negative by checking if it's less than 0.0
                axis_tmp = axes[i]
                if trans[i] < 0.0:
                    axis = "-{}".format(axis_tmp)
                else:
                    axis = axis_tmp
        return axis


def add_attribute_separator(object, attr_name):
    """Create a separator attribute on the specified control object

    Args:
        control: The control to add the separator attribute to
        attr: The separator attribute name

    Returns:

    Example:
        add_attribute_separator('Lf_arm_ctrl', '___')
    """
    # Check that object exists
    if not cmds.objExists(object):
        raise Exception("Control object {} does not exist!".format(object))

    # Check if attribute exists
    if cmds.objExists("{}.{}".format(object, attr_name)):
        raise Exception(
            "Control attribute {}.{} already exists!".format(object, attr_name)
        )

    # Create attribute
    cmds.addAttr(object, ln=attr_name, at="enum", en=":-:")
    cmds.setAttr("{}.{}".format(object, attr_name), cb=True)
    cmds.setAttr("{}.{}".format(object, attr_name), l=True)

    # Return result
    return "{}.{}".format(object, attr_name)


def add_softIK(ik_handle, ik_ctl, base_name):
    """Adds softIK to ikHandle to help avoid "popping" behavior as
    joint chain straightens.

    Note:  This method effectively moves the IK end effector's pivot
    as the length between the first ik joint and the anim control increases
    towards fully straightened

    Args:
        ik_handle:  IK handle that the soft ik effect will be added
        ik_ctl:  The anim control the ik_handle is constrained to
        base_name:  Base naming convention that will be used for newly created nodes

    Example:
        add_softIK( 'ikHandle2', 'ik_ctl', 'lf_arm')
    """
    if cmds.objExists(ik_handle):
        # Get end effector node from ik_handle
        end_effector = cmds.listConnections("{}.endEffector".format(ik_handle))[0]

        # Get list of joints controlled by ik_handle
        ik_joints = cmds.ikHandle(ik_handle, q=True, jointList=True)
        if len(ik_joints) != 2:
            log.error(
                "IK handle does not control enough joints, make sure this is a two bone IK setup"
            )
        else:
            ik_joints.append(
                cmds.listRelatives(ik_joints[1], children=True, type="joint")[0]
            )
        log.debug("IK joint list: {}".format(ik_joints))

        # Find the first joints aim axis (primary axis), handle if axis is negative as well
        aim_axis = get_aim_axis(ik_joints[0])
        aim_axis = aim_axis.capitalize()
        log.debug("IK joint aim axis: {}".format(aim_axis))

        neg_axis = False
        if "-" in aim_axis:
            neg_axis = True
            aim_axis = aim_axis.replace("-", "")
            aim_axis = aim_axis.capitalize()

        # Get abs ik mid and tip joints translate values to find that bones length
        mid_trans_axis_val = abs(
            cmds.getAttr("{}.translate{}".format(ik_joints[1], aim_axis))
        )
        tip_trans_axis_val = abs(
            cmds.getAttr("{}.translate{}".format(ik_joints[2], aim_axis))
        )
        chain_length = mid_trans_axis_val + tip_trans_axis_val

        # Create distance setup to track distance from start joint to controller
        start_pos_tfm = cmds.createNode(
            "transform", name="{}_startPos_tfm".format(base_name)
        )
        end_pos_tfm = cmds.createNode(
            "transform", name="{}_endPos_tfm".format(base_name)
        )
        cmds.pointConstraint(ik_joints[0], start_pos_tfm)
        cmds.pointConstraint(ik_ctl, end_pos_tfm)
        dist_node = cmds.createNode(
            "distanceBetween", name="{}_softIk_distance".format(base_name)
        )
        cmds.connectAttr(
            "{}.translate".format(start_pos_tfm), "{}.point1".format(dist_node)
        )
        cmds.connectAttr(
            "{}.translate".format(end_pos_tfm), "{}.point2".format(dist_node)
        )

        # Add softIK attrs to control - do attr names make sense here?
        add_attribute_separator(ik_ctl, "___")
        cmds.addAttr(
            ik_ctl,
            ln="soft_value",
            at="double",
            min=0.001,
            max=2,
            dv=0.001,
            k=True,
            hidden=False,
        )
        cmds.addAttr(ik_ctl, ln="dist_value", at="double", dv=0, k=True, hidden=False)
        cmds.addAttr(ik_ctl, ln="softIk", at="double", min=0, max=20, dv=0, k=True)
        cmds.connectAttr(
            "{}.distance".format(dist_node), "{}.dist_value".format(ik_ctl)
        )

        soft_remap = cmds.createNode(
            "remapValue", n="{}_soft_remapValue".format(base_name)
        )
        cmds.setAttr("{}.inputMin".format(soft_remap), 0)
        cmds.setAttr("{}.inputMax".format(soft_remap), 20)
        cmds.setAttr("{}.outputMin".format(soft_remap), 0.001)
        cmds.setAttr("{}.outputMax".format(soft_remap), 2)
        cmds.connectAttr("{}.softIk".format(ik_ctl), "{}.inputValue".format(soft_remap))
        cmds.connectAttr(
            "{}.outValue".format(soft_remap), "{}.soft_value".format(ik_ctl)
        )

        # ==========
        # Add Utility nodes

        # Plus Minus Average nodes
        len_minus_soft_pma = cmds.createNode(
            "plusMinusAverage", n="{}_len_minus_soft_pma".format(base_name)
        )  # lspma
        chaindist_minus_lenminussoft_pma = cmds.createNode(
            "plusMinusAverage",
            n="{}_chaindist_minus_lenminussoft_pma".format(base_name),
        )  # dslspma
        one_minus_pow = cmds.createNode(
            "plusMinusAverage", n="{}_one_minus_pow_pma".format(base_name)
        )  # opwpma
        plus_len_minus_soft_pma = cmds.createNode(
            "plusMinusAverage", n="{}_plus_len_minus_soft_pma".format(base_name)
        )  # plpma
        chain_dist_diff_pma = cmds.createNode(
            "plusMinusAverage", n="{}_chain_dist_diff_pma".format(base_name)
        )  # ddpma
        default_position_pma = cmds.createNode(
            "plusMinusAverage", n="{}_default_pos_pma".format(base_name)
        )  # dppma

        # Multiply Divide nodes
        nxm_mdn = cmds.createNode(
            "multiplyDivide", n="{}_negate_x_minus_mdn".format(base_name)
        )
        ds_mdn = cmds.createNode(
            "multiplyDivide", n="{}_divBy_soft_mdn".format(base_name)
        )
        pow_mdn = cmds.createNode("multiplyDivide", n="{}_pow_mdn".format(base_name))
        ts_mdn = cmds.createNode(
            "multiplyDivide", n="{}_times_soft_mdn".format(base_name)
        )

        # Add Double Linear nodes
        ee_adl = cmds.createNode(
            "addDoubleLinear", n="{}_endeffector_adl".format(base_name)
        )

        # Condition node
        len_minus_soft_cond = cmds.createNode(
            "condition", n="{}_len_minus_soft_cdn".format(base_name)
        )

        if neg_axis:
            neg_mdl = cmds.createNode(
                "multDoubleLinear", n="{}_negative_mdl".format(base_name)
            )
            cmds.setAttr("{}.input2".format(neg_mdl), -1.0)

        # ==========
        # Set Utility node values
        cmds.setAttr("{}.operation".format(len_minus_soft_pma), 2)
        cmds.setAttr("{}.operation".format(chaindist_minus_lenminussoft_pma), 2)
        cmds.setAttr("{}.operation".format(nxm_mdn), 1)
        cmds.setAttr("{}.operation".format(ds_mdn), 2)
        cmds.setAttr("{}.operation".format(pow_mdn), 3)
        cmds.setAttr("{}.operation".format(one_minus_pow), 2)
        cmds.setAttr("{}.operation".format(ts_mdn), 1)
        cmds.setAttr("{}.operation".format(plus_len_minus_soft_pma), 1)
        cmds.setAttr("{}.operation".format(len_minus_soft_cond), 5)
        cmds.setAttr("{}.operation".format(chain_dist_diff_pma), 2)
        cmds.setAttr("{}.operation".format(default_position_pma), 2)

        # ==========
        # Connect Utility nodes
        cmds.setAttr("{}.input1D[0]".format(len_minus_soft_pma), chain_length)
        cmds.connectAttr(
            "{}.soft_value".format(ik_ctl), "{}.input1D[1]".format(len_minus_soft_pma)
        )
        cmds.connectAttr(
            "{}.distance".format(dist_node),
            "{}.input1D[0]".format(chaindist_minus_lenminussoft_pma),
        )
        cmds.connectAttr(
            "{}.output1D".format(len_minus_soft_pma),
            "{}.input1D[1]".format(chaindist_minus_lenminussoft_pma),
        )
        cmds.connectAttr(
            "{}.output1D".format(chaindist_minus_lenminussoft_pma),
            "{}.input1X".format(nxm_mdn),
        )
        cmds.setAttr("{}.input2X".format(nxm_mdn), -1)
        cmds.connectAttr("{}.outputX".format(nxm_mdn), "{}.input1X".format(ds_mdn))
        cmds.connectAttr("{}.soft_value".format(ik_ctl), "{}.input2X".format(ds_mdn))
        cmds.setAttr("{}.input1X".format(pow_mdn), 2.718281828)
        cmds.connectAttr("{}.outputX".format(ds_mdn), "{}.input2X".format(pow_mdn))
        cmds.setAttr("{}.input1D[0]".format(one_minus_pow), 1)
        cmds.connectAttr(
            "{}.outputX".format(pow_mdn), "{}.input1D[1]".format(one_minus_pow)
        )
        cmds.connectAttr(
            "{}.output1D".format(one_minus_pow), "{}.input1X".format(ts_mdn)
        )
        cmds.connectAttr("{}.soft_value".format(ik_ctl), "{}.input2X".format(ts_mdn))
        cmds.connectAttr(
            "{}.outputX".format(ts_mdn), "{}.input1D[0]".format(plus_len_minus_soft_pma)
        )
        cmds.connectAttr(
            "{}.output1D".format(len_minus_soft_pma),
            "{}.input1D[1]".format(plus_len_minus_soft_pma),
        )
        cmds.connectAttr(
            "{}.output1D".format(len_minus_soft_pma),
            "{}.firstTerm".format(len_minus_soft_cond),
        )
        cmds.connectAttr(
            "{}.distance".format(dist_node), "{}.secondTerm".format(len_minus_soft_cond)
        )
        cmds.connectAttr(
            "{}.distance".format(dist_node),
            "{}.colorIfFalseR".format(len_minus_soft_cond),
        )
        cmds.connectAttr(
            "{}.output1D".format(plus_len_minus_soft_pma),
            "{}.colorIfTrueR".format(len_minus_soft_cond),
        )
        cmds.connectAttr(
            "{}.outColorR".format(len_minus_soft_cond),
            "{}.input1D[0]".format(chain_dist_diff_pma),
        )
        cmds.connectAttr(
            "{}.distance".format(dist_node), "{}.input1D[1]".format(chain_dist_diff_pma)
        )

        cmds.setAttr("{}.input1D[0]".format(default_position_pma), 0)
        cmds.connectAttr(
            "{}.output1D".format(chain_dist_diff_pma),
            "{}.input1D[1]".format(default_position_pma),
        )
        cmds.connectAttr(
            "{}.output1D".format(default_position_pma), "{}.input1".format(ee_adl)
        )
        cmds.setAttr("{}.input2".format(ee_adl), tip_trans_axis_val)

        # Connect final result to end effector's aim_axis
        ee_connected = cmds.listConnections(
            "{}.translate{}".format(end_effector, aim_axis),
            source=True,
            destination=False,
            plugs=True,
        )
        if ee_connected:
            cmds.disconnectAttr(
                ee_connected[0], "{}.translate{}".format(end_effector, aim_axis)
            )

        if neg_axis:
            neg_mdn = cmds.createNode(
                "multiplyDivide", n="{}_neg_mdn".format(base_name)
            )
            cmds.connectAttr("{}.output".format(ee_adl), "{}.input1X".format(neg_mdn))
            cmds.setAttr("{}.input2X".format(neg_mdn), -1)
            cmds.connectAttr(
                "{}.outputX".format(neg_mdn),
                "{}.translate{}".format(end_effector, aim_axis),
            )
        else:
            cmds.connectAttr(
                "{}.output".format(ee_adl),
                "{}.translate{}".format(end_effector, aim_axis),
            )

        cmds.parent(start_pos_tfm, end_pos_tfm, ik_ctl)
        cmds.select(ik_ctl)
        return ik_ctl

    else:
        log.error("IK handle {} does not exist in scene".format(ik_handle))