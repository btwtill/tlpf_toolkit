import maya.cmds as cmds



#connect Srt To Compose Matrix Node inputs
def connectSRTToComposeMatrixMultiSelectUI():

    sel = cmds.ls(sl=True)
    for item1, item2 in zip(sel[::2], sel[1::2]):
        connectSRTToComposeMatrix(item1, item2, rotateOrder = True)
    
def batchConnectSRTToComposeMatrixMultiSelectUI():
    input = cmds.ls(sl=True)
    inputLength = len(input)
    halfpoint = int(inputLength / 2)

    children = []
    for index in range(0, halfpoint):
        children.append(input[index])

    parents = []
    for index in range(halfpoint, inputLength):
        parents.append(input[index])
    
    for index in range(halfpoint):
        connectSRTToComposeMatrix(children[index], parents[index])

def connectSRTToComposeMatrix(srt, mtx, rotateOrder = True):
    for channel in "XYZ":
        cmds.connectAttr(f"{srt}.translate{channel}", f"{mtx}.inputTranslate{channel}")
        cmds.connectAttr(f"{srt}.rotate{channel}", f"{mtx}.inputRotate{channel}")
        cmds.connectAttr(f"{srt}.scale{channel}", f"{mtx}.inputScale{channel}")
    
    if rotateOrder:
            cmds.connectAttr(f"{srt}.rotateOrder", f"{mtx}.inputRotateOrder")

#Crate Compose Matrix Node from SRT Node

def createComposeMatrixFromSRTMultiSelectUI():

    sel = cmds.ls(sl=True)
    if type(sel) == list:
        createComposeMatrixFromSRT(sel)
    else:
        for item1 in sel:
            createComposeMatrixFromSRT(item1)

def createComposeMatrixFromSRT(items):
    for item in items:
        newCmNode = cmds.createNode("composeMatrix", name = f"{item}_Offset_cm_fNode")
        connectSRTToComposeMatrix(item, newCmNode, rotateOrder = True)