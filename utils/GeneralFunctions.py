#Module import
import maya.cmds as cmds



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