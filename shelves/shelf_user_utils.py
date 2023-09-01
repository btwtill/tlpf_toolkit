
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


# Import the week6 module whose commands we call in the week6 shelf button
from tlpf_toolkit.utils import week6

importlib.reload(week6)


# Import maya modules
from maya import cmds


# GLOBAL script variables referred to throughout this script
ICON_DIR = os.path.join(os.path.dirname(__file__), "shelf_user_utils_icons")
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "shelf_user_utils_scripts")
PLATFORM = sys.platform

sys.path.append(SCRIPTS_DIR)


def explore_maya_project():
    """Opens explorer window to current Maya project location"""
    proj_dir = cmds.workspace(rd=True, q=True)
    subprocess.Popen(r'explorer /select,"{}scenes"'.format(proj_dir.replace("/", "\\")))
    LOG.info("Exploring to %s".format(proj_dir))


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


def setup_user_marking_menu():
    from tlpf_toolkit.marking_menu import user_marking_menu

    importlib.reload(user_marking_menu)
    user_marking_menu.markingMenu()

    LOG.info("Setup User Marking Menu")


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

        # General Tools
        self.addButton(label="", icon=ICON_DIR + "/generalTools.png")

        general_tools_menu = cmds.popupMenu(b=1)

        self.addMenuItemDivider(
            general_tools_menu, divider=True, dividerLabel="PROJECT..."
        )

        self.addMenuItem(
            general_tools_menu,
            "Explore to Project Directory",
            command=lambda _: explore_maya_project(),
        )

        self.addMenuItemDivider(
            general_tools_menu, divider=True, dividerLabel="SETUP..."
        )

        self.addMenuItem(
            general_tools_menu,
            "Setup Marking Menu",
            command=lambda _: setup_user_marking_menu(),
        )

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        # ==================================================================
        # User Tools here

        # ==================================================================

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        # Week 6 Tools - FOR REFERENCE
        self.addButton(label="", icon=ICON_DIR + "/week6ToolsRef.png")

        week6_tools_menu = cmds.popupMenu(b=1)

        cmds.menuItem(
            p=week6_tools_menu,
            l="Duplicate (Parent Only)",
            command=lambda _: cmds.duplicate(parentOnly=True),
        )

        cmds.menuItem(
            p=week6_tools_menu,
            l="Snap second selected object to first",
            command=lambda _: week6.match_selection(),
        )

        cmds.menuItem(
            p=week6_tools_menu,
            l="Create Pole Vector (select PV control then IK handle)",
            command=lambda _: week6.create_pole_vector_from_selection(),
        )

        cmds.menuItem(
            p=week6_tools_menu,
            l="Create Category Switch (select rig top node)",
            command=lambda _: week6.create_category_ui(),
        )

        cmds.menuItem(
            p=week6_tools_menu,
            l="Add offset and group transforms above selected control",
            command=lambda _: week6.add_transforms_selected(),
        )
