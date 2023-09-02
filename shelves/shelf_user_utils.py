
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
from tlpf_toolkit.utils import ShapeInstanceFunction
from tlpf_toolkit.utils import MatchTransformFunction
from tlpf_toolkit.utils import ZeroOffsetFunction
from tlpf_toolkit.utils import NamingFunctions

from tlpf_toolkit.systems import IkFkSwitch
from tlpf_toolkit.systems import PoleVectorFunction
from tlpf_toolkit.systems import ReverseFootSetup
from tlpf_toolkit.systems import SimpleStretchSetup

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

        self.addButton(label="", icon=ICON_DIR + "/shapeInstance.png" ,command=ShapeInstanceFunction.shapeParentInstance)
        
        self.addButton(label="", icon=ICON_DIR + "/dupParentOnly.png", command="cmds.duplicate(parentOnly=True)")

        self.addButton(label="", icon=ICON_DIR + "/matchTransforms.png")
        transformMatchingMenu = cmds.popupMenu(b=1)

        self.addMenuItem(transformMatchingMenu, "match All", command=lambda _: MatchTransformFunction.matchAll())

        self.addMenuItem(transformMatchingMenu, "match Translation", command=lambda _: MatchTransformFunction.matchTranslation())

        self.addMenuItem(transformMatchingMenu, "match Rotation", command=lambda _: MatchTransformFunction.matchRotation())

        self.addMenuItem(transformMatchingMenu, "match Scale", command=lambda _: MatchTransformFunction.matchScale())
        
        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/ZeroFunctions.png")
        zeroMenu = cmds.popupMenu(b=1)

        self.addMenuItem(zeroMenu, "Sam Zero", command=lambda _: ZeroOffsetFunction.insertNodeBefore())
        self.addMenuItem(zeroMenu, "Tim Zero", command=lambda _: ZeroOffsetFunction.TimZeroUserConfig())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/suffix.png" ,command = NamingFunctions.SuffixConfigurationWindow)

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/IkFk.png" ,command=IkFkSwitch.IKFKConfigurationInterface)

        self.addButton(label="", icon=ICON_DIR + "/simplePV.png", command="")
        poleVectorMenu = cmds.popupMenu(b=1)

        self.addMenuItem(poleVectorMenu, "Simple PV", command=lambda _: PoleVectorFunction.createSimplePoleVector())
        self.addMenuItem(poleVectorMenu, "PV Line", command=lambda _: PoleVectorFunction.createPoleVectorLine())

        self.addButton(label="", icon=ICON_DIR + "/revChain.png" ,command= ReverseFootSetup.createReverseChain)

        self.addButton(label="", icon=ICON_DIR + "/samStretch.png" ,command=SimpleStretchSetup.SimpleStretchSetupConfigInterface)


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
