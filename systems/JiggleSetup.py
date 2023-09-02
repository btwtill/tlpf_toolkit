#Module Import
import maya.cmds as cmds



#=======================================
## Jiggle Setup Function
#=======================================
def createJiggleSetup():

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
## Jiggle Setup Function - END
#=======================================