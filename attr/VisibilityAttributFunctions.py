#Module Import
import maya.cmds as cmds
from tlpf_toolkit.ui import common

import logging
import os

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)




#=======================================
## Add VisibilityCtrl Attribute
#=======================================
def CreateHiddenVisibilityAttributeConfigUI():
    sel = cmds.ls(selection=True)

    configWindow = cmds.window(title="VisibilityCtrlAttr", iconName="AddAttr", sizeable=True)

    cmds.rowColumnLayout(adjustableColumn=True)

    attributeName = cmds.textField()

    defaultFirst = cmds.checkBox(label="Default ON First", value=False)

    isHidden = cmds.checkBox(label="Hide Attribute", value=True)

    executeButton = cmds.button(label="Good Luck", command=lambda _: CreateHiddenVisibilityAttribute(cmds.textField(attributeName, q=True, text=True),
                                                                                                     configWindow,
                                                                                                     sel,
                                                                                                     cmds.checkBox(isHidden, q=True, value=True),
                                                                                                     cmds.checkBox(defaultFirst, q=True, value=True)))
    
    cmds.showWindow(configWindow)


def CreateHiddenVisibilityAttribute(_attributeName, _configWindow, _selection, _isHidden, _defaultFirst):
    
    #get Obejct that is gonna hold the ctrl Attribute
    visibilityCtrlObj = _selection.pop(0)

    log.info("Visibility Ctrl Object: {}".format(visibilityCtrlObj))

    #get all the objects that will be connected by the attribute 
    attributeObject = _selection

    log.info("Visibility Ctrl Object: {}".format(_selection[0] + _selection[1] + "..."))

    if _defaultFirst:
        #add the Visibilty Ctrl Attribute on the Ctrl Obj
        cmds.addAttr(visibilityCtrlObj, ln=_attributeName, at="enum", en="ON:OFF", keyable=True, hidden=_isHidden)

    elif not _defaultFirst:

        cmds.addAttr(visibilityCtrlObj, ln=_attributeName, at="enum", en="OFF:ON", keyable=True, hidden=_isHidden)

    #Connect the Attrbibute with all the Selected Objects
    for i in attributeObject:
        if _defaultFirst:

            visibilityReverseNode = cmds.rename(cmds.createNode("reverse"), _attributeName + "_" + i + "_VisibilitySwitch")
            cmds.connectAttr(visibilityCtrlObj + "." + _attributeName, visibilityReverseNode + ".inputX")
            cmds.connectAttr(visibilityReverseNode + ".outputX", i + ".visibility")
            
        elif not _defaultFirst:
            cmds.connectAttr(visibilityCtrlObj + "." + _attributeName, i + ".visibility")


    common.CloseWindow(_configWindow)
#=======================================
## Add VisibilityCtrl Attribute - END
#=======================================


#=======================================
## Lock Unlock Default Attributes
#=======================================
def lock_unlock_channels(lock=True, attrs=["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]):
    """Locks/Unlocks all default channles on selected"""
    selection = cmds.ls(selection=True)
    if selection:
        for node in selection:
            for attr in attrs:
                if lock:
                    cmds.setAttr("{}.{}".format(node, attr), lock=True, keyable=False)
                else:
                    cmds.setAttr("{}.{}".format(node, attr), lock=False, keyable=True)
#=======================================
## Lock Unlock Default Attributes - END
#=======================================


#=======================================
## Add Divider Attribute
#=======================================
def CreateAttributeDividerConfigUI():
    sel = cmds.ls(selection=True)

    configWindow = cmds.window(title="Add Attribute Divider", iconName="Add Divider", sizeable=True)

    cmds.rowColumnLayout(adjustableColumn=True)

    attributeName = cmds.textField()

    executeButton = cmds.button(label="Good Luck", command=lambda _: CreateAttributeDivider(cmds.textField(attributeName, q=True, text=True),
                                                                                                     configWindow,
                                                                                                     sel))
    
    cmds.showWindow(configWindow)

def CreateAttributeDivider(_attributeName, _configWindow, _objects):

    #Add Attribute Divider for a selection of objects
    for i in _objects:
        cmds.addAttr(i, ln=_attributeName, at="enum", en="******", keyable=True)
        cmds.setAttr(i + "." + _attributeName, cb=True)

    #close UI
    common.CloseWindow(_configWindow)

#=======================================
## Add Divider Attribute - END
#=======================================

#=======================================
## Copy Attributes to Selected
#=======================================


def CopyAttributesToSelectionConfigUI():
    #get Selection
    sel = cmds.ls(selection=True)

    #create config window
    configWindow = cmds.window(title="CopyAttributesToSelection", iconName="CopyAttr", sizeable=True)

    cmds.rowColumnLayout(adjustableColumn=True)

    #list Attributes of the first selected Item
    attributes = cmds.listAttr(sel[0])

    selectAttributeMenu = cmds.optionMenu(label="Select an Attribute")

    for i in attributes:
        cmds.menuItem(i)

    #hand selected attribute list to build Function 
    executionButton = cmds.button(label="Lets Copy", command= lambda _: CopyAttributesToSelection(sel, cmds.optionMenu(selectAttributeMenu, query=True, value=True)))

    #display config window
    cmds.showWindow(configWindow)


def addAttributeToSelectionList(_selectedAttribute):
    attribute = _selectedAttribute
    newlabel = cmds.text(label=attribute[0])


    

def CopyAttributesToSelection(_selection, _attr):

    #create all the Attributes on the second selected Item

    attrList = [_attr]

    addAttributeToSelectionList(attrList)

    log.info("Attribute List {}".format(attrList[0]))
    log.info("Selection List {}".format(_selection[0]))

    for i in attrList:
        attrTpye = cmds.attributeQuery(i, node=_selection[0], attributeType=True)

        log.info("Attribute Type {}".format(attrTpye))

        if attrTpye == "enum":
            enumList = cmds.attributeQuery(i, node=_selection[0], listEnum=True)
            isKeyable = cmds.attributeQuery(i, node=_selection[0], keyable=True)
            ishidden = cmds.attributeQuery(i, node=_selection[0], hidden=True)

            #create Copied Enum Attribute on Second Selection
            cmds.addAttr(_selection[1], ln=i, at="enum", en=enumList[0], keyable=True, hidden=ishidden)

            #connect Newly Created Attribute from second Selection to source Attribtue on first selection
            cmds.connectAttr(_selection[1] + "." + i, _selection[0] + "." + i)
        
        elif attrTpye == "float":
            
            #create Copied Float Attribute on Second Selection
            getFloatAttributeConfigAndCopy(_selection[0], _selection[1], i, "float")

        elif attrTpye == "double3":

            children = cmds.attributeQuery(i, node=_selection[0], listChildren=True)

            cmds.addAttr(_selection[1], ln=i, at="double3")

            if children:
                 
                 for j in children:
                     
                    getFloatAttributeConfigAndCopy(_selection[0], _selection[1], j, "double")

        elif attrTpye == "double":

            getFloatAttributeConfigAndCopy(_selection[0], _selection[1], i, "double")


    #close window

def getFloatAttributeConfigAndCopy(_source, _target, _attribute, _type):

    
    ishidden = cmds.attributeQuery(_attribute, node=_source, hidden=True)

    default = cmds.attributeQuery(_attribute, node=_source, listDefault=True)

    log.info("is Hidden {}".format(ishidden))
    

    maxVal = getAttributeMaximum(_attribute, _source)
    minVal = getAttributeMinimum(_attribute, _source)

    if maxVal == "No Maximum" and minVal == "No Minimum":

        cmds.addAttr(_target, ln=_attribute, at=_type, defaultValue=default[0], keyable=True, hidden=ishidden)

        #connect Newly Created Attribute from second Selection to source Attribtue on first selection
        cmds.connectAttr(_target + "." + _attribute, _source + "." + _attribute)


    elif maxVal == "No Maximum" or minVal == "No Minimum":

        if maxVal == "No Maximum":

            cmds.addAttr(_target, ln=_attribute, at=_type, minValue=minVal[0], defaultValue=default[0], keyable=True, hidden=ishidden)
            
            #connect Newly Created Attribute from second Selection to source Attribtue on first selection
            cmds.connectAttr(_target + "." + _attribute, _source + "." + _attribute)


        else:
            cmds.addAttr(_target, ln=_attribute, at=_type, maxVal=maxVal[0], defaultValue=default[0], keyable=True, hidden=ishidden)
            
            #connect Newly Created Attribute from second Selection to source Attribtue on first selection
            cmds.connectAttr(_target + "." + _attribute, _source + "." + _attribute)
    
    else:
        cmds.addAttr(_target, ln=_attribute, at=_type, maxValue=maxVal[0], minValue=minVal[0], defaultValue=default[0], keyable=True, hidden=ishidden)
        
        #connect Newly Created Attribute from second Selection to source Attribtue on first selection
        cmds.connectAttr(_target + "." + _attribute, _source + "." + _attribute)



def getAttributeMaximum(_attr, _node):
    if cmds.attributeQuery(_attr, node=_node, maxExists=True):
            maxValue = cmds.attributeQuery(_attr, node=_node, maximum=True)
            return maxValue
    else:
        return "No Maximum"



def getAttributeMinimum(_attr, _node):
    if cmds.attributeQuery(_attr, node=_node, minExists=True):
            minValue = cmds.attributeQuery(_attr, node=_node, minimum=True)
            return minValue
    else:
        return "No Minimum"
#=======================================
## Copy Attributes to Selected - END
#=======================================
