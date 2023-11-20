from maya import cmds



#=======================================
## Snap Selection to Closest Curve Point
#=======================================

def snapSelectionToClosestCurvePoint():
    selection = cmds.ls(selection=True)

    selCurve = selection.pop()

    npcNodes = list()
    cacheTransforms = list()
    for i in selection:
        cacheTransform = cmds.createNode("transform", name = f"{i}_cacheTransform")
        outPutTransform = cmds.createNode("transform", name = f"{i}_outoutTransform")
        
        currentPos = cmds.xform(i, query = True, ws = True, m = True)
        cmds.xform(cacheTransform, m = currentPos, ws = True)
        
        npciNode = cmds.createNode("nearestPointOnCurve", name = f"{selCurve}_npciTmp")
        cmds.connectAttr(f"{selCurve}.worldSpace[0]", f"{npciNode}.inputCurve")
        for n in "XYZ":
            cmds.connectAttr(f"{cacheTransform}.translate{n}", f"{npciNode}.inPosition{n}")
            cmds.connectAttr(f"{npciNode}.position{n}", f"{outPutTransform}.translate{n}")
        
        outputPosition = cmds.xform(outPutTransform, query = True, ws = True, m = True)
        cmds.xform(i, m = outputPosition, ws=True)
        
        npcNodes.append(npciNode)
        cacheTransforms.append(cacheTransform)
        cacheTransforms.append(outPutTransform)
        
    cmds.delete(npcNodes)
    cmds.delete(cacheTransforms)

#=======================================
## Snap Selection to Closest Curve Point - END
#=======================================

#=======================================
## Create Linear Curve from Selection
#=======================================

def createLinearCurveFromSelectionConfig():
    selection = cmds.ls(flatten = True, os = True)
    createLinearCurveFromSelection(selection)

def createLinearCurveFromSelection(_objSelection, _crvName = "curve"):

    #define Curve Point Positions and Knots
    pointPositions = []
    knots = []

    #iterate over selection
    for i in range(len(_objSelection)):

        #get woldspace point position and store it in the point position list
        newPos = cmds.xform(_objSelection[i], q=True, ws=True, t=True)
        pointPositions.append(newPos)

        #add Knot into Knot list
        knots.append(i)
    
    print(_crvName)
    newCurve = cmds.curve(d=1, p=pointPositions, k=knots, n = _crvName)
    print(newCurve)
    cmds.rename(cmds.listRelatives(newCurve, shapes=True), _crvName + "Shape")

    return newCurve, knots

#=======================================
## Create Linear Curve from Selection -END
#=======================================