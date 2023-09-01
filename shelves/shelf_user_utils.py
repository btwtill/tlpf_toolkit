
SHELF_NAME = "tlpf_shelf"

# Logging module is used to print output to user
import logging

LOG = logging.getLogger(__name__)


# Import python modules used in this script
import os
import sys
import subprocess
import importlib


# Inherit shelf base class module whose functions we "override" to build our tlpf_toolkit shelf
from tlpf_toolkit.shelves import shelf_base

importlib.reload(shelf_base)


# Import maya modules
from maya import cmds

#Import Functions Modules
from tlpf_toolkit.utils import ShapeParentFunction

# GLOBAL script variables referred to throughout this script
ICON_DIR = os.path.join(os.path.dirname(__file__), "shelf_user_utils_icons")
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "shelf_user_utils_scripts")
PLATFORM = sys.platform

sys.path.append(SCRIPTS_DIR)


def reload_shelf(shelf_name=SHELF_NAME):
    """Reloads shelf"""
    try:
        from tlpf_toolkit.shelves import shelf_base

        importlib.reload(shelf_base)

        from tlpf_toolkit.shelves import shelf_user_utils

        importlib.reload(shelf_user_utils)

        shelf_user_utils.load(name=SHELF_NAME)

        LOG.info("Successfully reloaded {} shelf".format(SHELF_NAME))
        return True
    except:
        LOG.error("Error reloading shelf")
        return


class load(shelf_base._shelf):
    def build(self):
        # Reload shelf button
        self.addButton(
            label="",
            icon=ICON_DIR + "/reloadShelf.png",
            command=lambda: reload_shelf(shelf_name=SHELF_NAME),
        )

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/shapeParent.png" ,command=ShapeParentFunction.ShapeParent)


        

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")









        #Fr reference


        #general_tools_menu = cmds.popupMenu(b=1)

        # self.addMenuItemDivider(
        #     general_tools_menu, divider=True, dividerLabel="PROJECT..."
        # )
        # Week 6 Tools - FOR REFERENCE
        # self.addButton(label="", icon=ICON_DIR + "/week6ToolsRef.png")

        # week6_tools_menu = cmds.popupMenu(b=1)

        # cmds.menuItem(
        #     p=week6_tools_menu,
        #     l="Duplicate (Parent Only)",
        #     command=lambda _: cmds.duplicate(parentOnly=True),
        # )
