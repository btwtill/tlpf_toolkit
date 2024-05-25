import maya.cmds as cmds
from tlpf_toolkit.autoLib import autolibGlobalVariables as globalVar
from tlpf_toolkit.autoLib import generalFunctions as gf

#compose character Main component
def composeMainComponent(parent, numOfMainControlOffsets = 1, 
                         mainCtrlShapeName = "circle", offsetCtrlShapeName = "circle", 
                         size = 40, name = "main"):

    #create outliner structure
    mainComponentTopNode, mainComponentStructureNodes = gf.createRigComponent(name, parent)

    #create god node transform
    godNodeTransform = cmds.createNode("transform", name = f"{globalVar.CENTERDECLARATION}_{name}_godNode_{globalVar.NODEUSAGETYPETRANSFORM}")
    cmds.parent(godNodeTransform, mainComponentStructureNodes[2])
    gf.untouchableTransform([godNodeTransform])


    #create main Controls
    mainCtrlNode = cmds.circle(name = f"{globalVar.CENTERDECLARATION}_{name}_global_{globalVar.NODEUSAGETYPECONTROL}", radius = size, nr = [0,1,0])
    cmds.parent(mainCtrlNode, godNodeTransform)

    #create main Offset Controls
    offsetControls = []
    for offCtrl in range(numOfMainControlOffsets):

        #parent first offset ctrl to main ctrl
        if len(offsetControls) == 0:
            newOffsetCtrl = cmds.circle(name = f"{globalVar.CENTERDECLARATION}_{name}_globalOffset{offCtrl}_{globalVar.NODEUSAGETYPECONTROL}", 
                                        radius = size - ((offCtrl + 1)*4), nr = [0,1,0])
            cmds.parent(newOffsetCtrl, mainCtrlNode)
            offsetControls.append(newOffsetCtrl)
        #parent all next offset ctrls to the one before themselves
        else:
            newOffsetCtrl = cmds.circle(name = f"{globalVar.CENTERDECLARATION}_{name}_globalOffset{offCtrl}_{globalVar.NODEUSAGETYPECONTROL}", 
                                        radius = size - (offCtrl*2), nr = [0,1,0])
            cmds.parent(newOffsetCtrl, offsetControls[offCtrl - 1])
            offsetControls.append(newOffsetCtrl)
            
