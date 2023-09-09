
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
from tlpf_toolkit.systems import LipSetup
from tlpf_toolkit.systems import EyeLidSetup

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

from tlpf_toolkit.attr import VisibilityAttributFunctions

from tlpf_toolkit.ctrlShapes import color as ctl_color
from tlpf_toolkit.ctrlShapes import core as ctl_core
from tlpf_toolkit.ctrlShapes import functions as ctl_func
from tlpf_toolkit.ctrlShapes import transform as ctl_trans

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

        #IKFK Menu
        self.addButton(label="", icon=ICON_DIR + "/V002/IkFk.png" , command="")
        IkFkMenu = cmds.popupMenu(b=1)

        self.addMenuItem(IkFkMenu, "Auto IKFK Chain", command=lambda _: IkFkSwitch.IKFKConfigurationInterface())

        self.addMenuItemDivider(IkFkMenu, divider=True, dividerLabel="UTILITY")
        
        self.addMenuItem(IkFkMenu, "Add Soft IK", command=lambda _: IkFkSwitch.SoftIKConfigInterface())

        self.addMenuItem(IkFkMenu, "Create Single IKFK Blend", command=lambda _: IkFkSwitch.CreateSinlgeIKFKBlend())

        #PoleVector Menu
        self.addButton(label="", icon=ICON_DIR + "/V002/PV.png", command="")
        poleVectorMenu = cmds.popupMenu(b=1)

        self.addMenuItem(poleVectorMenu, "Simple PV", command=lambda _: PoleVectorFunction.createSimplePoleVector())

        self.addMenuItem(poleVectorMenu, "PV Line", command=lambda _: PoleVectorFunction.createPoleVectorLine())

        #Revers Chain
        self.addButton(label="", icon=ICON_DIR + "/V002/RevChain.png" ,command= ReverseFootSetup.createReverseChain)

        #Stretch Setup
        self.addButton(label="", icon=ICON_DIR + "/V002/Stretch.png" ,command=SimpleStretchSetup.SimpleStretchSetupConfigInterface)

        #Twist Joints
        self.addButton(label="", icon=ICON_DIR + "/V002/TwistJoints.png" ,command=TwistJoints.twistSetupConfigInterface)

        #Jiggle Menu
        self.addButton(label="", icon=ICON_DIR + "/V002/Jiggle.png")
        jiggleMenu = cmds.popupMenu(b=1)

        self.addMenuItem(jiggleMenu, "Sam Jiggle Setup", command=lambda _: JiggleSetup.createSamJiggleSetup())

        self.addMenuItem(jiggleMenu, "Tim Jiggle Setup", command=lambda _: JiggleSetup.TimJiggleSetupConfigInterface())


        #Lip Setup
        self.addButton(label="", icon=ICON_DIR + "/V002/Lip.png" ,command = LipSetup.SimpleStretchSetupConfigInterface)

        #Eyelid Setup
        self.addButton(label="", icon=ICON_DIR + "/V002/EyeMenu.png")
        EyeMenu = cmds.popupMenu(b=1)

        self.addMenuItem(EyeMenu, "Eyelid Base", command = lambda _: EyeLidSetup.EyelidConfigWindow())

        
        



        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V002/CtrlColor.png" ,command=CtrlColorFunction.ColorSettingWindow)

        self.addButton(label="", icon=ICON_DIR + "/V002/BasicCtrls.png" ,command= CreateBasicCtls.CreateCircleCtrls)





        #=======================================
        ## DISCLAIMER - Credit for the Following 
        # Menu goes to Tim Colemen and Martin Lanton From CGMA 
        # and there MechRig Toolkit Repsoitory - https://github.com/martinlanton/mechRig_toolkit
        #=======================================
        # Anim Control Tools
        self.addButton(label="", icon=ICON_DIR + "/V002/CtrlShapes.png")
        ctl_tools_menu = cmds.popupMenu(b=1)

        cmds.menuItem(p=ctl_tools_menu, divider=True, dividerLabel="SHAPE...")
        cmds.menuItem(
            p=ctl_tools_menu, l="Save Shape...", command=ctl_func.save_ctl_shape_to_lib
        )

        sub = cmds.menuItem(
            p=ctl_tools_menu, l="Assign Shape to selected...", subMenu=1
        )

        for each in ctl_func.get_available_control_shapes():
            self.addMenuItem(sub, each[0], command=each[1])

        cmds.menuItem(
            p=ctl_tools_menu,
            l="Open Shape directory...",
            c=lambda *args: ctl_core.open_control_shape_directory(),
        )

        cmds.menuItem(p=ctl_tools_menu, divider=True, dividerLabel="COLOR...")
        cmds.menuItem(
            p=ctl_tools_menu,
            l="Color Shapes",
            command=lambda *args: ctl_color.set_override_color_UI(),
        )

        cmds.menuItem(p=ctl_tools_menu, divider=True, dividerLabel="COPY/PASTE...")
        cmds.menuItem(
            p=ctl_tools_menu,
            l="Copy Shape",
            command=lambda *args: ctl_func.copy_ctl_shape(),
        )
        cmds.menuItem(
            p=ctl_tools_menu,
            l="Paste Shape",
            command=lambda *args: ctl_func.paste_ctl_shape(),
        )
        cmds.menuItem(
            p=ctl_tools_menu,
            l="Delete Shapes",
            command=lambda *args: ctl_func.delete_shapes(),
        )

        # cmds.menuItem(p=ctl_tools_menu, divider=True, dividerLabel="TRANSFORM...")
        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Mirror Shape",
        #     command=lambda *args: ctl_trans.mirror_ctl_shapes(),
        # )

        cmds.menuItem(p=ctl_tools_menu, divider=True)

        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Rotate X 90",
        #     command=lambda *args: ctl_trans.rotate_shape([90, 0, 0]),
        # )
        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Rotate Y 90",
        #     command=lambda *args: ctl_trans.rotate_shape([0, 90, 0]),
        # )
        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Rotate Z 90",
        #     command=lambda *args: ctl_trans.rotate_shape([0, 0, 90]),
        # )

        # cmds.menuItem(p=ctl_tools_menu, divider=True)

        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Rotate X -90",
        #     command=lambda *args: ctl_trans.rotate_shape([-90, 0, 0]),
        # )
        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Rotate Y -90",
        #     command=lambda *args: ctl_trans.rotate_shape([0, -90, 0]),
        # )
        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Rotate Z -90",
        #     command=lambda *args: ctl_trans.rotate_shape([0, 0, -90]),
        # )

        # cmds.menuItem(p=ctl_tools_menu, divider=True)

        cmds.menuItem(
            p=ctl_tools_menu,
            l="Scale Up Shape",
            command=lambda *args: ctl_trans.scale_up_selected(),
        )
        cmds.menuItem(
            p=ctl_tools_menu,
            l="Scale Down Shape",
            command=lambda *args: ctl_trans.scale_down_selected(),
        )

        cmds.menuItem(p=ctl_tools_menu, divider=True)

        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Flip Shape",
        #     command=lambda *args: ctl_trans.flip_shape_callback(),
        # )
        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Flip Shape X",
        #     command=lambda *args: ctl_trans.flip_shape_X(),
        # )
        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Flip Shape Y",
        #     command=lambda *args: ctl_trans.flip_shape_Y(),
        # )
        # cmds.menuItem(
        #     p=ctl_tools_menu,
        #     l="Flip Shape Z",
        #     command=lambda *args: ctl_trans.flip_shape_Z(),
        # )
        #=======================================
        ## DISCLAIMER - END
        #=======================================






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

        self.addMenuItem(SkinMenu, "Transfer SkinCluster Between Namespaces", command=lambda _: SkinFunctions.NamespaceSkinClusterTransferConfigInterface())
        
        self.addMenuItemDivider(SkinMenu, divider=True, dividerLabel="IMPORT/EXPORT")

        self.addMenuItem(SkinMenu, "Export SkinWeights", command=lambda _: SkinFunctions.export_skin_weights_selected())

        self.addMenuItem(SkinMenu, "Import SkinWeights", command=lambda _: SkinFunctions.import_skin_weights_selected())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/sep.png", command="")

        #Attribute Menu
        self.addButton(label="", icon=ICON_DIR + "/V002/AttrMenu.png")
        AttrMenu = cmds.popupMenu(b=1)

        self.addMenuItemDivider(AttrMenu, divider=True, dividerLabel="VISIBILITY ATTR")

        self.addMenuItem(AttrMenu, "Add Visibility Attr", command=lambda _: VisibilityAttributFunctions.CreateHiddenVisibilityAttributeConfigUI())

        self.addMenuItemDivider(AttrMenu, divider=True, dividerLabel="LOCK/UNLOCK")

        self.addMenuItem(AttrMenu, "Lock Default Attributes", command=lambda _: VisibilityAttributFunctions.lock_unlock_channels(True))

        self.addMenuItem(AttrMenu, "Unlock Default Attributes", command=lambda _: VisibilityAttributFunctions.lock_unlock_channels(False))

        self.addMenuItemDivider(AttrMenu, divider=True, dividerLabel="UTILITY")

        self.addMenuItem(AttrMenu, "Add Attribute Divider", command=lambda _: VisibilityAttributFunctions.CreateAttributeDividerConfigUI())

        self.addMenuItem(AttrMenu, "Copy Attributes Over", command=lambda _: VisibilityAttributFunctions.CopyAttributesToSelectionConfigUI())

        
        