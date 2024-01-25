#Module import
import maya.cmds as cmds
import maya.api.OpenMaya as om

from tlpf_toolkit.mtrx import MatrixZeroOffset

__startIndex__ = {0:0, 
                  1:4,
                  2:8,
                  3:12}


#=======================================
## String Filter Function
#=======================================
def filter_strings(AttributeList, filterAttributes):
    filtered_strings = []
    
    for main_Attribute in AttributeList:
        for filter_string in filterAttributes:
            if filter_string in main_Attribute:
                filtered_strings.append(main_Attribute)
                break
    return filtered_strings
#=======================================
## String Filter Function - END
#=======================================


#=======================================
## duplicate List and parent to world Function
#=======================================
def duplicateSelection(selectionArray):
        dupList = []
        for i in selectionArray:
            newJoint = cmds.duplicate(i, parentOnly=True)
            try:
                cmds.parent(newJoint, world=True)
            except:
                print("already world Parent")
            dupList.append(newJoint)
            
        return dupList
#=======================================
## duplicate List - END
#=======================================

#=======================================
## Remove dup 1 in Name and Prefix with 
## specified name Function
#=======================================
def removeOneAndPrefixName(targetList, name):
            renamedList = []
            for i in range(len(targetList)):
                listElement = "".join(targetList[i])
                newName = listElement.replace("1", "")
                newName = name + newName
                renamedList.append(newName)
                cmds.rename(targetList[i], newName)
            return renamedList
#=======================================
## Remove dup and Prefix Function - END
#=======================================

#=======================================
## Reparent target Object into Hirarchy
#=======================================
def reparenting(targetArray):
            for i in range(len(targetArray)):
                if i != (len(targetArray) - 1):
                    cmds.parent(targetArray[i + 1], targetArray[i])
#=======================================
## Reparenting Function - END
#=======================================


#=======================================
## Convert Vertecie List to Locators
#=======================================


def convertVerteciePositionsToLacators(verteciePos):
      
    locators = list()

    for vert in verteciePos:
        pos = cmds.xform(vert, query = True, worldSpace = True, t = True)
        loc = cmds.spaceLocator()[0]
        cmds.xform(loc, t = pos, worldSpace=True)
        locators.append(loc)

    return locators

#=======================================
## Convert Vertecie List to Locators - END
#=======================================



#=======================================
## Set SelectedNode First Input
#=======================================

def setNodeInputToOne():
     selectedNode = cmds.ls(selection=True)[0]

     cmds.setAttr(f"{selectedNode}.input[0]", 1)

def setNodeInputToZero():
     selectedNode = cmds.ls(selection=True)[0]

     cmds.setAttr(f"{selectedNode}.input[0]", 0)

#=======================================
## Set SelectedNode First Input - END
#=======================================

#=======================================
## clean Transform channels Functions
#=======================================

def cleanTranslation(target):
    state = True
    for i in "XYZ":
        if state:
            print(cmds.getAttr(f"{target}.translate{i}"))
            if cmds.getAttr(f"{target}.translate{i}") == 0:
                state = True
            else:
                state = False
        else:
            return False
    return True

def cleanRotation(target):
    state = True
    for i in "XYZ":
        if state:
            print(cmds.getAttr(f"{target}.rotate{i}"))
            if cmds.getAttr(f"{target}.translate{i}") == 0:
                state = True
            else:
                state = False
        else:
            return False
    return True

#=======================================
## clean Transform channels Functions - END
#=======================================

#=======================================
## Select None Zero Transform Nodes 
#=======================================

def selectNoneZeroTransforms():
    targets = cmds.ls(sl=True)
    cmds.select(clear=True)
    
    for i in targets:
        if not cleanTranslation(i) and not cleanRotation(i):
            cmds.select(i, add = True)
        else:
            print(f"{i}: No Traslation")

#=======================================
## Select None Zero Transform Nodes - END
#=======================================

#=======================================
## Multi Parent
#=======================================

def multiParent():
    sel = cmds.ls(sl = True)
    
    for item1, item2 in zip(sel[::2], sel[1::2]):
        cmds.parent(item1, item2)

#=======================================
## Multi Parent - END
#=======================================
        
#=======================================
## Set Display Type
#=======================================

def setSelectionDisplayTypeNormal():
    for i in cmds.ls(sl=True):
        cmds.setAttr(f"{i}.overrideDisplayType", 0)

#=======================================
## Set Display Type - END
#=======================================
        
#=======================================
## Clear Transforms 
#=======================================
        
def clearTransforms(items):
     for item in items:
          for channel in "XYZ":
               cmds.setAttr(f"{item}.translate{channel}", 0)
               cmds.setAttr(f"{item}.rotate{channel}", 0)
               cmds.setAttr(f"{item}.scale{channel}", 1)

#=======================================
## Clear Transforms - End
#=======================================
               

def clearTransformsSpecific(items, t = True, r = True, s = True):
     for item in items:
          for channel in "XYZ":
               if t:
                cmds.setAttr(f"{item}.translate{channel}", 0)
               if r:
                cmds.setAttr(f"{item}.rotate{channel}", 0)
               if s: 
                cmds.setAttr(f"{item}.scale{channel}", 1)


def getMatrixTranslation(inputMatrix):
    resultTranslation = getMatrixRow(3, inputMatrix)
    return resultTranslation


def getMatrixRow(row = 0, inMat =None):
    outVec = om.MVector(inMat[__startIndex__[row]],
                        inMat[__startIndex__[row]+ 1],
                        inMat[__startIndex__[row]+ 2])
    return outVec

def getOffsetSrt(source, target):
    
    localCoord = om.MMatrix(cmds.getAttr(f"{source}.worldInverseMatrix[0]"))
    WorldMatrix = om.MMatrix(cmds.getAttr(f"{target}.worldMatrix[0]"))

    resultMatrix = localCoord * WorldMatrix

    return resultMatrix