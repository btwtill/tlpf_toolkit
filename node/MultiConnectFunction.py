#Module Import
import maya.cmds as cmds
from tlpf_toolkit.utils import GeneralFunctions
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)



#=======================================
## 1-N MultiConnect Function
#=======================================
####Execute the Attribute Connections
def ConnectOneToNNodes(_outputNodeAttribute, _inputNodeAttribute):

    _targetList = cmds.ls(selection=True)

    _outputNode = _targetList.pop(0)

    #get the string for the output Attribute on the output Node
    outputName = _outputNode + "." + _outputNodeAttribute
    
    #loop over the selected Input nodes and connect the selected output to the input sockets
    for i in _targetList:
        cmds.connectAttr(outputName, i + "." + _inputNodeAttribute)



#Configuration Interface to let the user decide what Output Attribute should be used to connect to all the selected Input Nodes
def MultiConnectOneToNConfigurationInterfaceFiltered():  

    #get selection
    sel = cmds.ls(selection=True)

    # Filter Attributes
    filterAttributes = ["translate", "rotate", "scale", "Translate", "Rotate", "Scale", "default", "outFloat"]

    #seperate out the output node and input nodes into different lists
    firstElementAttributes = cmds.listAttr(sel[0])
    secondElementAttribtues = cmds.listAttr(sel[1])

    #filter the first attriubte list
    firstElementAttributes = GeneralFunctions.filter_strings(firstElementAttributes, filterAttributes)
    secondElementAttribtues = GeneralFunctions.filter_strings(secondElementAttribtues, filterAttributes)

    #safe the output Node into a seperate Variable
    OutputNode = sel.pop(0)
    InputNodes = sel[0]


    #basic Window creation
    configWindow = cmds.window(title="1XN_MultiConnector", iconName='1xN', widthHeight=(200, 55), sizeable=True)

    #Window Layout
    cmds.rowColumnLayout( adjustableColumn=True)

    #create the Options menues and store them in a variable
    OutputNodeOptionMenu = cmds.optionMenu(label="Output node")

    for item in firstElementAttributes:
        cmds.menuItem(label=item)

    InputNodesOptionMenu = cmds.optionMenu(label="Input Nodes")

    for item in secondElementAttribtues:
        cmds.menuItem(label=item)
        


    #create visuallizers of what nodes are selected
    cmds.text(OutputNode, annotation="Output Node", height=20, backgroundColor = [0.01, 0.01, 0.01] )

    cmds.text(InputNodes, annotation="Input Nodes", height=20, backgroundColor = [0.3, 0.3, 0.3] )

    #execution button to connect the inputs and outputs
    cmds.button(label='Connect Attributes', command=lambda _: ConnectOneToNNodes(cmds.optionMenu(OutputNodeOptionMenu, query=True, value=True), cmds.optionMenu(InputNodesOptionMenu, query=True, value=True)))


    #Display The window
    cmds.showWindow(configWindow)


    #Configuration Interface to let the user decide what Output Attribute should be used to connect to all the selected Input Nodes
def MultiConnectOneToNConfigurationInterfaceAll():  

    #get selection
    sel = cmds.ls(selection=True)

    #seperate out the output node and input nodes into different lists
    firstElementAttributes = cmds.listAttr(sel[0])
    secondElementAttribtues = cmds.listAttr(sel[1])

    #safe the output Node into a seperate Variable
    OutputNode = sel.pop(0)
    InputNodes = sel[0]


    #basic Window creation
    configWindow = cmds.window(title="1XN_MultiConnector", iconName='1xN', widthHeight=(200, 55), sizeable=True)

    #Window Layout
    cmds.rowColumnLayout( adjustableColumn=True)

    #create the Options menues and store them in a variable
    OutputNodeOptionMenu = cmds.optionMenu(label="Output node")

    for item in firstElementAttributes:
        cmds.menuItem(label=item)

    InputNodesOptionMenu = cmds.optionMenu(label="Input Nodes")

    for item in secondElementAttribtues:
        cmds.menuItem(label=item)
        


    #create visuallizers of what nodes are selected
    cmds.text(OutputNode, annotation="Output Node", height=20, backgroundColor = [0.01, 0.01, 0.01] )

    cmds.text(InputNodes, annotation="Input Nodes", height=20, backgroundColor = [0.3, 0.3, 0.3] )

    #execution button to connect the inputs and outputs
    cmds.button(label='Connect Attributes', command=lambda _: ConnectOneToNNodes(cmds.optionMenu(OutputNodeOptionMenu, query=True, value=True), cmds.optionMenu(InputNodesOptionMenu, query=True, value=True)))


    #Display The window
    cmds.showWindow(configWindow)
#=======================================
## 1-N MultiConnect Function - END
#=======================================




    

#=======================================
## mxn MultiConnect Function
#=======================================

def ConnectMxNAttributes(_outputList, _targetList, _outputAttribute, _targetAttribute):
    for i in range(len(_outputList)):
        cmds.connectAttr(_outputList[i] + "." + _outputAttribute, _targetList[i] + "." + _targetAttribute)





def MultiConnectMToNConfigurationInterfaceFiltered():  

    #selection
    sel  = cmds.ls(selection=True)

    #empty list to later receive the seperated selection list into main and target Objects
    mainList = []
    targetList = []
    
    #Check if the Selected Objects list length is dividable by 2
    isDividable = (len(sel) % 2) == 0
    
    if isDividable:
        half = len(sel) / 2

        #append the individual object to there list
        for i in range(len(sel)):
            if i < half:
                mainList.append(sel[i])
            else:
                targetList.append(sel[i])

        # Filter Attributes
        filterAttributes = ["translate", "rotate", "scale", "Translate", "Rotate", "Scale", "default", "outFloat"]

        #seperate out the output node and input nodes into different lists
        firstElementAttributes = cmds.listAttr(mainList[0])
        secondElementAttribtues = cmds.listAttr(targetList[0])

        #filter the first attriubte list
        firstElementAttributes = GeneralFunctions.filter_strings(firstElementAttributes, filterAttributes)
        secondElementAttribtues = GeneralFunctions.filter_strings(secondElementAttribtues, filterAttributes)

        #safe the output Node into a seperate Variable
        #OutputNode = sel.pop(0)
        #InputNodes = sel[0]


        #basic Window creation
        configWindow = cmds.window(title="MxN_MultiConnector", iconName='nxm', widthHeight=(200, 55), sizeable=True)

        #Window Layout
        cmds.rowColumnLayout( adjustableColumn=True)

        #create the Options menues and store them in a variable
        OutputNodeOptionMenu = cmds.optionMenu(label="Output nodes")

        for item in firstElementAttributes:
            cmds.menuItem(label=item)

        TargetNodesOptionMenu = cmds.optionMenu(label="Target Nodes")

        for item in secondElementAttribtues:
            cmds.menuItem(label=item)
            


        #create visuallizers of what nodes are selected
        for i in mainList:
            cmds.text(i, annotation = "Output Nodes", height=20, backgroundColor = [0.5, 0.5, 0] )
    
        cmds.text(label="", height=30, backgroundColor= [0,0,0])
        
        for i in targetList:    
            cmds.text(i, annotation="Target Nodes", height=20, backgroundColor = [0, 0.5, 0.5] )

        #execution button to connect the inputs and outputs
        cmds.button(label='Connect Attributes', command=lambda _: ConnectMxNAttributes(mainList, targetList, cmds.optionMenu(OutputNodeOptionMenu, query=True, value=True), cmds.optionMenu(TargetNodesOptionMenu, query=True, value=True)))


        #Display The window
        cmds.showWindow(configWindow)
    else:
        log.error("List is not dividable by 2")
        raise


def MultiConnectMToNConfigurationInterfaceAll():  

    #selection
    sel  = cmds.ls(selection=True)

    #empty list to later receive the seperated selection list into main and target Objects
    mainList = []
    targetList = []
    
    #Check if the Selected Objects list length is dividable by 2
    isDividable = (len(sel) % 2) == 0
    
    if isDividable:
        half = len(sel) / 2

        #append the individual object to there list
        for i in range(len(sel)):
            if i < half:
                mainList.append(sel[i])
            else:
                targetList.append(sel[i])

        #seperate out the output node and input nodes into different lists
        firstElementAttributes = cmds.listAttr(mainList[0])
        secondElementAttribtues = cmds.listAttr(targetList[0])

        #safe the output Node into a seperate Variable
        #OutputNode = sel.pop(0)
        #InputNodes = sel[0]


        #basic Window creation
        configWindow = cmds.window(title="MxN_MultiConnector", iconName='nxm', widthHeight=(200, 55), sizeable=True)

        #Window Layout
        cmds.rowColumnLayout( adjustableColumn=True)

        #create the Options menues and store them in a variable
        OutputNodeOptionMenu = cmds.optionMenu(label="Output nodes")

        for item in firstElementAttributes:
            cmds.menuItem(label=item)

        TargetNodesOptionMenu = cmds.optionMenu(label="Target Nodes")

        for item in secondElementAttribtues:
            cmds.menuItem(label=item)
            


        #create visuallizers of what nodes are selected
        for i in mainList:
            cmds.text(i, annotation = "Output Nodes", height=20, backgroundColor = [0.5, 0.5, 0] )
    
        cmds.text(label="", height=30, backgroundColor= [0,0,0])
        
        for i in targetList:    
            cmds.text(i, annotation="Target Nodes", height=20, backgroundColor = [0, 0.5, 0.5] )

        #execution button to connect the inputs and outputs
        cmds.button(label='Connect Attributes', command=lambda _: ConnectMxNAttributes(mainList, targetList, cmds.optionMenu(OutputNodeOptionMenu, query=True, value=True), cmds.optionMenu(TargetNodesOptionMenu, query=True, value=True)))


        #Display The window
        cmds.showWindow(configWindow)
    else:
        log.error("List is not dividable by 2")
        raise
#=======================================
## nxm MultiConnect Function - END
#=======================================