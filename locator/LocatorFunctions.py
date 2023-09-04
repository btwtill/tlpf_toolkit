#=======================================
## Disclaimer
#  The following code is from the MechRig Toolkit Provided 
#  By Tim Coleman and Martin Lanton at CGMA and can be found on Github at 
#  https://github.com/martinlanton/mechRig_toolkit
#  Huge Thanks!!
#
#=======================================

import logging

from maya import cmds

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)




#=======================================
## Enable track selection If turned OFF
#=======================================
def enable_track_selections():
    # Enable trackSelectionOrder to get proper selection order for aim_selection()
    if not cmds.selectPref(trackSelectionOrder=True):
        cmds.selectPref(trackSelectionOrder=True)
        log.info("Track selection order enabled")
#=======================================
## Enable track selection If turned OFF - END
#=======================================



#=======================================
## Create Locators at Selected Position
#=======================================
def selected_points():
    sel = cmds.ls(selection=True, flatten=True)

    # If there is a valid selection
    if sel:
        # Loop through the selected nodes
        for i in range(0, len(sel)):
            # We'll store the position data returned by the xform command in the "pos" variable
            pos = list()

            # Check if node is a transform/joint OR a component vertex/CV
            # If a transform, we'll use the "piv" flag in the xform command for accuracy
            if "transform" in cmds.nodeType(sel[i]) or "joint" in cmds.nodeType(sel[i]):
                log.info("{} is a transform/joint".format(sel[i]))
                pos = cmds.xform(sel[i], query=True, worldSpace=True, piv=True)

            # Otherwise, we'll use the "translation" flag for all else, including components
            else:
                log.info("{} is a component".format(sel[i]))
                pos = cmds.xform(sel[i], query=True, worldSpace=True, translation=True)

            # Create a locator and move it to the node's position we just obtained
            loc = cmds.spaceLocator(p=[0, 0, 0])
            cmds.setAttr(loc[0] + ".translate", pos[0], pos[1], pos[2])

        log.info("Created locators at selected positions.")
        return True

    # If nothing is selected, let the user know
    else:
        log.error("Nothing selected!")
        return
#=======================================
## Create Locators at Selected Position - END
#=======================================

#=======================================
## Create Locators at Center of Selected 
#=======================================
def center_selection_weighted_average():
    """Locator created at center position of selected"""
    sel = cmds.ls(orderedSelection=True, flatten=True)

    if sel:
        # Initialize our cntr_pos variable to "0" to start, these 3 values represent XYZ positions
        cntr_pos = [0.0, 0.0, 0.0]

        # Loop through each selection and add it's XYZ position to cntr_pos
        for i in range(0, len(sel)):
            # Check if node is a transform/joint OR a component vertex/CV
            # If a transform, we'll use the "piv" flag in the xform command for accuracy
            if "transform" in cmds.nodeType(sel[i]) or "joint" in cmds.nodeType(sel[i]):
                log.info("{} is a transform/joint".format(sel[i]))
                pos = cmds.xform(sel[i], query=True, worldSpace=True, piv=True)

            # Otherwise, we'll use the "translation" flag for all else, including components
            else:
                log.info("{} is a component".format(sel[i]))
                pos = cmds.xform(sel[i], query=True, worldSpace=True, translation=True)

            cntr_pos[0] = pos[0] + cntr_pos[0]
            cntr_pos[1] = pos[1] + cntr_pos[1]
            cntr_pos[2] = pos[2] + cntr_pos[2]

        # Now divide the sum of all the positions by the number of selected items
        cntr_pos[0] = cntr_pos[0] / len(sel)
        cntr_pos[1] = cntr_pos[1] / len(sel)
        cntr_pos[2] = cntr_pos[2] / len(sel)

        # Create a locator and set it's position to the final cntr_pos value
        loc = cmds.spaceLocator(p=[0, 0, 0])
        cmds.setAttr(loc[0] + ".translate", cntr_pos[0], cntr_pos[1], cntr_pos[2])

        log.info("Created locators at selected positions.")
        return loc[0]

    else:
        log.error("Nothing selected!")
#=======================================
## Create Locators at Center of Selected - END
#=======================================


#=======================================
## Create Aimed Locator Function 
#=======================================
def aim_selection(aim_vec=[1, 0, 0], up_vec=[0, 1, 0]):
    """Takes 3 points, position, aim and up and creates positioned/oriented locator"""

    # Make sure we're getting our list of items in the correct order here, pos, aim, up
    sel = cmds.ls(
        selection=True, flatten=True
    )  # BUG - for some reason, need to run this first?
    sel = cmds.ls(orderedSelection=True, flatten=True)

    # If we have 3 selected points/objects let's continue
    if len(sel) == 3:
        # Get the positions of each vector
        pos = cmds.xform(sel[0], query=True, ws=True, translation=True)
        aim = cmds.xform(sel[1], query=True, ws=True, translation=True)
        up = cmds.xform(sel[2], query=True, ws=True, translation=True)

        # Create a locator and move it to the position
        pos_loc = cmds.spaceLocator(p=[0, 0, 0])
        cmds.setAttr(pos_loc[0] + ".translate", pos[0], pos[1], pos[2])

        # Create a temp AIM locator and move it to the aim position
        aim_loc = cmds.spaceLocator(p=[0, 0, 0], name="aimTEMP")
        cmds.setAttr(aim_loc[0] + ".translate", aim[0], aim[1], aim[2])

        # Create a temp UP locator and move it to the up position
        up_loc = cmds.spaceLocator(p=[0, 0, 0], name="upTEMP")
        cmds.setAttr(up_loc[0] + ".translate", up[0], up[1], up[2])

        # Aim constrain pos_loc to aim_loc while using our up position as up vector
        cmds.aimConstraint(
            aim_loc,
            pos_loc,
            aimVector=aim_vec,
            upVector=up_vec,
            worldUpType="object",
            worldUpObject=up_loc[0],
            worldUpVector=[up[0], up[1], up[2]],
        )

        cmds.delete(aim_loc, up_loc)
        cmds.setAttr("{}.displayLocalAxis".format(pos_loc[0]), 1)
        cmds.select(sel, pos_loc[0])

    else:
        log.error("Please select 3 points/objects (position, aim and up)")
        return
#=======================================
## Create Aimed Locator Function - END
#=======================================


#=======================================
## Create Locator at Selected Loc/Rot
#=======================================
def create_locator_snap():
    """Creates new locator and snaps to selected"""
    created_locs = list()
    selection = cmds.ls(selection=True)
    for item in selection:
        loc = cmds.spaceLocator()
        cmds.select(loc[0], item)
        snap_object()
        created_locs.append(loc[0])
        log.info("Created {} and snapped to {}".format(loc[0], item))
    cmds.select(created_locs)


def snap_object():
    """Snaps first selected objects to last selected object"""
    selection = cmds.ls(selection=True)
    if len(selection) >= 2:
        pos = cmds.xform(selection[-1], q=True, ws=True, t=True)
        rot = cmds.xform(selection[-1], q=True, ws=True, ro=True)
        for item in selection[:-1]:
            cmds.xform(item, ws=True, t=pos)
            cmds.xform(item, ws=True, ro=rot)
            log.info("Snapped {} to {}".format(item, selection[-1]))
#=======================================
## Create Locator at Selected Loc/Rot - END
#=======================================
