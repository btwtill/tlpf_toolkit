import maya.cmds as cmds
from tlpf_toolkit.autoLib import autolibGlobalVariables as gVar

#function to hide all the default channel box attributes from a list of transforms
def untouchableTransform(transforms):
    #clean all the channelbox attributes from a transform
    for transform in transforms:
        for channel in "XYZ":
            cmds.setAttr(f"{transform}.translate{channel}", keyable=False)
            cmds.setAttr(f"{transform}.rotate{channel}", keyable=False)
            cmds.setAttr(f"{transform}.scale{channel}", keyable=False)
        cmds.setAttr(f"{transform}.visibility", keyable=False)

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
        newSrt = cmds.createNode("transform", name = f"{srt}_wrldMtx_{gVar.NODEUSAGETYPEOUTPUT}]")
        cmds.connectAttr(f"{srt}.worldMatrix[0]", f"{newSrt}.offsetParentMatrix")
        if connectRotateOrder:
            cmds.connectAttr(f"{srt}.rotateOrder", f"{newSrt}.rotateOrder" )
        cmds.parent(newSrt, outputDir)
        outputTransforms.append(newSrt)

    return outputTransforms
