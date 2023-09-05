#Module Import 
import maya.cmds as cmds




#=======================================
## Commonly UsedUI Functions
#=======================================
def buildUserInputGrp(buttonLabel, displayLabelText, displayLabelHeight):
    cmds.text(label="", height=10, backgroundColor=[0.0,0.0,0.0])
    cmds.button(label=buttonLabel, height=40, command=lambda _: updateLabel(labelname, getFirstUserSelection()))
    labelname = cmds.text(label=displayLabelText, height=displayLabelHeight, backgroundColor=[0.6, 0.1, 0.1])
    return labelname

def getFirstUserSelection():
    sel = cmds.ls(selection=True)
    return sel[0]

def updateLabel(_label, _newLabelText):
    rgbColor = [0.3, 0.8, 0.2]
    cmds.text(_label, edit=True, label=_newLabelText, backgroundColor=rgbColor)
#=======================================
## Commonly UsedUI Functions - END
#=======================================


#=======================================
## Delete Given UI Window
#=======================================
def CloseWindow(_windowName):
    cmds.deleteUI(_windowName, window=True)
#=======================================
## Delete Given UI Window - END
#=======================================