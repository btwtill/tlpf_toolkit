#Module import
import maya.cmds as cmds

from tlpf_toolkit.mtrx import MatrixZeroOffset

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



#Tmp Functions used for Baby Groot

def parentVineCtrlToBendy():

    sel  = cmds.ls(selection=True)

    parentGrp = cmds.listRelatives(parent = True)[0]
    print(parentGrp)

    cmds.parent(sel[0], sel[1])

    cmds.select(clear=True)
    cmds.select(sel[0]) 

    constraintNode = cmds.pickWalk(direction="down")[0]
    print(constraintNode)

    MatrixZeroOffset.createMatrixZeroOffset(constraintNode)

    cmds.parent(constraintNode, parentGrp)
    cmds.select(clear=True)

    