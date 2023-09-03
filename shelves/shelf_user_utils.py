
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
from tlpf_toolkit.utils import MultiConstraintFunction

from tlpf_toolkit.systems import IkFkSwitch
from tlpf_toolkit.systems import PoleVectorFunction
from tlpf_toolkit.systems import ReverseFootSetup
from tlpf_toolkit.systems import SimpleStretchSetup
from tlpf_toolkit.systems import TwistJoints
from tlpf_toolkit.systems import JiggleSetup

from tlpf_toolkit.ctrls import CtrlColorFunction
from tlpf_toolkit.ctrls import CreateBasicCtls

from tlpf_toolkit.mtrx import MatrixZeroOffset
from tlpf_toolkit.mtrx import MatrixZeroDrvOffset

from tlpf_toolkit.node import MultiConnectFunction
from tlpf_toolkit.node import CreateDistanceBetween
from tlpf_toolkit.node import NodeSRTConnector

from tlpf_toolkit.locator import LocatorFunctions

from tlpf_toolkit.joint import JointFunctions

from tlpf_toolkit.skin import SkinFunctions

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

        self.addButton(label="", icon=ICON_DIR + "/V002/ShapeParent.png" ,command=ShapeParentFunction.ShapeParent)

        self.addButton(label="", icon=ICON_DIR + "/V002/ShapeInstance.png" ,command=ShapeInstanceFunction.shapeParentInstance)
        
        self.addButton(label="", icon=ICON_DIR + "/V002/DupParentOnly.png", command="cmds.duplicate(parentOnly=True)")

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/MatchMenu.png")
        transformMatchingMenu = cmds.popupMenu(b=1)

        self.addMenuItem(transformMatchingMenu, "match All", command=lambda _: MatchTransformFunction.matchAll())

        self.addMenuItem(transformMatchingMenu, "match Translation", command=lambda _: MatchTransformFunction.matchTranslation())

        self.addMenuItem(transformMatchingMenu, "match Rotation", command=lambda _: MatchTransformFunction.matchRotation())

        self.addMenuItem(transformMatchingMenu, "match Scale", command=lambda _: MatchTransformFunction.matchScale())

        self.addButton(label="", icon=ICON_DIR + "/V002/LRA.png", command="for i in cmds.ls(selection=True): cmds.toggle(i, la=True)")

        
        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/ZeroFunctionsv2.png")
        zeroMenu = cmds.popupMenu(b=1)

        self.addMenuItem(zeroMenu, "Sam Zero", command=lambda _: ZeroOffsetFunction.insertNodeBefore())

        self.addMenuItem(zeroMenu, "Tim Zero", command=lambda _: ZeroOffsetFunction.TimZeroUserConfig())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/Suffix.png" ,command = NamingFunctions.SuffixConfigurationWindow)

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/IkFk.png" ,command=IkFkSwitch.IKFKConfigurationInterface)

        self.addButton(label="", icon=ICON_DIR + "/V002/PV.png", command="")
        poleVectorMenu = cmds.popupMenu(b=1)

        self.addMenuItem(poleVectorMenu, "Simple PV", command=lambda _: PoleVectorFunction.createSimplePoleVector())

        self.addMenuItem(poleVectorMenu, "PV Line", command=lambda _: PoleVectorFunction.createPoleVectorLine())

        self.addButton(label="", icon=ICON_DIR + "/V002/RevChain.png" ,command= ReverseFootSetup.createReverseChain)

        self.addButton(label="", icon=ICON_DIR + "/V002/Stretch.png" ,command=SimpleStretchSetup.SimpleStretchSetupConfigInterface)

        self.addButton(label="", icon=ICON_DIR + "/V002/TwistJoints.png" ,command=TwistJoints.twistSetupConfigInterface)

        self.addButton(label="", icon=ICON_DIR + "/V002/Jiggle.png" ,command = JiggleSetup.createJiggleSetup)

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/CtrlColor.png" ,command=CtrlColorFunction.ColorSettingWindow)

        self.addButton(label="", icon=ICON_DIR + "/V002/BasicCtrls.png" ,command= CreateBasicCtls.CreateCircleCtrls)

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/MtrxMenu.png", command="")
        MatrixMenu = cmds.popupMenu(b=1)

        self.addMenuItem(MatrixMenu, "Matrix Zero Offset", command=lambda _: MatrixZeroOffset.iterateCreateMatrixZeroOffset())
        self.addMenuItem(MatrixMenu, "Matrix Drv Offset", command=lambda _: MatrixZeroDrvOffset.createMatrixDrvOffset())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/NodeMenu.png", command="")
        NodeMenu = cmds.popupMenu(b=1)

        self.addMenuItemDivider(NodeMenu, divider=True, dividerLabel="MULTI CONNECTOR")

        self.addMenuItem(NodeMenu, "1 zu N MultiConnect", command=lambda _: MultiConnectFunction.MultiConnectOneToNConfigurationInterface())

        self.addMenuItem(NodeMenu, "M zu N MultiConnect", command=lambda _: MultiConnectFunction.MultiConnectMToNConfigurationInterface())

        self.addMenuItemDivider(NodeMenu, divider=True, dividerLabel="SRT Connector")
        
        self.addMenuItem(NodeMenu, "Connect SRT", command= lambda _: NodeSRTConnector.ConnectSRT())

        self.addMenuItem(NodeMenu, "Connect Translate", command= lambda _: NodeSRTConnector.ConnectTranslate())

        self.addMenuItem(NodeMenu, "Connect Rotate", command= lambda _: NodeSRTConnector.ConnectRotate())

        self.addMenuItem(NodeMenu, "Connect Scale", command= lambda _: NodeSRTConnector.ConnectScale())

        self.addMenuItemDivider(NodeMenu, divider=True, dividerLabel="UTILITY")

        self.addMenuItem(NodeMenu, "Distance Bewteen", command=lambda _: CreateDistanceBetween.createDistance())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        #Multi Constraining
        self.addButton(label="", icon=ICON_DIR + "/V002/ConstraintMenu.png")
        multiConstraining_menu = cmds.popupMenu(b=1)

        ##Adding all menu items for Multi Constraining
        self.addMenuItemDivider(multiConstraining_menu, divider=True, dividerLabel="CHOOSE CONSTRAINT TYPE")

        self.addMenuItem(multiConstraining_menu, "Parent Constraint", command=lambda _: MultiConstraintFunction.MultiParentConstraintConfig())

        self.addMenuItem(multiConstraining_menu, "Orient Constraint", command=lambda _: MultiConstraintFunction.MultiOrientConstraintConfig())

        self.addMenuItem(multiConstraining_menu, "Scale Constraint", command=lambda _: MultiConstraintFunction.MultiScaleConstraintConfig())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/LOCMenu.png")
        LocatorMenu = cmds.popupMenu(b=1)

        self.addMenuItem(LocatorMenu, "Create Loc at Seleceted Pos", command=lambda _: LocatorFunctions.selected_points())

        self.addMenuItem(LocatorMenu, "Create Loc at CENTER of Selected", command=lambda _: LocatorFunctions.center_selection_weighted_average())

        self.addMenuItem(LocatorMenu, "Create Loc Aimed at Selected", command=lambda _: LocatorFunctions.aim_selection())

        self.addMenuItem(LocatorMenu, "Create Loc at Loc/Rot", command=lambda _: LocatorFunctions.create_locator_snap())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/JNTMenu.png")
        JointMenu = cmds.popupMenu(b=1)

        self.addMenuItem(JointMenu, "Create Joint at Selection", command=lambda _: JointFunctions.CreateJointsOnSelected())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/SkinMenu.png")
        SkinMenu = cmds.popupMenu(b=1)

        self.addMenuItem(SkinMenu, "Transfer SkinCluster", command=lambda _: SkinFunctions.do_transfer_skin())

        self.addMenuItemDivider(SkinMenu, divider=True, dividerLabel="IMPORT/EXPORT")

        self.addMenuItem(SkinMenu, "Export SkinWeights", command=lambda _: SkinFunctions.export_skin_weights_selected())

        self.addMenuItem(SkinMenu, "Import SkinWeights", command=lambda _: SkinFunctions.import_skin_weights_selected())
        
        
