#Module Import
import maya.cmds as cmds
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)



#=======================================
## Connect SRT Funciton
#=======================================
def ConnectSRT():
    try:
        sel = cmds.ls(selection=True)
        if sel:
            attributes = ["scale", "rotate", "translate"]
            for i in attributes:
                for j in "XYZ":
                    cmds.connectAttr(sel[0] + "." + i + j, sel[1] + "." + i + j)
        else:
            log.info("No Objects Selected")
    except:
        log.error("Unable to perform desired Operation")
        raise
#=======================================
## Connect SRT Funciton - END
#=======================================



#=======================================
## Connect Scale Funciton
#=======================================
def ConnectScale():
    try:
        sel = cmds.ls(selection=True)
        if sel:
            for i in "XYZ":
                cmds.connectAttr(sel[0] + ".scale" + i, sel[1] + ".scale" + i)
        else:
            log.info("No Objects Selected")
    except:
        log.error("Unable to perform desired Operation")
        raise
#=======================================
## Connect Scale Funciton - END
#=======================================



#=======================================
## Connect Rotation Funciton
#=======================================
def ConnectRotate():
    sel = cmds.ls(selection=True)
    
    for i in "XYZ":
        cmds.connectAttr(sel[0] + ".rotate" + i, sel[1] + ".rotate" + i)
#=======================================
## Connect Rotation Funciton - END
#=======================================



#=======================================
## Connect Translate Funciton
#=======================================
def ConnectTranslate():
    try:
        
        sel = cmds.ls(selection=True)
        if sel:

            for i in "XYZ":
                cmds.connectAttr(sel[0] + ".translate" + i, sel[1] + ".translate" + i)
            else:
                log.info("No Objects Selected")
    except:
        log.error("Unable to perform desired Operation")
        raise
#=======================================
## Connect Translate Funciton - END
#=======================================