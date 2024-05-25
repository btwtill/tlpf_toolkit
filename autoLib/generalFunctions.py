import maya.cmds as cmds

#function to hide all the default channel box attributes from a list of transforms
def untouchableTransform(transforms):
    #clean all the channelbox attributes from a transform
    for transform in transforms:
        for channel in "XYZ":
            cmds.setAttr(f"{transform}.translate{channel}", keyable=False)
            cmds.setAttr(f"{transform}.rotate{channel}", keyable=False)
            cmds.setAttr(f"{transform}.scale{channel}", keyable=False)
        cmds.setAttr(f"{transform}.visibility", keyable=False)

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
def createRigComponent(name, parentNode = "world", additionalStructure = []):

    #base component Structure
    componentStructure = ["input", "output", "control", "deform", "mod"]

    if len(additionalStructure) != 0:
        componentStructure = componentStructure + additionalStructure

    #create component top level node
    componentTopLevelNode = cmds.createNode("transform", name = f"{name}_cmpnt_hrc", parent = parentNode)

    #clean top level Node channel box
    untouchableTransform([componentTopLevelNode])

    #create component Structure
    for hrc in componentStructure:
        cmds.createNode("transform", name = f"{hrc}", parent = componentTopLevelNode)

    #clean component structure nodes channel box
    untouchableTransform(componentStructure)

    return componentTopLevelNode, componentStructure

#function to create a single guide
def createGuide(name, side = "M", cmpnt = "world", color = [0.5, 0.5, 0.5]):
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

    return guideLoc

