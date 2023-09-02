#Module import
import maya.cmds as cmds
from tlpf_toolkit.utils import GeneralFunctions


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