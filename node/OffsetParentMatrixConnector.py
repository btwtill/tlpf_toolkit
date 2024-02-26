import maya.cmds as cmds


#batch Connection World Matrix -> Offset Parent Matrix
def connectOffsetParentMatrixBatchUI():
    input = cmds.ls(sl=True)
    inputLength = len(input)
    halfpoint = int(inputLength / 2)


    for inte in range(0, halfpoint):
        print(inte)
    
    for inte in range(halfpoint, inputLength):
        print(inte)

    children = []
    for index in range(0, halfpoint):
        children.append(input[index])

    parents = []
    for index in range(halfpoint, inputLength):
        parents.append(input[index])
    
    connectOffsetParentMatrixBatch(children, parents)

def connectOffsetParentMatrixBatch(children, parents):
    for i, child in enumerate(children):
        cmds.connectAttr(f"{parents[i]}.worldMatrix[0]",f"{child}.offsetParentMatrix")