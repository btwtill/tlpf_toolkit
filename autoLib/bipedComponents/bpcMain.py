import maya.cmds as cmds
from tlpf_toolkit.autoLib import autolibGlobalVariables as gVar
from tlpf_toolkit.autoLib import generalFunctions as gf


def createMainComponentGuide(rigName, cmpntName = "main"):
    #List to store Guides
    guides = []

    #create cmpntGuide hrc in rig hirarchy
    mainCmpntGuidehirarchy = cmds.createNode("transform", name = f"{cmpntName}_guides_hrc", parent = f"{rigName}_guide_hrc")

    #create main Component Guide
    mainGuide = gf.createGuide("globalCtrl", gVar.CENTERDECLARATION, "main", [1, 1, 0], 10)

    #parent main Component Guide to guide Hirarchy
    cmds.parent(mainGuide, mainCmpntGuidehirarchy)

    return guides

#compose character Main component
def composeMainComponent(rigName, guideDir, characterMesh = None, numOfMainControlOffsets = 1, 
                         size = 40, cmpntName = "main", color = [1, 1, 0], additionalMeshVisibilityAttributes = [[]], jointOrientation = "xyz"):

    #component Directory path
    rigComponentDirectoryPath = f"{rigName}_component_hrc"

    #create outliner structure
    mainComponentTopNode, mainComponentStructureNodes = gf.createRigComponent(cmpntName, rigComponentDirectoryPath)

    #create god node transform
    godNodeTransform = cmds.createNode("transform", name = f"{gVar.CENTERDECLARATION}_{cmpntName}_godNode_{gVar.NODEUSAGETYPETRANSFORM}")
    cmds.parent(godNodeTransform, mainComponentStructureNodes[2])
    gf.untouchableTransform([godNodeTransform])

    #calculate the size for the control circles
    if characterMesh == None:
        characterWidth = size
    else:
        characterBoundingBoxSpan = cmds.exactWorldBoundingBox(characterMesh)
        characterWidth = (characterBoundingBoxSpan[3] - characterBoundingBoxSpan[0]) / 4

    #create main Controls
    mainCtrlNode = cmds.circle(name = f"{gVar.CENTERDECLARATION}_{cmpntName}_global_{gVar.NODEUSAGETYPECONTROL}", radius = characterWidth, nr = [0,1,0])[0]
    cmds.parent(mainCtrlNode, godNodeTransform)

    #create main Offset Controls
    offsetControls = []
    for offCtrl in range(numOfMainControlOffsets):

        #parent first offset ctrl to main ctrl
        if len(offsetControls) == 0:
            newOffsetCtrl = cmds.circle(name = f"{gVar.CENTERDECLARATION}_{cmpntName}_globalOffset{offCtrl}_{gVar.NODEUSAGETYPECONTROL}", 
                                        radius = characterWidth - ((offCtrl + 1) * 4), nr = [0,1,0])[0]
            cmds.parent(newOffsetCtrl, mainCtrlNode)
            offsetControls.append(newOffsetCtrl)
        #parent all next offset ctrls to the one before themselves
        else:
            newOffsetCtrl = cmds.circle(name = f"{gVar.CENTERDECLARATION}_{cmpntName}_globalOffset{offCtrl}_{gVar.NODEUSAGETYPECONTROL}", 
                                        radius = characterWidth - ((offCtrl + 1) * 4), nr = [0,1,0])[0]
            cmds.parent(newOffsetCtrl, offsetControls[offCtrl - 1])
            offsetControls.append(newOffsetCtrl)
    
    #configure controls
    mainGuide = cmds.listRelatives(guideDir)[0]
    mainGuideRotationOrder = cmds.getAttr(f"{mainGuide}.rotateOrder")
    mainGuidePos = cmds.xform(mainGuide, query = True, ws=True, m = True)
    
    #set Rotation Order for all controls
    cmds.setAttr(f"{mainCtrlNode}.rotateOrder", mainGuideRotationOrder) # set Rotation Order on Main Control
    cmds.xform(mainCtrlNode, m = mainGuidePos, ws = True) # set Position on Main Control

    for offCtrl in offsetControls:
        cmds.setAttr(f"{offCtrl}.rotateOrder", mainGuideRotationOrder) #set Rotation order on Offset Controls

    #check for transform values on the main control and create buffer if necessary
    mainCtrlMatrix, mainCtrlHasTransformations = gf.hasTransformValues(mainCtrlNode)

    if mainCtrlHasTransformations:
        gf.moveSrtValuesToOffsetParentMatrix(mainCtrlNode)

    #configure the output of the main component
    mainCtrlOutputTransform = gf.createOutputTransformSRTNode([mainCtrlNode], mainComponentStructureNodes[1])
    offsetCtrlOutputTransforms = gf.createOutputTransformSRTNode(offsetControls, mainComponentStructureNodes[1])

    #configure Deformation output
    lastOffsetCtrlMember = offsetControls[-1]
    mainComponentDeformOutputNode = cmds.createNode("transform", name = f"{gVar.CENTERDECLARATION}_{cmpntName}_root_{gVar.NODEUSAGETYPEDEFORM}", parent = mainComponentStructureNodes[3])
    cmds.connectAttr(f"{lastOffsetCtrlMember}.worldMatrix[0]", f"{mainComponentDeformOutputNode}.offsetParentMatrix")
    cmds.connectAttr(f"{lastOffsetCtrlMember}.rotateOrder", f"{mainComponentDeformOutputNode}.rotateOrder")

    #get rig of the construction history of the initial ctrl shapes
    #get ctrl shapes
    mainCtrlInitialShape = cmds.listRelatives(mainCtrlNode, shapes = True)
    
    offsetCtrlInitialShapes = []
    for ctrl in offsetControls:
        listOfCtrlShapes = cmds.listRelatives(ctrl, shapes = True)
        offsetCtrlInitialShapes.append(listOfCtrlShapes)

    #color the global ctrls
    for shape in mainCtrlInitialShape:
        cmds.delete(shape, ch=True)  #delete construction History
        gf.setOverrideColor([shape], color) #set Color
        cmds.setAttr(f"{shape}.isHistoricallyInteresting", False)

    for ctrl in offsetCtrlInitialShapes:
        gf.setOverrideColor(ctrl, color) #set Color

        for shape in ctrl:
            cmds.delete(shape, ch=True) #delete construction History
            cmds.setAttr(f"{shape}.isHistoricallyInteresting", False)
    
    #clean Channelbox of ctrls
    gf.untouchableTransform([mainCtrlNode], t = False, r = False)
    gf.untouchableTransform(offsetControls, t = False, r = False)
    

    #configure the Attribute hub of the rig
    attributeHubNode = cmds.createNode("transform", name = f"{gVar.CENTERDECLARATION}_{cmpntName}_AttributeHub_output", parent = mainComponentStructureNodes[1])
    gf.untouchableTransform([attributeHubNode])

    #add Global Scale Attribute
    globalScaleAttributeName = "GlobalScale"
    cmds.addAttr(ln= globalScaleAttributeName, at = "float", minValue = 0.001, defaultValue = 1, keyable = True)

    #configure global scale attribute to component controls
    for channel in "XYZ":
        cmds.connectAttr(f"{attributeHubNode}.{globalScaleAttributeName}", f"{mainCtrlNode}.scale{channel}")
    
    #lock scale attribute channels in srt channelbox
    gf.lockChannelboxTransformChannel(mainCtrlNode, t=False, r = False)

    for offsetCtrl in offsetControls:
        gf.lockChannelboxTransformChannel(offsetCtrl, t=False, r = False)

    #publish scale Attribute to controls
    gf.createChannelboxAttributeDivider(mainCtrlNode, "GlobalAttributes")
    cmds.addAttr(mainCtrlNode, ln=globalScaleAttributeName, proxy = f"{attributeHubNode}.{globalScaleAttributeName}")

    for offsetCtrl in offsetControls:
        gf.createChannelboxAttributeDivider(offsetCtrl, "GlobalAttributes")
        cmds.addAttr(offsetCtrl, ln=globalScaleAttributeName, proxy = f"{attributeHubNode}.{globalScaleAttributeName}")

    

    #Mesh Attributes
    meshAttributes = ["character"]
    meshAttributeTargets = ["mesh_hrc"]

    #add Aditional Mesh Visibility Attributes
    for additionalAttr in additionalMeshVisibilityAttributes:
        if len(additionalAttr) > 1:
            meshAttributes.append(additionalAttr[1])
            meshAttributeTargets.append(additionalAttr[0])
        elif len(additionalAttr) == 1:
            meshAttributes.append(additionalAttr[0])
            meshAttributeTargets.append(additionalAttr[0])

    #add Divider to main Ctrls
    gf.createChannelboxAttributeDivider(mainCtrlNode, "GeometryAttributes")
    for offsetCtrl in offsetControls:
            gf.createChannelboxAttributeDivider(offsetCtrl, "GeometryAttributes")

    geoVisibilityAttributeSuffix = "_geo_visibility"
    geoSelectebilityAttributeSuffix = "_geo_selectebility"

    #add mesh attributes to attribute hub
    for index, attr in enumerate(meshAttributes):
        cmds.addAttr(attributeHubNode, ln=f"{attr}{geoVisibilityAttributeSuffix}", at = "enum", enumName = "OFF:ON", keyable = True) # add Visibility Attribute
        cmds.addAttr(attributeHubNode, ln=f"{attr}{geoSelectebilityAttributeSuffix}", at = "enum", enumName = "Normal:Template:Reference", keyable = True) # add Mesh Selectability Attribute

        #configure mesh attributes
        cmds.connectAttr(f"{attributeHubNode}.{attr}{geoVisibilityAttributeSuffix}", f"{meshAttributeTargets[index]}.visibility")
        cmds.setAttr(f"{attributeHubNode}.{attr}{geoVisibilityAttributeSuffix}", 1)

        cmds.setAttr(f"{meshAttributeTargets[index]}.overrideEnabled", 1)
        cmds.connectAttr(f"{attributeHubNode}.{attr}{geoSelectebilityAttributeSuffix}", f"{meshAttributeTargets[index]}.overrideDisplayType")

        #publish mesh attributes
        cmds.addAttr(mainCtrlNode, ln=f"{attr}{geoVisibilityAttributeSuffix}", proxy = f"{attributeHubNode}.{attr}{geoVisibilityAttributeSuffix}") # publish visibility to main Ctrl 
        cmds.addAttr(mainCtrlNode, ln=f"{attr}{geoSelectebilityAttributeSuffix}", proxy = f"{attributeHubNode}.{attr}{geoSelectebilityAttributeSuffix}") # publish selectablitiy to main Ctrl 

        for offsetCtrl in offsetControls:
            cmds.addAttr(offsetCtrl, ln=f"{attr}{geoVisibilityAttributeSuffix}", proxy = f"{attributeHubNode}.{attr}{geoVisibilityAttributeSuffix}") # publish visibility to offset Ctrl 
            cmds.addAttr(offsetCtrl, ln=f"{attr}{geoSelectebilityAttributeSuffix}", proxy = f"{attributeHubNode}.{attr}{geoSelectebilityAttributeSuffix}") # publish selectability to offset Ctrl


