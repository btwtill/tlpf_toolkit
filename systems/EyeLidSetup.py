#Module Import 
import maya.cmds as cmds

#Eyelid_rig

## FUNCTIONS

#Joint Creation Function for seperate Eyelids
def createEylidJoints(vtxSelection, _centerPos, _baseName, *args, **kwargs):

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
def createAimedAtLocators(_constraintObjects, _targetPositions, _upVectorObject, _baseName, *args, **kwargs):
    
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

## Build
def buildEyeLidSetup():
    #base Name
    baseName = "l_eyelid"

    #get Selected Vertecies
    vtxSelectionUpperEyelid = cmds.ls(selection=True, flatten=True)

    vtxSelectionLowerEyelid = cmds.ls(selection=True, flatten=True)

    #get Eye center Position
    eyeCenterPos = cmds.xform("l_eyeCenterPos", q=True, ws=True, t=True)

    #Create an UpVector for aimConstraints
    upVectorObject = cmds.rename(cmds.spaceLocator()[0], baseName + "_UpVector")
    cmds.xform(upVectorObject, ws=True, t=[eyeCenterPos[0], eyeCenterPos[1] + 0.5, eyeCenterPos[2]])


    #create and store the Joints for the upper Eyelid
    upperEyelidParentJoints, upperEyelidSlideJoints = createEylidJoints(vtxSelectionUpperEyelid, eyeCenterPos, baseName, "Upper")
    print(upperEyelidParentJoints, upperEyelidSlideJoints)

    #clean Outliner
    upperEylidGrp = cmds.group(upperEyelidParentJoints, name=baseName + "UpperJoints_grp", world=True)

    #create the Aimed At Locators 
    aimLocators = createAimedAtLocators(upperEyelidParentJoints, upperEyelidSlideJoints, upVectorObject, baseName, "Upper")
    print(aimLocators)