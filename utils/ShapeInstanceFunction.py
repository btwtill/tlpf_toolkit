#Module import
import maya.cmds as cmds



#=======================================
##ShapeNode Instance
#=======================================


def shapeParentInstance():

    selectionList = cmds.ls(selection=True)
    instanceNode = ""
    for i in range(len(selectionList)):
        #print(selectionList[i])
        if i == 0:
            instanceNode = selectionList[i]
            #print(instanceNode)
        else:
            cmds.parent(instanceNode, selectionList[i], add=True, shape=True)


#=======================================
##ShapeNode Instance - END
#=======================================