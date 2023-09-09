#Module Import
import maya.cmds as cmds
from tlpf_toolkit.ui import common
from tlpf_toolkit.ctrlShapes import utils
import time

import logging
import os
import re
import subprocess

CURRENT_DIRECTORY = os.path.dirname(__file__)
DATA_LIBRARY_PATH = os.path.abspath("{}\\tmpData".format(CURRENT_DIRECTORY))

EYELIDUPPERVERTEXPATH = os.path.join(DATA_LIBRARY_PATH, "EyelidUpperVtxSel.json")
EYELIDLOWERVERTEXPATH = os.path.join(DATA_LIBRARY_PATH, "EyelidLowerVtxSel.json")

#Eyelid_rig

## FUNCTIONS

#Joint Creation Function for seperate Eyelids
def createEylidJoints(_baseName, _centerPos, vtxSelection, *args, **kwargs):

    #Store Vtx Joints
    vertexJoints = []

    #Store Parent Joints
    parentJoints = []
    
    #create joint createion
    for i in range(len(vtxSelection)):
        
        #craete joints at vertex position
        cmds.select(cl=1)
        vtxJnt = cmds.rename(cmds.joint(), _baseName + args[0] + "_skn" + str(i))
        vtxPos = cmds.xform(vtxSelection[i], q=True, ws=True, t=True)
        cmds.xform(vtxJnt, ws=True, t=vtxPos)
        vertexJoints.append(vtxJnt)
        
        #create joint at center position 
        cmds.select(cl=1)
        centerJnt = cmds.rename(cmds.joint(), _baseName + args[0] + "_jnt")
        cmds.xform(centerJnt, ws=True, t=_centerPos)
        parentJoints.append(centerJnt)
        
        #parent vertex joint to center joint
        cmds.parent(vtxJnt, centerJnt)
        
        #oritent the center joint to point towards the vertex joint
        cmds.joint(centerJnt, edit=True, orientJoint="xyz", secondaryAxisOrient="yup", zeroScaleOrient=True)
        
    return parentJoints, vertexJoints

#Create Locators at given Positions and Aim an Object at that Locator
def createAimedAtLocators(_baseName, _constraintObjects, _targetPositions, _upVectorObject, *args, **kwargs):
    
    #store the created Locators
    outputLocators = []
    
    #Iterate over target Positions
    for i in range(len(_targetPositions)):
            
        #create and Rename SpaceLocator
        targetLocator = cmds.rename(cmds.spaceLocator()[0], _baseName + args[0] + "_loc")
        
        #get target Position
        targetPos = cmds.xform(_targetPositions[i], q=True, ws=True, t=True)
        
        #set Locator Position to target Position
        cmds.xform(targetLocator, ws=True, t=targetPos)
        
        #crate aimConstraint
        cmds.aimConstraint(targetLocator, _constraintObjects[i], maintainOffset=True, weight=1, aimVector=[1, 0, 0], upVector=[0, 1, 0], worldUpType="object", worldUpObject=_upVectorObject)
        
        #add Locator to Output List
        outputLocators.append(targetLocator)
        
    #return output List
    return outputLocators   


#create Linear Curve from Selection
def createLinearCurveFromSelection(_objSelection, _crvName):

    #define Curve Point Positions and Knots
    pointPositions = []
    knots = []

    #iterate over selection
    for i in range(len(_objSelection)):

        #get woldspace point position and store it in the point position list
        newPos = cmds.xform(_objSelection[i], q=True, ws=True, t=True)
        pointPositions.append(newPos)

        #add Knot into Knot list
        knots.append(i)
    
    newCurve = cmds.curve(d=1, p=pointPositions, k=knots, n = _crvName)
    cmds.rename(cmds.listRelatives(newCurve, shapes=True), _crvName + "Shape")

    return newCurve, knots


#bind Objects to Closest Point on Curve
def bindObjectToCurve(_objects, _curve, _UParameter, _name = "pci"):
    
    #get the shape Node of the Curve
    curveShapeNode = cmds.listRelatives(_curve, shapes=True)[0]

    #iterate over Obejct selection
    for i in range(len(_objects)):

        #create Point on curve info node
        pciNode = cmds.createNode("pointOnCurveInfo", name = _name)

        #connect curve WorldSpace to pci
        cmds.connectAttr(curveShapeNode + ".worldSpace[0]", pciNode + ".inputCurve")

        #set pci Parameter Value to _UParameter
        cmds.setAttr(pciNode + ".parameter", _UParameter[i])

        #connect pci position Output to Object Translation
        for j in "XYZ":
            cmds.connectAttr(pciNode + ".position" + j, _objects[i] + ".translate" + j)


def EyelidConfigWindow():

    configWindow = cmds.window(title="Eyelid Setup", iconName="Eyelid", sizeable=True)

    cmds.rowColumnLayout( adjustableColumn=True )

    cmds.text(label="Give a Base Name for the Setup")

    Name= cmds.textField()

    eyeCenter = common.buildUserInputGrp("Set Eye Center Position", "Not Defined", 40)

    upperLabel = cmds.text(label="Not Defined")
    setUpper = cmds.button(label="set Upper", command = lambda _: saveUpperVertecies(upperLabel))
    
    lowerLabel=cmds.text(label="Not Defined")
    setLower = cmds.button(label="set Lower", command = lambda _: saveLowerVertecies(lowerLabel))

    buildEyelid = cmds.button(label="Build Setup", command= lambda _: BuildEyelidSetup(cmds.textField(Name, q=True, text=True), cmds.text(eyeCenter, q=True, label=True)))

    cmds.showWindow(configWindow)


def saveUpperVertecies(_label):
    vtx = cmds.ls(os=True, flatten=True)
    utils.save_data(EYELIDUPPERVERTEXPATH, vtx)
    cmds.text(_label, edit=True, label="Set", backgroundColor=[0.1, 0.8, 0.1])

def saveLowerVertecies(_label):
    vtx = cmds.ls(os=True, flatten=True)
    utils.save_data(EYELIDLOWERVERTEXPATH, vtx)
    cmds.text(_label, edit=True, label="Set", backgroundColor=[0.1, 0.8, 0.1])

## Build

def BuildEyelidSetup(_baseName, _centerPos):

    #base Name
    baseName = _baseName

    #get Selected Vertecies
    vtxSelectionUpperEyelid = utils.load_data(EYELIDUPPERVERTEXPATH)

    vtxSelectionLowerEyelid = utils.load_data(EYELIDLOWERVERTEXPATH)

    os.remove(EYELIDUPPERVERTEXPATH)
    os.remove(EYELIDLOWERVERTEXPATH)
    #get Eye center Position
    eyeCenterPos = cmds.xform(_centerPos, q=True, ws=True, t=True)

    #Create an UpVector for aimConstraints
    upVectorObject = cmds.rename(cmds.spaceLocator()[0], baseName + "_UpVector")
    cmds.xform(upVectorObject, ws=True, t=[eyeCenterPos[0], eyeCenterPos[1] + 0.5, eyeCenterPos[2]])


    #create and store the Joints for the upper Eyelid
    upperEyelidParentJoints, upperEyelidSlideJoints = createEylidJoints(_baseName, eyeCenterPos, vtxSelectionUpperEyelid, "Upper")
    print(upperEyelidParentJoints, upperEyelidSlideJoints)

    #create and store the Joints fo the lower Eyelid
    lowerEyelidParentJoints, lowerEyelidSlideJoints = createEylidJoints(_baseName, eyeCenterPos, vtxSelectionLowerEyelid, "Lower")
    
    #clean Outliner
    upperEyelidGrp = cmds.group(upperEyelidParentJoints, name=baseName + "UpperJoints_grp", world=True)
    lowerEyelidGrp = cmds.group(lowerEyelidParentJoints, name=baseName + "LowerJoints_grp", world=True)

    jointsGrp = cmds.group([upperEyelidGrp, lowerEyelidGrp], name=baseName + "Joints_grp", world = True)

    #create the Upper Aimed at Locators 
    upperAimLocators = createAimedAtLocators(_baseName, upperEyelidParentJoints, upperEyelidSlideJoints, upVectorObject, "Upper")

    #create the Lower Aimed at Locators
    lowerAimLocators = createAimedAtLocators(_baseName, lowerEyelidParentJoints, lowerEyelidSlideJoints, upVectorObject, "Lower")

    #clean Outliner
    upperEyelidAimLocatorGrp = cmds.group(upperAimLocators, name=baseName + "UpperAimLocator_grp", world=True)
    lowerEyelidAimLocatorGrp = cmds.group(lowerAimLocators, name=baseName + "LowerAimLocator_grp", world=True)
    
    AimLocatorGrp = cmds.group([upperEyelidAimLocatorGrp, lowerEyelidAimLocatorGrp], name= baseName + "AimLocator_grp", world=True)

    #create Curve from Selected Positions
    upperEyelidDefCurve, upperEyelidDefCurveParameters = createLinearCurveFromSelection(upperAimLocators, baseName + "UpperDefCurve")

    updatedlowerEylidAimLocators = lowerAimLocators

    updatedlowerEylidAimLocators.insert(0, upperAimLocators[0])

    updatedlowerEylidAimLocators.append(upperAimLocators[-1])

    lowerEyelidDefCurve, lowerEyelidDefCurveParameters = createLinearCurveFromSelection(updatedlowerEylidAimLocators, baseName + "lowerDefCurve")

    #bind locators to curve 
    bindObjectToCurve(upperAimLocators, upperEyelidDefCurve, upperEyelidDefCurveParameters, "UpperEyelid_PointInfo")

    lowerEyelidDefCurveParameters.pop(0)
    lowerEyelidDefCurveParameters.pop(-1)

    lowerAimLocators.pop(0)
    lowerAimLocators.pop(-1)

    bindObjectToCurve(lowerAimLocators, lowerEyelidDefCurve, lowerEyelidDefCurveParameters, "Lower_Eyelid_PointInfo")

    #rebuild Curve to Cubic deformation
    upperEyelidDriverCurve = cmds.rename(cmds.rebuildCurve(cmds.duplicate(upperEyelidDefCurve), ch=1, rpo=1, rt=0, kr=0, kcp=0, kep=0, kt=0, s=2, d=3, tol = 0.01), baseName + "UpperDriverCurve")

    lowerEyelidDriverCurve = cmds.rename(cmds.rebuildCurve(cmds.duplicate(lowerEyelidDefCurve), ch=1, rpo=1, rt=0, kr=0, kcp=0, kep=0, kt=0, s=2, d=3, tol = 0.01), baseName + "LowerDriverCurve")

    #hook def curve to ctr crv  mel(wire -gw false -en 1.000000 -ce 0.000000 -li 0.000000 -w l_eyelidUpperDriverCurve l_eyelidUpperDefCurve;)
    upperDrvCurveToDefCurve = cmds.wire(upperEyelidDefCurve, w = upperEyelidDriverCurve, name = "UpperdrvToDefWire")

    lowerDrvCurveToDefCurve = cmds.wire(lowerEyelidDefCurve, w = lowerEyelidDriverCurve, name = "LowerdrvToDefWire")