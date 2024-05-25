import maya.cmds as cmds
import generalFunctions as gf

#compose character Main component
def composeMainComponent(parent, numOfMainControls = 1, 
                         mainCtrlShapeName = "circle", offsetCtrlShapeName = "circle", 
                         size = 40, name = "main"):
    #define side Prefix
    side = "M"
    nodeUsageTypeTransform = "srt"
    nodeUsageTypeControl = "ctrl"

    #create outliner structure
    mainComponentTopNode, mainComponentStructureNodes = gf.createRigComponent(name, parent)

    #create god node transform
    godNodeTransform = cmds.createNode("transform", name = f"{side}_{name}_godNode_{nodeUsageTypeTransform}")
    cmds.parent(godNodeTransform, mainComponentStructureNodes[2])
    gf.untouchableTransform([godNodeTransform])


    #create main Controls
    mainCtrlNode = cmds.circle(name = f"{side}_{name}_global_{nodeUsageTypeControl}")
