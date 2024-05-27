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
                         size = 40, cmpntName = "main", color = [1, 1, 0]):

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

    #configure the output of the main component
    mainCtrlOutputTransform = gf.createOutputTransformSRTNode([mainCtrlNode], mainComponentStructureNodes[1])
    offsetCtrlOutputTransforms = gf.createOutputTransformSRTNode(offsetControls, mainComponentStructureNodes[1])

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

    for ctrl in offsetCtrlInitialShapes:
        gf.setOverrideColor(ctrl, color) #set Color

        for shape in ctrl:
            cmds.delete(shape, ch=True) #delete construction History
    

    #configure the Attribute hub of the rig
    
