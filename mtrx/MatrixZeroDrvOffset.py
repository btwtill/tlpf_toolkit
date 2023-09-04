#Module Import
import maya.cmds as cmds




#=======================================
## Matrix Node Zero Drv Offset
#=======================================
def createMatrixDrvOffset():
    sel = cmds.ls(selection=True)


    try:
        zroName = sel[0].replace('_zro', '_drv')
    except:
        print(sel[0])

    cmds.disconnectAttr(sel[0] + '.outputMatrix', sel[1] + '.matrixIn[0]')

    newMultMatrix = cmds.createNode('multMatrix')

    driverMatrix = cmds.createNode('composeMatrix', name= zroName)

    cmds.connectAttr(newMultMatrix + '.matrixSum', sel[1] + '.matrixIn[0]')


    cmds.connectAttr(driverMatrix + '.outputMatrix', newMultMatrix + '.matrixIn[0]')
    cmds.connectAttr(sel[0] + '.outputMatrix', newMultMatrix + '.matrixIn[1]')
#=======================================
## Matrix Node Zero Drv Offset - END
#=======================================