#Module Import
import maya.cmds as cmds
from tlpf_toolkit.ui import common

import logging
import os

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

#=======================================
## Sam Jiggle Setup Function
#=======================================
def createSamJiggleSetup():

    #get user Joint Selection
    sel = cmds.ls(selection=True)

    #get the parent of the user selection 
    parentJoint = cmds.pickWalk(direction="Up")

    #create the locatior structure, zro and pos
    zro_loc = cmds.spaceLocator(name=sel[0] + "_loc_zro")
    pos_loc = cmds.spaceLocator(name=sel[0] + "_loc_pos")

    #get the worldspace translation and rotation of the selected joint
    jointTranslation = cmds.xform(sel[0], query=True, ws=True, translation=True)
    jointRotation = cmds.xform(sel[0], query=True, ws=True, rotation=True)

    #set the locators translation and rotation to the same as the joint
    cmds.xform(zro_loc, translation=jointTranslation)
    cmds.xform(zro_loc, rotation=jointRotation)

    cmds.xform(pos_loc, translation=jointTranslation)
    cmds.xform(pos_loc, rotation=jointRotation)

    #parent the pos locator to the zro locator and the zro locator to the parent joint
    cmds.parent(pos_loc, zro_loc)
    cmds.parent(zro_loc, parentJoint)

    #create a locator that the joint will follow later
    follow_loc = cmds.spaceLocator(name=sel[0] + "_loc_follow")

    #create the particle used to sim the jiggle
    newParticle = cmds.particle(p=jointTranslation)

    #set the particles goal
    cmds.goal(newParticle, g=pos_loc)

    #connect the worldspace position of the particle to the follow locator pos
    cmds.connectAttr(newParticle[0] + ".worldCentroidX", follow_loc[0] + ".translateX")
    cmds.connectAttr(newParticle[0] + ".worldCentroidY", follow_loc[0] + ".translateY")
    cmds.connectAttr(newParticle[0] + ".worldCentroidZ", follow_loc[0] + ".translateZ")

    #constraint the joint between the position locator and follow locator
    cmds.pointConstraint(pos_loc, follow_loc, sel[0])


#=======================================
## Sam Jiggle Setup Function - END
#=======================================


#=======================================
## Tim Jiggle Setup Function
#=======================================

def TimJiggleSetupConfigInterface():
    
    #maya finwo object
    configwindow = cmds.window(sizeable=True, title="Tim Jiggle Setup", iconName="TimJiggle")

    #Set Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #Description
    cmds.text(label="Set the Motion Source Object")

    sourceObj = common.buildUserInputGrp("Set Source", "Not Defined Jet", 40)

    targetObject = common.buildUserInputGrp("Set Target", "Not Defined Jet", 40)

    parentObject = common.buildUserInputGrp("Set Parent", "Not Defined Jet", 40)

    cmds.text(label="Provide a Base Name for Node Naming Concvention", height=20, width=20)
    baseName = cmds.textField()

    buildButton = cmds.button(label="Lets Jiggle", command=lambda _: BuildTimJiggleSetup(cmds.text(sourceObj, query=True, label=True), 
                                                                                         cmds.textField(baseName, query=True, text=True),
                                                                                         cmds.text(targetObject, query=True, label=True),
                                                                                         cmds.text(parentObject, query=True, label=True)))

    cmds.showWindow(configwindow)

def BuildTimJiggleSetup(_sourceObj, _baseName, _targetObj, _parentObj):
    if _sourceObj == "Not Defined Jet":
        log.error("U Must Select a Source Object!!")
    else:
        log.info("Your Defined Source Object: {}".format(_sourceObj))
        if _baseName == None:
            _baseName = _sourceObj
        log.info("Your Defined Base Name: {}".format(_baseName))

        log.info("Your Defined Target Object: {}".format(_targetObj))

        log.info("Your Defined Parent Object: {}".format(_parentObj))
        
        if cmds.objExists(_sourceObj):

            #Source Object World Position
            pos = cmds.xform(_sourceObj, q=True, ws=True, t=True)

            #create Particle

            part = cmds.particle(p=[pos[0], (pos[1]), pos[2]], c=1, name="{}_particle".format(_baseName))
            cmds.setAttr("{}.particleRenderType".format(part[1]), 4)

            #set Particle goal
            cmds.goal(part[0], goal=_sourceObj, w=0.5, utr=True)

            #CreateOutput transform connected to Particle Centroid

            jiggle_output = cmds.spaceLocator(name="{}_ctl".format(_baseName))[0]
            cmds.connectAttr("{}.worldCentroid".format(part[1]), "{}.translate".format(jiggle_output))

            #Lock Output loc rotation/scale visibility
            for attr in ["rx", "ry", "rz", "sx", "sy", "sz", "v"]:
                cmds.setAttr("{}.{}".format(jiggle_output, attr), k=False, lock=True)

            #add gravity Object
            grav = cmds.gravity(
                    name="{}_gravity".format(_baseName),
                    pos=[0, 0, 0],
                    m=100,
                    att=0,
                    dx=0,
                    dy=-1,
                    dz=0,
                    mxd=-1,
            )[0]

            #dynamic connect Particle to Gravity Object
            cmds.connectDynamic(part, f=grav)
            
            # Add attrs: isDynamic=on, conserve=1.0, goalWeight[0]=1.0, goalSmoothness=3, gravity=9.8
            cmds.addAttr(jiggle_output, ln="JIGGLE", at="enum", en="__:")
            cmds.setAttr("{}.JIGGLE".format(jiggle_output), cb=True)

            # Enabled
            cmds.addAttr(jiggle_output, ln="enable", at="enum", en="OFF:ON")
            cmds.setAttr("{}.enable".format(jiggle_output), k=True, l=False)

            cmds.connectAttr(
                "{}.enable".format(jiggle_output), "{}.isDynamic".format(part[1])
            )

            # Conserve
            cmds.addAttr(jiggle_output, ln="conserve", at="double", min=0, max=1, dv=1)
            cmds.setAttr("{}.conserve".format(jiggle_output), k=True, l=False)
            cmds.connectAttr(
                "{}.conserve".format(jiggle_output), "{}.conserve".format(part[1])
            )

            # Goal Smoothness
            cmds.addAttr(jiggle_output, ln="goalSmoothness", at="double", min=0, dv=3)
            cmds.setAttr("{}.goalSmoothness".format(jiggle_output), k=True, l=False)
            cmds.connectAttr(
                "{}.goalSmoothness".format(jiggle_output),
                "{}.goalSmoothness".format(part[1]),
            )

            # Goal Weight
            cmds.addAttr(
                jiggle_output, ln="goalWeight", at="double", min=0, max=1.0, dv=0.5
            )
            cmds.setAttr("{}.goalWeight".format(jiggle_output), k=True, l=False)
            cmds.connectAttr(
                "{}.goalWeight".format(jiggle_output), "{}.goalWeight[0]".format(part[1])
            )

            cmds.addAttr(jiggle_output, ln="GRAVITY", at="enum", en="__:")
            cmds.setAttr("{}.GRAVITY".format(jiggle_output), cb=True)

            # Gravity
            cmds.addAttr(jiggle_output, ln="gravityMagnitude", at="double", min=0, dv=100)
            cmds.setAttr("{}.gravityMagnitude".format(jiggle_output), k=True, l=False)
            cmds.connectAttr(
                "{}.gravityMagnitude".format(jiggle_output), "{}.magnitude".format(grav)
            )

            # Gravity Direction
            cmds.addAttr(jiggle_output, ln="gravityDirection", at="double3")
            cmds.addAttr(
                jiggle_output,
                ln="gravityDirectionX",
                at="double",
                p="gravityDirection",
                dv=0,
            )
            cmds.addAttr(
                jiggle_output,
                ln="gravityDirectionY",
                at="double",
                p="gravityDirection",
                dv=-1,
            )
            cmds.addAttr(
                jiggle_output,
                ln="gravityDirectionZ",
                at="double",
                p="gravityDirection",
                dv=0,
            )

            cmds.setAttr("{}.gravityDirection".format(jiggle_output), k=True, l=False)
            cmds.setAttr("{}.gravityDirectionX".format(jiggle_output), k=True, l=False)
            cmds.setAttr("{}.gravityDirectionY".format(jiggle_output), k=True, l=False)
            cmds.setAttr("{}.gravityDirectionZ".format(jiggle_output), k=True, l=False)

            cmds.connectAttr(
                "{}.gravityDirectionX".format(jiggle_output), "{}.directionX".format(grav)
            )
            cmds.connectAttr(
                "{}.gravityDirectionY".format(jiggle_output), "{}.directionY".format(grav)
            )
            cmds.connectAttr(
                "{}.gravityDirectionZ".format(jiggle_output), "{}.directionZ".format(grav)
            )

            # Cleanup
            jiggle_group = cmds.group(empty=True, name="{}All_grp".format(_baseName))
            cmds.parent(part[0], jiggle_output, grav, jiggle_group)

            cmds.select(jiggle_output)

            #Disable Inherit Transform for the Output Locator
            cmds.setAttr(jiggle_output + ".inheritsTransform", 0)

            # #Constraint the targetObject to the output OBject
            # jiggleOffsetNode = cmds.duplicate(_targetObj, po=True, name=_targetObj + "_JiggleOffset")
            # cmds.parent(_targetObj, jiggleOffsetNode)

            # targetConstraint = cmds.pointConstraint(jiggle_output, jiggleOffsetNode, mo=True, sk= ["x", "y"])
            # cmds.connectAttr(jiggle_output + ".enable", targetConstraint[0] + "." + jiggle_output + "W0")

            #parent the jiggle group to the parent Object
            cmds.parent(jiggle_group, _parentObj)

            return jiggle_output
#=======================================
## Tim Jiggle Setup Function - END
#=======================================
