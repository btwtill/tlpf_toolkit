#Module Import
import maya.cmds as cmds



#=======================================
## Multi ParentConstraint Function 
#=======================================
#Functino to Parent Constaraint Multiple Objects with each Other
def MultiParentConstraintConfig():
    configWindow = cmds.window(title="ParentConstraintConfig", sizeable=True, iconName="MultiParent", widthHeight=(200, 55))
    
    cmds.rowColumnLayout(adjustableColumn=True)

    cmds.text(label="Search for master suffix")

    firstItemSufffix = cmds.textField()

    cmds.text(label="Search for target suffix")

    seconItemSufffix = cmds.textField()

    cmds.button(label="Parent", command= lambda _: MultiParentConstraint(cmds.textField(firstItemSufffix, query=True, text=True), cmds.textField(seconItemSufffix, query=True, text=True)))

    cmds.showWindow(configWindow)

def MultiParentConstraint(_firstSuffix, _secondSuffix):
    sel = cmds.ls(selection=True)
    try:
        constrainingList = _firstSuffix
        targetList = _secondSuffix

        filteredFirstList = [s for s in sel if constrainingList in s]
        filteredSecondList = [s for s in sel if targetList in s]

        if len(filteredFirstList) == len(filteredSecondList):

            for i in range(len(filteredFirstList)):
                cmds.parentConstraint(filteredFirstList[i], filteredSecondList[i])



    except:
        print("Nope!!")

#=======================================
## Multi ParentConstraint Function - END
#=======================================





#=======================================
## Multi OrientConstraint Function 
#=======================================
def MultiOrientConstraintConfig():
    configWindow = cmds.window(title="OrientConstraintConfig", sizeable=True, iconName="MultiOrient", widthHeight=(200, 55))
    
    cmds.rowColumnLayout(adjustableColumn=True)

    cmds.text(label="Search for master suffix")

    firstItemSufffix = cmds.textField()

    cmds.text(label="Search for target suffix")

    seconItemSufffix = cmds.textField()

    cmds.button(label="Orient", command= lambda _: MultiOrientConstraint(cmds.textField(firstItemSufffix, query=True, text=True), cmds.textField(seconItemSufffix, query=True, text=True)))

    cmds.showWindow(configWindow)


#Functino to Orient Constaraint Multiple Objects with each Other
def MultiOrientConstraint(_firstSuffix, _secondSuffix):
    sel = cmds.ls(selection=True)
    try:
        constrainingList = _firstSuffix
        targetList = _secondSuffix

        filteredFirstList = [s for s in sel if constrainingList in s]
        filteredSecondList = [s for s in sel if targetList in s]

        if len(filteredFirstList) == len(filteredSecondList):

            for i in range(len(filteredFirstList)):
                cmds.orientConstraint(filteredFirstList[i], filteredSecondList[i])



    except:
        print("Nope!!")
#=======================================
## Multi OrientConstraint Function - END
#=======================================



#=======================================
## Multi ScaleConstraint Function 
#=======================================
def MultiScaleConstraintConfig():
    configWindow = cmds.window(title="ScaleConstraintConfig", sizeable=True, iconName="MultiScale", widthHeight=(200, 55))
    
    cmds.rowColumnLayout(adjustableColumn=True)

    cmds.text(label="Search for master suffix")

    firstItemSufffix = cmds.textField()

    cmds.text(label="Search for target suffix")

    seconItemSufffix = cmds.textField()

    cmds.button(label="Scale", command= lambda _: MultiScaleConstraint(cmds.textField(firstItemSufffix, query=True, text=True), cmds.textField(seconItemSufffix, query=True, text=True)))

    cmds.showWindow(configWindow)


#Functino to Scale Constaraint Multiple Objects with each Other
def MultiScaleConstraint(_firstSuffix, _secondSuffix):
    sel = cmds.ls(selection=True)
    try:
        constrainingList = _firstSuffix
        targetList = _secondSuffix

        filteredFirstList = [s for s in sel if constrainingList in s]
        filteredSecondList = [s for s in sel if targetList in s]

        if len(filteredFirstList) == len(filteredSecondList):

            for i in range(len(filteredFirstList)):
                cmds.scaleConstraint(filteredFirstList[i], filteredSecondList[i])



    except:
        print("Nope!!")
#=======================================
## Multi ScaleConstraint Function - END
#=======================================
