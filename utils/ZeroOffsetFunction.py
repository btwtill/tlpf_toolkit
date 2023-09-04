#Module Import
import maya.cmds as cmds


#=========================================
## Sam Zero - Credit to Alexander Samouridis 
## for providing the base of this script
#=========================================
def insertNodeBefore(sfx = '_zro', alignToParent = False, loc = False, replace = '_ctl'):
    nodes = cmds.ls(sl = 1)

    isRoot = False
    cnNodes = []
    for node in nodes:
        zName = node
        # if we add a zero to a ctl, kill the suffix
        if replace in node:
            zName = node.replace(replace, '')

        # create in between node
        if loc:
            cnNode = cmds.spaceLocator( n = zName + sfx)[0]
        else:
            cnNode = cmds.createNode('transform', n = zName + sfx)

        # get parent
        nodeParent = cmds.listRelatives(node, p = True)


        if nodeParent == None:
            if alignToParent:
                print ('Do Nothing, world parented')
            else:
                cmds.matchTransform(cnNode, node)
        else:
            if alignToParent:
                cmds.matchTransform(cnNode, nodeParent)
            else:
                cmds.matchTransform(cnNode, node)
            cmds.parent(cnNode, nodeParent)

        cmds.parent(node, cnNode)
        cnNodes.append(cnNode)

        # check if we have are zeroeing a joint (because if so we need to zero out all Orients)
        if not alignToParent:
            if cmds.objectType(node, isType = 'joint'):
                for attr in ('.rx', '.ry', '.rz', '.jointOrientX', '.jointOrientY', '.jointOrientZ'):
                    cmds.setAttr(node+attr, 0)

    return cnNodes
#=======================================
## Sam Zero - End
#=======================================


#=======================================
## Tim Colement Zero Method
#=======================================
def TimZeroUserConfig():

    #basic Window creation
    configWindow = cmds.window(title="TimZeroConfig", iconName='TimZero', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.rowColumnLayout( adjustableColumn=True )
    
    #Label
    cmds.text( label='Offset Nodes' )
    
    #Input Field Sotring the Stirng value
    grp = cmds.checkBox(label="_grp", value=True)
    offs = cmds.checkBox(label="_off")
    drv = cmds.checkBox(label="_drv")
    
    #Building the switch execution button
    cmds.button( label='create Offset Nodes', command=lambda _: TimZero(cmds.ls(selection=True), assembleOffsetList(cmds.checkBox(grp, query=True, value=True), 
                                                                                                                cmds.checkBox(offs, query=True, value=True),
                                                                                                                cmds.checkBox(drv, query=True, value=True))))

    #Display The window
    cmds.showWindow(configWindow)

def assembleOffsetList(_grp, _offs, _drv):
    offsetList = []

    if _grp:
        offsetList.append('_grp')
    if _offs:
        offsetList.append("_off")
    if _drv:
        offsetList.append("_drv")
    print(offsetList)
    return offsetList


def TimZero(transform_list, add_transforms):
    for tfm in transform_list:
        if cmds.nodeType(tfm) == 'transform':
            created_tfms = list()
            for i in range(0, len(add_transforms)):
                add_tfm = cmds.duplicate(tfm, po=True, name= tfm + add_transforms[i])
                created_tfms.append(add_tfm)
                if i:
                    cmds.parent(add_tfm, created_tfms[i - 1])
            cmds.parent(tfm, created_tfms[-1])
                    
        else:
            print ('No not a tranform')

#=======================================
## Tim COlement Zero Method - END
#=======================================