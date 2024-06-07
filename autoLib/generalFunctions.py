import maya.cmds as cmds
import logging

from tlpf_toolkit.autoLib import autolibGlobalVariables as gVar

#function to hide all the default channel box attributes from a list of transforms
def untouchableTransform(transforms, t = True, r = True, s = True):
    #clean all the channelbox attributes from a transform
    for transform in transforms:
        for channel in "XYZ":
            if t:
                cmds.setAttr(f"{transform}.translate{channel}", keyable=False)
            if r:
                cmds.setAttr(f"{transform}.rotate{channel}", keyable=False)
            if s:
                cmds.setAttr(f"{transform}.scale{channel}", keyable=False)
        cmds.setAttr(f"{transform}.visibility", keyable=False)

#function to lock channelBox Transformation channels
def lockChannelboxTransformChannel(srt, t = True, r = True, s = True):
    for channel in "XYZ":
        if t:
            cmds.setAttr(f"{srt}.translate{channel}", lock = True)
        if r:
            cmds.setAttr(f"{srt}.rotate{channel}", lock = True)
        if s:
            cmds.setAttr(f"{srt}.scale{channel}", lock = True)

#function to create an Attribute Divider
def createChannelboxAttributeDivider(target, name = "Divider"):
    cmds.addAttr(target, ln=name, at="enum", en=gVar.ATTRDIVIDERSYMBOLS, keyable=False)
    cmds.setAttr(target + "." + name, cb=True)

#function to color a node draw override attribute
def setOverrideColor(shapes, color):

    for shape in shapes:
        cmds.setAttr(f"{shape}.overrideEnabled", 1)
        cmds.setAttr(f"{shape}.overrideRGBColors", 1)
        cmds.setAttr(f"{shape}.overrideColorR", color[0])
        cmds.setAttr(f"{shape}.overrideColorG", color[1])
        cmds.setAttr(f"{shape}.overrideColorB", color[2])

#function to create the overall top level rig hirarchy
def createNewRigHirarchy(name):

    #list of topLevel transforms
    topLevelRigStructure = []

    #top level hirachry transform
    topLevelNode = cmds.createNode("transform", name = f"{name}_Rig_hrc")
    topLevelRigStructure.append(topLevelNode)

    #charcter hirarchy transform
    characterNode = cmds.createNode("transform", name = f"{name}_character_hrc", parent = topLevelNode)
    topLevelRigStructure.append(characterNode)

    #component hirarchy transform
    componentNode = cmds.createNode("transform", name = f"{name}_component_hrc", parent = topLevelNode)
    topLevelRigStructure.append(componentNode)

    #guide hirarchy transfrom
    guideNode = cmds.createNode("transform", name = f"{name}_guide_hrc", parent = topLevelNode)
    topLevelRigStructure.append(guideNode)

    #skeleton hirarchy transform
    skeletonNode = cmds.createNode("transform", name = "skeleton_hrc", parent = characterNode)
    topLevelRigStructure.append(skeletonNode)

    #mesh hirarchy transform
    meshNode = cmds.createNode("transform", name = "mesh_hrc", parent = characterNode)
    topLevelRigStructure.append(meshNode)

    #clean all hirarchy nodes channel box
    untouchableTransform(topLevelRigStructure)

    return topLevelRigStructure

#function to create a new rig component structure for the outliner
def createRigComponent(name, parentNode = "world", side = gVar.CENTERDECLARATION, additionalStructure = []):

    #base component Structure
    componentStructure = ["input", "output", "control", "deform", "mod"]

    if len(additionalStructure) != 0:
        componentStructure = componentStructure + additionalStructure

    #create component top level node
    componentTopLevelNode = cmds.createNode("transform", name = f"{side}_{name}_cmpnt_hrc", parent = parentNode)

    #clean top level Node channel box
    untouchableTransform([componentTopLevelNode])

    #component Structure Transform Nodes
    componentStructureNodes = []

    #create component Structure
    for index, hrc in enumerate(componentStructure):
        componentStructure[index] = cmds.createNode("transform", name = f"{side}_{name}_{hrc}_hrc", parent = componentTopLevelNode)

    #clean component structure nodes channel box
    untouchableTransform(componentStructure)

    return componentTopLevelNode, componentStructure

#function to create a single guide
def createGuide(name, side = gVar.CENTERDECLARATION, cmpnt = "world", color = [0.5, 0.5, 0.5], size = 5):
    #create guide locator
    guideLoc = cmds.spaceLocator(name = f"{side}_{cmpnt}_{name}_guide_srt")[0]

    #get Guide Shape
    guideLocShape = cmds.listRelatives(guideLoc, children = True)[0]

    #set guide Shape Color
    cmds.setAttr(f"{guideLocShape}.overrideEnabled", 1)
    cmds.setAttr(f"{guideLocShape}.overrideRGBColors", 1)
    cmds.setAttr(f"{guideLocShape}.overrideColorR", color[0])
    cmds.setAttr(f"{guideLocShape}.overrideColorG", color[1])
    cmds.setAttr(f"{guideLocShape}.overrideColorB", color[2])

    #set Guide Size
    for channel in "XYZ":
        cmds.setAttr(f"{guideLocShape}.localScale{channel}", size)
        cmds.setAttr(f"{guideLocShape}.localScale{channel}", size)
        cmds.setAttr(f"{guideLocShape}.localScale{channel}", size)

    #TODO Furthur modification to the appearence of the guide
    #
    #
    #
    #

    return guideLoc

#function to create Guide Chains based on a numerical value
def createGuideChainNumBased(numOfGuides, cmpnt = "world", side = gVar.CENTERDECLARATION, color = [0.5, 0.5, 0.5],
                             defaultDist = 0.5, defaultforwardAxies = "X", baseName = "ChainGuide"):
    
    #list of names that will be assigend to the guides
    guideNameList = []

    #create guideNames iterative
    for amount in range(numOfGuides):
        guideNameList.append(f"{baseName}_{amount}")
    
    #call guide chain function to create the guide chain
    createGuideChain(guideNameList, cmpnt, side, color, defaultDist, defaultforwardAxies)

    return guideNameList

#function to create a curve line between guides
def createLineEdgeBetweenGuides(guides, color = [0.5, 0.5, 0.5]):
    #check if there is more than one guide
    if len(guides) > 0:
        for index, guide in enumerate(guides):
            if index + 1 < len(guides):
                #create the curve shape
                edgeLine = cmds.curve(p=[(0,0,0), (0,0,0)], d=1)

                #rename transform
                edgeLine = cmds.rename(edgeLine, guide + '_edgeLineConnector')

                #get srt shape
                edgeLineShape = cmds.listRelatives(edgeLine, children = True)[0]

                #parent shape to guide
                cmds.parent(edgeLineShape, guide, shape=True, relative=True)

                #delete original edge srt
                cmds.delete(edgeLine)

                #constraint the edge line to the next guide
                multmatrix = cmds.createNode('multMatrix', name = f"{guide}_edgeLineConnection_mmtx_fNode")
                decomposeMatrix = cmds.createNode('decomposeMatrix', name = f"{guide}_edgeLineConnection_dcm_fNode")


                cmds.connectAttr(multmatrix + '.matrixSum', decomposeMatrix + '.inputMatrix')

                cmds.connectAttr(guides[index + 1] + '.worldMatrix', multmatrix + '.matrixIn[0]')
                cmds.connectAttr(guide + '.worldInverseMatrix[0]', multmatrix + '.matrixIn[1]')


                cmds.connectAttr(decomposeMatrix + '.outputTranslateX', edgeLineShape + '.controlPoints[0].xValue')
                cmds.connectAttr(decomposeMatrix + '.outputTranslateY', edgeLineShape + '.controlPoints[0].yValue')
                cmds.connectAttr(decomposeMatrix + '.outputTranslateZ', edgeLineShape + '.controlPoints[0].zValue')

                #set line Color
                cmds.setAttr(f"{edgeLineShape}.overrideEnabled", 1)
                cmds.setAttr(f"{edgeLineShape}.overrideRGBColors", 1)
                cmds.setAttr(f"{edgeLineShape}.overrideColorR", color[0])
                cmds.setAttr(f"{edgeLineShape}.overrideColorG", color[1])
                cmds.setAttr(f"{edgeLineShape}.overrideColorB", color[2])

#function to create a chain of guides
def createGuideChain(guideNames = [], cmpnt = "world", side = gVar.CENTERDECLARATION, color = [0.5, 0.5, 0.5], 
                     defaultDist = 0.5, defaultforwardAxies = "X"):
    
    #list to store the created Guides
    guideChain = []

    #create guides for each input name
    for name in guideNames:
        newGuide = createGuide(name, side, cmpnt, color)
        guideChain.append(newGuide)
    
    #reverseOrder of Guides
    revGuideChain = guideChain[::-1]

    #parent all guide in a hirarchy
    for index, guide in enumerate(revGuideChain):
        if index + 1 < len(guideChain):
            cmds.parent(guide, revGuideChain[index + 1])

    #space the guides from each other in default position
    for index, guide in enumerate(guideChain):
        if index > 0:
            #decide the direction the chain will be offset by default
            cmds.setAttr(f"{guide}.translate{defaultforwardAxies}", defaultDist)
    
    #connect Guides with curve Lines
    createLineEdgeBetweenGuides(guideChain)

    return guideChain

#function to create a output Transform from an input transform
def createOutputTransformSRTNode(transformInputs, outputDir, connectRotateOrder = True):
    #create Transforms
    outputTransforms = []

    for srt in transformInputs:
        newSrt = cmds.createNode("transform", name = f"{srt}_wrldMtx_{gVar.NODEUSAGETYPEOUTPUT}")
        cmds.connectAttr(f"{srt}.worldMatrix[0]", f"{newSrt}.offsetParentMatrix")
        if connectRotateOrder:
            cmds.connectAttr(f"{srt}.rotateOrder", f"{newSrt}.rotateOrder" )
        cmds.parent(newSrt, outputDir)
        outputTransforms.append(newSrt)

    return outputTransforms

#function to check if there is any transformation values in a given srt
def hasTransformValues(srt):

    #get the current Position Matrix of a given srt
    srtTransformMatrix = cmds.xform(srt, query=True, m = True)
    hasTransformations = False

    #round Values in Transformation Matrix
    for index, value in enumerate(srtTransformMatrix):
        roundedValue = round(value, 5)
        srtTransformMatrix[index] = roundedValue

    if srtTransformMatrix != gVar.IDENTITYMATRIXLIST:
        hasTransformations = True

    return srtTransformMatrix, hasTransformations

#function to evaluete if a given joint has joint Orient Values
def jointHasOrientValues(jnt):
    for channel in "XYZ":
        channelValue = cmds.getAttr(f"{jnt}.jointOrient{channel}")
        print(channelValue)
        if channelValue != 0:
            return False
    return True

#function to create a four by four vector node with input matrix transform
def createFourByFourMayaMatrixNode(matrix, nodeName = "tmp_fourbyfour_matrix"):
    #create temporary fourByFourMatrix to set offsetParent Matrix later
    matrixNode = cmds.createNode("fourByFourMatrix", name = nodeName)
    
    #set control variables
    indecies = [4, 4, 4, 4]
    counter = 0

    for index, vector in enumerate(indecies):
        for entry in range(vector):
            cmds.setAttr(f"{matrixNode}.in{index}{entry}", matrix[counter])
            counter += 1

    return matrixNode

#function to remove all values from srt channelbox and set to default identity matrix
def clearTransforms(srt, t = True, r = True, s = True): 
    for channel in "XYZ":
        if t:
            cmds.setAttr(f"{srt}.translate{channel}", 0) # reset Translation if True
        if r:
            cmds.setAttr(f"{srt}.rotate{channel}", 0) # reset Rotation if True
        if s: 
            cmds.setAttr(f"{srt}.scale{channel}", 1) # reset Scale if True

#function to move Srt Values to ther OffsetParentMatrix
def moveSrtValuesToOffsetParentMatrix(srt):
    #check if the input object type is string
    if type(srt) == str and cmds.objExists(srt):
        #get object space Matrix
        currentObjectSpaceMatrix = cmds.xform(srt, query = True, m = True)

        #create tmp four by four matrix 
        matrixNode = createFourByFourMayaMatrixNode(currentObjectSpaceMatrix)

        #connect output matrix to offset parent Matrix
        cmds.connectAttr(f"{matrixNode}.output", f"{srt}.offsetParentMatrix")

        #clean channelbox transforms
        clearTransforms(srt)

        #dissconnect the four by four matrix from the target object
        cmds.disconnectAttr(f"{matrixNode}.output", f"{srt}.offsetParentMatrix")

        #delete tmp matrix Node
        cmds.delete(matrixNode)
    else:
        cmds.warning("The input Object is not String and therefore the transforms of the given object cannot be moved to there respective offset Parent Matrix!!")

#function to create a outout deform with world matrix decomposed Srt Values
def createWrldMtxDeformOutput(inputSrt, outputDir = "world", connectRotationOrder = True):
    
    #list of name tokens from input
    nameTokenList = inputSrt.split("_")
    
    nameTokenString = nameTokenList[0] + "_" + nameTokenList[1] + "_" + nameTokenList[2]
    
    #create new decompose node
    deformDecomposeNode = cmds.createNode("decomposeMatrix", name = f"{nameTokenString}_dcm_fNode")
    
    #connect the output transform
    deformOutputDeformNode = cmds.createNode("transform", name = f"{nameTokenString}_wrldMtx_defOutput", parent = outputDir)
    
    #connect srt to deformDecompose Node
    cmds.connectAttr(f"{inputSrt}.worldMatrix[0]", f"{deformDecomposeNode}.inputMatrix")
    
    if connectRotationOrder:
        cmds.connectAttr(f"{inputSrt}.rotateOrder", f"{deformDecomposeNode}.inputRotateOrder")
    
    #connect srt to output transform
    for channel in "XYZ":
        cmds.connectAttr(f"{deformDecomposeNode}.outputTranslate{channel}", f"{deformOutputDeformNode}.translate{channel}")
        cmds.connectAttr(f"{deformDecomposeNode}.outputRotate{channel}",  f"{deformOutputDeformNode}.rotate{channel}")
        cmds.connectAttr(f"{deformDecomposeNode}.outputScale{channel}",  f"{deformOutputDeformNode}.scale{channel}")

    return deformOutputDeformNode

#function to connect Srt vales to a compose Matrix Node
def connectSRTToComposeMatrix(srt, mtx, rotateOrder = True):
    for channel in "XYZ":
        cmds.connectAttr(f"{srt}.translate{channel}", f"{mtx}.inputTranslate{channel}")
        cmds.connectAttr(f"{srt}.rotate{channel}", f"{mtx}.inputRotate{channel}")
        cmds.connectAttr(f"{srt}.scale{channel}", f"{mtx}.inputScale{channel}")
    if rotateOrder:
            cmds.connectAttr(f"{srt}.rotateOrder", f"{mtx}.inputRotateOrder")

#function to disconnect a composeMatrix from an Srt input
def disconnectComposeMatrixFromSrt(srt, cm):
    #try to disconnect the rotate order attribtue
    try:
        cmds.disconnectAttr(f"{srt}.rotateOrder", f"{cm}.inputRotateOrder")
    except:
        print(f"No Rotate Order Connection Betwee {srt} and {cm}")

    #try to disconnect all the srt values
    for channel in "XYZ":
        try:
            cmds.disconnectAttr(f"{srt}.translate{channel}", f"{cm}.inputTranslate{channel}")
        except:
            print(f"No Translate {channel} Connection Betwee {srt} and {cm}")
        try:
            cmds.disconnectAttr(f"{srt}.rotate{channel}", f"{cm}.inputRotate{channel}")
        except:
            print(f"No Rotate {channel} Connection Betwee {srt} and {cm}")
        try:
            cmds.disconnectAttr(f"{srt}.scale{channel}", f"{cm}.inputScale{channel}")
        except:
            print(f"No Scale {channel} Connection Betwee {srt} and {cm}")

#function to connect a decompose Matrix Node to an SRT
def connectDecomposeMatrixToSrt(dcm, srt, rotateOrder = True, t = True, r = True, s = True):
   
    if rotateOrder:
            cmds.connectAttr(f"{dcm}.inputRotateOrder", f"{srt}.rotateOrder")
    
    for channel in "XYZ":
        if t:
            cmds.connectAttr(f"{dcm}.outputTranslate{channel}", f"{srt}.translate{channel}")
        if r:
            cmds.connectAttr(f"{dcm}.outputRotate{channel}", f"{srt}.rotate{channel}")
        if s:
            cmds.connectAttr(f"{dcm}.outputScale{channel}", f"{srt}.scale{channel}")

#function to create a compose matrix node From an Srt input
def createComposeMatrixFromSRT(srt, name = None):
    #create new compose matrix node
    if name == None:
        newCmNode = cmds.createNode("composeMatrix", name = f"{srt}_Offset_cm_fNode")
    else:
        newCmNode = cmds.createNode("composeMatrix", name = f"{name}_Offset_cm_fNode")

    connectSRTToComposeMatrix(srt, newCmNode, rotateOrder = True)

    return newCmNode
    
#function to create a matrix parent constraint
def createMatrixParentConstraint(source, target, t = True, r = True, s = True):
    #check Rotation Orders
    targetRotateOrder = cmds.getAttr(f"{target}.rotateOrder")
    sourceRotateOrder = cmds.getAttr(f"{source}.rotateOrder")
    
    if targetRotateOrder != sourceRotateOrder:
        print("RotationOrders between source and Target Objects do not Match.")
    else: 
    # check if we are working with a joint or an srt
        if cmds.nodeType(target) == "joint":
            #check the joint Orients
            if not jointHasOrientValues(target):
                pass

            #create the joint orient extra multiplication
        else:
            
            srtOffsetReaderObject = cmds.createNode("transform", name = "tmp_srtOffsetReader")
            
            #configure offset Obejct
            cmds.setAttr(f"{srtOffsetReaderObject}.rotateOrder", targetRotateOrder)
            cmds.matchTransform(srtOffsetReaderObject, target)
            cmds.parent(srtOffsetReaderObject, source)

            # check if there is a need to compute an offset
            OffsetMatrix, hasOffset = hasTransformValues(srtOffsetReaderObject)
            
            print(OffsetMatrix)

            # create mult matrix nodes
            parentConstraintMultMatrixNode = cmds.createNode("multMatrix", name = f"{target}_parentConstraint_mmtx_fNode")
            parentConstraintDecomposeNode = cmds.createNode("decomposeMatrix", name = f"{target}_parentConstraint_dcm_fNode")

            # connect setup
            cmds.connectAttr(f"{target}.parentInverseMatrix[0]", f"{parentConstraintMultMatrixNode}.matrixIn[0]")
            cmds.connectAttr(f"{source}.worldMatrix[0]", f"{parentConstraintMultMatrixNode}.matrixIn[1]")

            if hasOffset:
                # get the offset
                offsetMatrixNode = createComposeMatrixFromSRT(srtOffsetReaderObject, name = target)
                offsetMultMatrixNode = cmds.createNode("multMatrix", name = f"{target}_parentConstraintOffset_mmtx_fNode")

                #configure offset Multiplication
                cmds.connectAttr(f"{offsetMatrixNode}.outputMatrix", f"{offsetMultMatrixNode}.matrixIn[0]")
                cmds.connectAttr(f"{parentConstraintMultMatrixNode}.matrixSum", f"{offsetMultMatrixNode}.matrixIn[1]")
                
                #connect offset Multiplication to decompose
                cmds.connectAttr(f"{offsetMultMatrixNode}.matrixSum", f"{parentConstraintDecomposeNode}.inputMatrix")

                #disconnect tmp reader from offset matrix compose node
                disconnectComposeMatrixFromSrt(srtOffsetReaderObject, offsetMatrixNode)
            else:
                #connect multiplication to decompose 
                cmds.connectAttr(f"{parentConstraintMultMatrixNode}.matrixSum", f"{parentConstraintDecomposeNode}.inputMatrix")
            
            #connect decompose Values to target Object
            connectDecomposeMatrixToSrt(parentConstraintDecomposeNode, target, True, t, r, s)
            
            

            cmds.delete(srtOffsetReaderObject)

        

        