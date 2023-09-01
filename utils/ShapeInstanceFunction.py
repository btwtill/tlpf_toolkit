#Module import
import maya.cmds as mc



#=======================================
##ShapeNode Instance
#=======================================


def shapeParentInstance():

    selectionList = mc.ls(selection=True)
    instanceNode = ""
    for i in range(len(selectionList)):
        print(selectionList[i])
        if i == 0:
            instanceNode = selectionList[i]
            print(instanceNode)
        else:
            mc.parent(instanceNode, selectionList[i], add=True, shape=True)


#=======================================
##ShapeNode Instance - END
#=======================================