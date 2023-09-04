#Module import
import maya.cmds as cmds



#=======================================
## Simple Pole Vector Function
#=======================================
def createSimplePoleVector():
    
    sel = cmds.ls(selection=True)
    
    if len(sel) == 2:
        
        ik_handle = sel[0]
        pv_ctrl = sel[1]
    
        start_joint = cmds.ikHandle(ik_handle, query=True, startJoint=True)
        
        mid_joint = cmds.listRelatives(start_joint, children=True, type='joint')[0]
        
        cmds.delete(cmds.pointConstraint(start_joint, ik_handle, pv_ctrl))
        
        cmds.delete(cmds.aimConstraint(mid_joint, pv_ctrl, aim=[0,0,-1], u= [-1, 0, 0], wuo=start_joint, wut='object'))
        
        pv_pos = cmds.xform(pv_ctrl, q=True, ws=True, t=True)
        mid_pos = cmds.xform(mid_joint, q=True, ws=True, t=True)
        
        pv_dist = (pv_pos[0] - mid_pos[0], pv_pos[1] - mid_pos[1], pv_pos[2] - mid_pos[2])
        
        cmds.xform(pv_ctrl, t=(mid_pos[0] - pv_dist[0] * 1.2, mid_pos[1] - pv_dist[1] * 1.2, mid_pos[2] - pv_dist[2]* 1.2))
        
        cmds.poleVectorConstraint(pv_ctrl, ik_handle)

        pv_off = cmds.duplicate(pv_ctrl, po=True, name=pv_ctrl + "_grp")
        cmds.parent(pv_ctrl, pv_off)

    else:
        print("Please Select IF Hanlde and then the PV Ctrl")
    
    return True
#=======================================
## Simple Pole Vector Function - END
#=======================================

#=======================================
## Connection Line Function
#=======================================
def createPoleVectorLine():
    try:
            
        sel = cmds.ls(selection=True)

        qshape = cmds.curve(p=[(0,0,0), (0,0,0)], d=1)


        qshape = cmds.rename(qshape, sel[0] + '_q')
        cmds.select(qshape)

        selectionShape = cmds.pickWalk(direction="Down")


        cmds.parent(selectionShape, sel[0], shape=True, relative=True)

        multmatrix = cmds.createNode('multMatrix')
        decomposeMatrix = cmds.createNode('decomposeMatrix')


        cmds.connectAttr(multmatrix + '.matrixSum', decomposeMatrix + '.inputMatrix')

        cmds.connectAttr(sel[1] + '.worldMatrix', multmatrix + '.matrixIn[0]')
        cmds.connectAttr(sel[0] + '.worldInverseMatrix[0]', multmatrix + '.matrixIn[1]')


        cmds.connectAttr(decomposeMatrix + '.outputTranslateX', selectionShape[0] + '.controlPoints[0].xValue')
        cmds.connectAttr(decomposeMatrix + '.outputTranslateY', selectionShape[0] + '.controlPoints[0].yValue')
        cmds.connectAttr(decomposeMatrix + '.outputTranslateZ', selectionShape[0] + '.controlPoints[0].zValue')

        cmds.delete(qshape)
    except:
        print("time to investigate!!")
#=======================================
## ConnectionLine Function - END
#=======================================