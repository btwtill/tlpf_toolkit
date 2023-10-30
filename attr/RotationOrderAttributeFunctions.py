#Module Import
import maya.cmds as cmds

def getRotationOrderIndex(order):
    switch = {
        "xyz": 0,
        "yzx": 1,
        "zxy": 2,
        "xzy": 3,
        "yxz": 4,
        "zyx": 5,
    }
    return switch.get(order, "Wrong input!!")

def updateRotationOrder(rotationOrder):

    #get index corresponding with rotation order attribute
    rotationOrderIndex = getRotationOrderIndex(rotationOrder)

    #iterate over selection and set rotation order attribute
    for i in cmds.ls(selection = True):
        cmds.setAttr(i + ".rotateOrder", rotationOrderIndex)



def setRotationOrderUI():
    #window 
    configWindow = cmds.window(title="setRotationsOrder", iconName = "RotationOrder", widthHeight=(200, 300), sizeable=True)

    #Window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Title Text
    titleText = cmds.text(label="Set RotationOrder on Selected Items", height = 30, backgroundColor = [.5, .5, .5])

    #Space Divider
    cmds.text(label="", height=10)

    rotationOrderList = ["xyz", "yzx", "zxy", "xzy", "yxz", "zyx"]

    #option menu to select the Rotationorder
    rotationOrderOptionsWindow = cmds.optionMenu(label="RotationOrder")

    for item in rotationOrderList:
        cmds.menuItem(label = item)

    #execution Button to set Rotation order
    setRotationOrderButton = cmds.button(label="Set RotationOrder", command= lambda _: updateRotationOrder(cmds.optionMenu(rotationOrderOptionsWindow, query=True, value=True)))

    #show window 
    cmds.showWindow(configWindow)

    