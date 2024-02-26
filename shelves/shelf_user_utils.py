
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
from tlpf_toolkit.utils import GeneralFunctions

from tlpf_toolkit.systems import IkFkSwitch
from tlpf_toolkit.systems import PoleVectorFunction
from tlpf_toolkit.systems import ReverseFootSetup
from tlpf_toolkit.systems import SimpleStretchSetup
from tlpf_toolkit.systems import TwistJoints
from tlpf_toolkit.systems import JiggleSetup
from tlpf_toolkit.systems import LipSetup
from tlpf_toolkit.systems import EyeLidSetup
from tlpf_toolkit.systems import SplineSystem
from tlpf_toolkit.systems import SpaceSwapping
from tlpf_toolkit.systems import RibbonSetup

from tlpf_toolkit.ctrls import CtrlColorFunction
from tlpf_toolkit.ctrls import CreateBasicCtls
from tlpf_toolkit.ctrls import CtrlMirror

from tlpf_toolkit.mtrx import MatrixZeroOffset
from tlpf_toolkit.mtrx import MatrixZeroDrvOffset
from tlpf_toolkit.mtrx import CorrectiveMatrixSetup
from tlpf_toolkit.mtrx import MatrixConstraints
from tlpf_toolkit.mtrx import MatrixFunctions

from tlpf_toolkit.node import MultiConnectFunction
from tlpf_toolkit.node import CreateDistanceBetween
from tlpf_toolkit.node import NodeSRTConnector
from tlpf_toolkit.node import batchOffsetParentMatrixConnector

from tlpf_toolkit.locator import LocatorFunctions

from tlpf_toolkit.joint import JointFunctions

from tlpf_toolkit.skin import SkinFunctions

from tlpf_toolkit.attr import VisibilityAttributFunctions
from tlpf_toolkit.attr import RotationOrderAttributeFunctions

from tlpf_toolkit.ctrlShapes import color as ctl_color
from tlpf_toolkit.ctrlShapes import core as ctl_core
from tlpf_toolkit.ctrlShapes import functions as ctl_func
from tlpf_toolkit.ctrlShapes import transform as ctl_trans

from tlpf_toolkit.curves import CurveFunctions


from tlpf_toolkit.builds.BabyGroot_rig import plates
from tlpf_toolkit.builds.BabyGroot_rig import utilityFunctions
from tlpf_toolkit.builds.BabyGroot_rig import build





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
            icon=ICON_DIR + "/V003/reloadShelf.png",
            command=lambda: reload_shelf(shelf_name=SHELF_NAME),
        )

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V003/utils.png")
        utilityMenu = cmds.popupMenu(b=1)

        shapesSubmenu = self.addSubMenu(utilityMenu, "Shape Functions")

        self.addMenuItem(shapesSubmenu, "Parent Shapes", command=lambda _: ShapeParentFunction.shapeParentMultiUI())

        self.addMenuItem(shapesSubmenu, "Instance Shape", command=lambda _: ShapeInstanceFunction.shapeParentInstance())

        self.addMenuItem(shapesSubmenu, "Shape Replace", command=lambda _: ShapeParentFunction.ShapeReplace())

        self.addMenuItem(utilityMenu, "Parent Only", command="cmds.duplicate(parentOnly=True)")

        self.addMenuItem(utilityMenu, "LRA", command="for i in cmds.ls(selection=True): cmds.toggle(i, la=True)")

        self.addMenuItem(utilityMenu, "SRT To OffsetParnet Matrix", command=lambda _: ZeroOffsetFunction.ClearTransformsToOffsetParentMatrix())
        
        parentSubMenu = self.addSubMenu(utilityMenu, "Parenting")

        self.addMenuItem(parentSubMenu, "MultiParent In Order", command=lambda _: GeneralFunctions.multiParentInOrderUI())

        self.addMenuItem(parentSubMenu, "MultiParent Batch", command=lambda _: GeneralFunctions.batchMultiParentUI())
        
        self.addMenuItem(utilityMenu, "Select Transformed Objects", command=lambda _: GeneralFunctions.selectNoneZeroTransforms())
        
        self.addMenuItem(utilityMenu, "Set Display Type to Normal ", command=lambda _: GeneralFunctions.setSelectionDisplayTypeNormal())

        utilityNodeInputSubmenu = self.addSubMenu(utilityMenu, "SetNodeInput")

        self.addMenuItem(utilityNodeInputSubmenu, "0", command = lambda _: GeneralFunctions.setNodeInputToZero())
        self.addMenuItem(utilityNodeInputSubmenu, "1", command = lambda _: GeneralFunctions.setNodeInputToOne())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")


        self.addButton(label="", icon=ICON_DIR + "/V003/name.png", command=NamingFunctions.BatchRenameABCUI)

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V003/match.png")
        transformMatchingMenu = cmds.popupMenu(b=1)

        self.addMenuItem(transformMatchingMenu, "match All", command=lambda _: MatchTransformFunction.matchAll())

        self.addMenuItem(transformMatchingMenu, "match Translation", command=lambda _: MatchTransformFunction.matchTranslation())

        self.addMenuItem(transformMatchingMenu, "match Rotation", command=lambda _: MatchTransformFunction.matchRotation())

        self.addMenuItem(transformMatchingMenu, "match Scale", command=lambda _: MatchTransformFunction.matchScale())
        
        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V003/zero.png")
        zeroMenu = cmds.popupMenu(b=1)

        self.addMenuItem(zeroMenu, "Sam Zero", command=lambda _: ZeroOffsetFunction.insertNodeBefore())

        self.addMenuItem(zeroMenu, "Tim Zero", command=lambda _: ZeroOffsetFunction.TimZeroUserConfig())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        #IKFK Menu
        self.addButton(label="", icon=ICON_DIR + "/V003/ikfk.png" , command="")
        IkFkMenu = cmds.popupMenu(b=1)

        self.addMenuItem(IkFkMenu, "Auto IKFK Chain", command=lambda _: IkFkSwitch.IKFKConfigurationInterface())

        self.addMenuItemDivider(IkFkMenu, divider=True, dividerLabel="UTILITY")
        
        self.addMenuItem(IkFkMenu, "Add Soft IK", command=lambda _: IkFkSwitch.SoftIKConfigInterface())

        self.addMenuItem(IkFkMenu, "Create Single IKFK Blend", command=lambda _: IkFkSwitch.CreateSinlgeIKFKBlend())

        self.addMenuItem(IkFkMenu, "Create Multi IKFK Blend", command=lambda _: IkFkSwitch.CreateMultiIKFKBlendUI())

        #PoleVector Menu
        self.addButton(label="", icon=ICON_DIR + "/V003/poleVector.png", command="")
        poleVectorMenu = cmds.popupMenu(b=1)

        self.addMenuItem(poleVectorMenu, "Simple PV", command=lambda _: PoleVectorFunction.createSimplePoleVector())

        self.addMenuItem(poleVectorMenu, "PV Line", command=lambda _: PoleVectorFunction.createPoleVectorLine())

        #Revers Chain
        #self.addButton(label="", icon=ICON_DIR + "/V002/RevChain.png" ,command= ReverseFootSetup.createReverseChain)

        #Stretch Setup
        self.addButton(label="", icon=ICON_DIR + "/V003/stretch.png" ,command=SimpleStretchSetup.SimpleStretchSetupConfigInterface)

        #Twist Menu
        self.addButton(label="", icon=ICON_DIR + "/V003/twist.png", command="")
        twistMenu = cmds.popupMenu(b=1)

        self.addMenuItem(twistMenu, "Twist Joints", command=lambda _: TwistJoints.twistSetupConfigInterface())

        self.addMenuItem(twistMenu, "Twist Setup", command=lambda _: TwistJoints.MatrixForwardTwistSetup())



        #Twist Menu
        self.addButton(label="", icon=ICON_DIR + "/V003/lip.png", command="")
        lipMenu = cmds.popupMenu(b=1)

        self.addMenuItem(lipMenu, "Sam Lip Setup", command=lambda _: LipSetup.SamLipSetupUI())
        self.addMenuItem(lipMenu, "Arturo Coso Setup", command=lambda _: LipSetup.createArturoCosoLipSetupUI())


        #Eyelid Setup
        self.addButton(label="", icon=ICON_DIR + "/V003/eye.png")
        EyeMenu = cmds.popupMenu(b=1)

        self.addMenuItem(EyeMenu, "Eyelid Base", command = lambda _: EyeLidSetup.EyelidConfigWindow())

        #Spline Setup
        self.addButton(label="", icon=ICON_DIR + "/V003/spline.png", command="")
        splineMenu = cmds.popupMenu(b=1)

        self.addMenuItem(splineMenu, "Simple Spline", command= lambda _: SplineSystem.NeckSplineIKConfigUI())
        

        #Space Swapping
        self.addButton(label="", icon=ICON_DIR + "/V003/space.png", command="")
        spaceMenu = cmds.popupMenu(b=1)

        self.addMenuItem(spaceMenu, "Matrix SpaceSwap", command= lambda _: SpaceSwapping.MatrixSpaceSwitch())
        
        self.addButton(label="", icon=ICON_DIR + "/V003/revFoot.png", command="")
        revFootMenu = cmds.popupMenu(b=1)

        self.addMenuItem(revFootMenu, "RevFoot Setup V001", command= lambda _: ReverseFootSetup.revFootSetup01ConfigUI())

        #Ribbon
        self.addButton(label="", icon=ICON_DIR + "/V003/ribbon.png", command="")
        ribbonMenu = cmds.popupMenu(b=1)

        self.addMenuItem(ribbonMenu, "Guided Ribbon", command= lambda _: RibbonSetup.guidedRibbonUI())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")
        
        #Jiggle Menu
        self.addButton(label="", icon=ICON_DIR + "/V003/dynamics.png")
        dynamicsMenu = cmds.popupMenu(b=1)

        self.addMenuItem(dynamicsMenu, "Sam Jiggle Setup", command=lambda _: JiggleSetup.createSamJiggleSetup())

        self.addMenuItem(dynamicsMenu, "Tim Jiggle Setup", command=lambda _: JiggleSetup.TimJiggleSetupConfigInterface())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V003/color.png" ,command=CtrlColorFunction.ColorSettingWindow)
 

        self.addButton(label="", icon=ICON_DIR + "/V003/ctrls.png")
        ctrlsMenu = cmds.popupMenu(b=1)

        self.addMenuItem(ctrlsMenu, "Circle Ctrls - Hirarchy", command=lambda _: CreateBasicCtls.CreateCircleCtrlsHirarchyUserInput())

        self.addMenuItem(ctrlsMenu, "Circle Ctrls - Flat", command=lambda _: CreateBasicCtls.CreateCircleCtrlsUserInput())
        
        ctrlMirrorSubMenu = self.addSubMenu(ctrlsMenu, "Ctrl Mirroring")
        
        self.addMenuItem(ctrlMirrorSubMenu, "Scale Based Ctrls Mirror", command=lambda _: CtrlMirror.MirrorCtrlsBehaviorUserInput())
        
        self.addMenuItem(ctrlMirrorSubMenu, "Joint Based Ctrl Mirror", command=lambda _: CtrlMirror.mirrorCtrlsJointsMethodUI())

        #=======================================
        ## DISCLAIMER - Credit for the Following 
        # Menu goes to Tim Colemen and Martin Lanton From CGMA 
        # and there MechRig Toolkit Repsoitory - https://github.com/martinlanton/mechRig_toolkit
        #=======================================
        # Anim Control Tools
        self.addButton(label="", icon=ICON_DIR + "/V003/shapes.png")
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
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V003/matrix.png", command="")
        MatrixMenu = cmds.popupMenu(b=1)

        self.addMenuItem(MatrixMenu, "Matrix Zero Offset", command=lambda _: MatrixZeroOffset.iterateCreateMatrixZeroOffset())
        self.addMenuItem(MatrixMenu, "Matrix Drv Offset", command=lambda _: MatrixZeroDrvOffset.createMatrixDrvOffset())
        self.addMenuItem(MatrixMenu, "Ball Joint Corrective Tool", command = lambda _: CorrectiveMatrixSetup.ballJointCorrectiveSystemUI())
        self.addMenuItem(MatrixMenu, "Hinge Joint Corrective Tool", command = lambda _: CorrectiveMatrixSetup.hingeJointCorrectiveSystemUI())
        self.addMenuItem(MatrixMenu, "Matrix Constraint to Joint", command = lambda _: MatrixConstraints.matrixConstraintsToJointsUI())
        self.addMenuItem(MatrixMenu, "Reset Parent offset Matrix", command = lambda _: MatrixFunctions.resetOffsetParentMatrix())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V003/node.png", command="")
        NodeMenu = cmds.popupMenu(b=1)

        self.addMenuItemDivider(NodeMenu, divider=True, dividerLabel="MULTI CONNECTOR")

        self.addMenuItem(NodeMenu, "1 zu N MultiConnect Filtered", command=lambda _: MultiConnectFunction.MultiConnectOneToNConfigurationInterfaceFiltered())

        self.addMenuItem(NodeMenu, "1 zu N MultiConnect All", command=lambda _: MultiConnectFunction.MultiConnectOneToNConfigurationInterfaceAll())

        self.addMenuItem(NodeMenu, "M zu N MultiConnect Filtered", command=lambda _: MultiConnectFunction.MultiConnectMToNConfigurationInterfaceFiltered())

        self.addMenuItem(NodeMenu, "M zu N MultiConnect All", command=lambda _: MultiConnectFunction.MultiConnectMToNConfigurationInterfaceAll())

        self.addMenuItem(NodeMenu, "Batch Connect WorldMatrix to OffsetParent Matrix", command=lambda _: batchOffsetParentMatrixConnector.connectOffsetParentMatrixBatchUI())

        self.addMenuItemDivider(NodeMenu, divider=True, dividerLabel="SRT Connector")
        
        self.addMenuItem(NodeMenu, "Connect SRT", command= lambda _: NodeSRTConnector.ConnectSRT())

        self.addMenuItem(NodeMenu, "Connect Translate", command= lambda _: NodeSRTConnector.ConnectTranslate())

        self.addMenuItem(NodeMenu, "Connect Rotate", command= lambda _: NodeSRTConnector.ConnectRotate())

        self.addMenuItem(NodeMenu, "Connect Scale", command= lambda _: NodeSRTConnector.ConnectScale())

        self.addMenuItemDivider(NodeMenu, divider=True, dividerLabel="UTILITY")

        self.addMenuItem(NodeMenu, "Distance Bewteen", command=lambda _: CreateDistanceBetween.createDistance())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        #Multi Constraining
        self.addButton(label="", icon=ICON_DIR + "/V003/multConstrain.png")
        multiConstraining_menu = cmds.popupMenu(b=1)

        ##Adding all menu items for Multi Constraining
        self.addMenuItemDivider(multiConstraining_menu, divider=True, dividerLabel="CHOOSE CONSTRAINT TYPE")

        self.addMenuItem(multiConstraining_menu, "Parent Constraint", command=lambda _: MultiConstraintFunction.MultiParentConstraintConfig())

        self.addMenuItem(multiConstraining_menu, "Orient Constraint", command=lambda _: MultiConstraintFunction.MultiOrientConstraintConfig())

        self.addMenuItem(multiConstraining_menu, "Scale Constraint", command=lambda _: MultiConstraintFunction.MultiScaleConstraintConfig())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V003/locator.png")
        LocatorMenu = cmds.popupMenu(b=1)

        self.addMenuItem(LocatorMenu, "Create Loc at Seleceted Pos", command=lambda _: LocatorFunctions.selected_points())

        self.addMenuItem(LocatorMenu, "Create Loc at CENTER of Selected", command=lambda _: LocatorFunctions.center_selection_weighted_average())

        self.addMenuItem(LocatorMenu, "Create Loc Aimed at Selected", command=lambda _: LocatorFunctions.aim_selection())

        self.addMenuItem(LocatorMenu, "Create Loc at Loc/Rot", command=lambda _: LocatorFunctions.create_locator_snap())

        self.addMenuItem(LocatorMenu, "Add Inbetween Locators", command=lambda _: LocatorFunctions.createInbetweenLocators())
        
        self.addMenuItem(LocatorMenu, "Rivet Locator", command=lambda _: LocatorFunctions.buildRivetUIConfig())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V003/joints.png")
        JointMenu = cmds.popupMenu(b=1)

        self.addMenuItem(JointMenu, "Create Joint at Selection", command=lambda _: JointFunctions.CreateJointsOnSelected())

        self.addMenuItem(JointMenu, "Move Joint SRT to Matrix", command=lambda _: JointFunctions.MoveJointSRTtoParentMatrixOffset())

        self.addMenuItem(JointMenu, "Clear Joint Orients", command=lambda _: JointFunctions.ClearJointOrientValues())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        self.addButton(label="", icon=ICON_DIR + "/V003/skin.png")
        SkinMenu = cmds.popupMenu(b=1)

        self.addMenuItem(SkinMenu, "Transfer SkinCluster", command=lambda _: SkinFunctions.do_transfer_skin())

        self.addMenuItem(SkinMenu, "Transfer SkinCluster Between Namespaces", command=lambda _: SkinFunctions.NamespaceSkinClusterTransferConfigInterface())
        
        self.addMenuItemDivider(SkinMenu, divider=True, dividerLabel="IMPORT/EXPORT")

        self.addMenuItem(SkinMenu, "Export SkinWeights", command=lambda _: SkinFunctions.export_skin_weights_selected())

        self.addMenuItem(SkinMenu, "Import SkinWeights", command=lambda _: SkinFunctions.import_skin_weights_selected())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        #Attribute Menu
        self.addButton(label="", icon=ICON_DIR + "/V003/attr.png")
        AttrMenu = cmds.popupMenu(b=1)

        self.addMenuItemDivider(AttrMenu, divider=True, dividerLabel="VISIBILITY ATTR")

        self.addMenuItem(AttrMenu, "Add Visibility Attr", command=lambda _: VisibilityAttributFunctions.CreateHiddenVisibilityAttributeConfigUI())

        self.addMenuItemDivider(AttrMenu, divider=True, dividerLabel="LOCK/UNLOCK")

        self.addMenuItem(AttrMenu, "Lock Default Attributes", command=lambda _: VisibilityAttributFunctions.lock_unlock_channels(True))

        self.addMenuItem(AttrMenu, "Unlock Default Attributes", command=lambda _: VisibilityAttributFunctions.lock_unlock_channels(False))

        self.addMenuItemDivider(AttrMenu, divider=True, dividerLabel="UTILITY")

        self.addMenuItem(AttrMenu, "Add Attribute Divider", command=lambda _: VisibilityAttributFunctions.CreateAttributeDividerConfigUI())

        self.addMenuItem(AttrMenu, "Copy Attributes Over", command=lambda _: VisibilityAttributFunctions.CopyAttributesToSelectionConfigUI())

        self.addMenuItem(AttrMenu, "Hide from ChannelBox", command=lambda _: VisibilityAttributFunctions.hideNodeFromChannelboxHistory())

        self.addMenuItemDivider(AttrMenu, divider=True, dividerLabel="ROTATE ORDER")

        self.addMenuItem(AttrMenu, "Set Rotation Order", command=lambda _: RotationOrderAttributeFunctions.setRotationOrderUI())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        #Curve Menu
        self.addButton(label="", icon=ICON_DIR + "/V003/curve.png")
        curveMenu = cmds.popupMenu(b=1)

        self.addMenuItem(curveMenu, "Snap to Closest Curve Point", command=lambda _: CurveFunctions.snapSelectionToClosestCurvePoint())
        
        self.addMenuItem(curveMenu, "Create Curve from Selection", command=lambda _: CurveFunctions.createLinearCurveFromSelectionConfig())

        # Separator
        self.addButton(label="", icon=ICON_DIR + "/V003/sep.png", command="")

        #Curve Menu
        self.addButton(label="", icon=ICON_DIR + "/V003/rigs.png")
        rigsMenu = cmds.popupMenu(b=1)

        babyGrootSubMenu = self.addSubMenu(rigsMenu, "BabyGroot")

        self.addMenuItem(babyGrootSubMenu, "Build BabyGroot", command= lambda _: build.build_BabyGroot_Rig())
        self.addMenuItem(babyGrootSubMenu, "Parent Ctrl via Mtrx", command= lambda _: utilityFunctions.parentVineCtrlToBendy())
        self.addMenuItem(babyGrootSubMenu, "ConnectVisibilit Remap", command= lambda _: utilityFunctions.connectVisibilityRemap())
        self.addMenuItem(babyGrootSubMenu, "resetOffsetParentMatrix", command= lambda _: utilityFunctions.resetOffsetParentMatrix())
        self.addMenuItem(babyGrootSubMenu, "Plate Module", command = lambda _: plates.platesInput())

        

        

        

        
        