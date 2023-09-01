'''A simple example of a custom marking menu in Maya. The benefits of doing it this way with Python are that
it is very flexible and easily maintainable. Additionally, you can keep it in a version control system.


This file is used for demonstration purposes, to be followed along with in this blog post
http://bindpose.com/custom-marking-menu-maya-python/


from user_toolkit.marking_menu import user_marking_menu
reload(user_marking_menu)
user_marking_menu.markingMenu()


*Use RMB + CTL + ALT to invoke marking menu
'''
import logging
LOG = logging.getLogger(__name__)

from maya import cmds
import pymel.core as pm
import pymel.api as api


MENU_NAME = "user_markingMenu"


class markingMenu():
    '''The main class, which encapsulates everything we need to build and rebuild our marking menu. All
    that is done in the constructor, so all we need to do in order to build/update our marking menu is
    to initialize this class.'''
    def __init__(self):

        self._removeOld()
        self._build()

    def _build(self):
        '''Creates the marking menu context and calls the _buildMarkingMenu() method to populate it with all items.'''
        menu = cmds.popupMenu(MENU_NAME, mm=1, b=3, aob=1, ctl=1, alt=1, sh=0, p="viewPanes", pmo=1, pmc=self._buildMarkingMenu)

    def _removeOld(self):
        '''Checks if there is a marking menu with the given name and if so deletes it to prepare for creating a new one.
        We do this in order to be able to easily update our marking menus.'''
        if cmds.popupMenu(MENU_NAME, ex=1):
            cmds.deleteUI(MENU_NAME)

    def _buildMarkingMenu(self, menu, parent):
        '''This is where all the elements of the marking menu our built.'''
        pm.popupMenu(MENU_NAME, e=True, dai=True)


        # Tool Launch Menu
        pm.menuItem(p=menu, l='Script Editor', c=pm.Callback(pm.mel.eval, 'ScriptEditor;'))
        pm.menuItem(p=menu, l='Node Editor', c=pm.Callback(pm.mel.eval, 'NodeEditorWindow;'))
        pm.menuItem(p=menu, l='Connection Editor', c=pm.Callback(pm.mel.eval, 'ConnectionEditor;'))
        pm.menuItem(p=menu, l='Outliner', c=pm.Callback(pm.mel.eval, 'OutlinerWindow;'))
        pm.menuItem(p=menu, d=True)
        pm.menuItem(p=menu, l='Paint Weights', c=pm.Callback(pm.mel.eval, 'ArtPaintSkinWeightsToolOptions;'))
        pm.menuItem(p=menu, d=True)

        # Rebuild
        cmds.menuItem(p=menu, l="Rebuild Marking Menu", c=rebuildMarkingMenu)

        # Build Sub-Radial Menus
        self._buildJointMenu(menu, parent)
        self._buildLocatorMenu(menu, parent)

    # W
    def _buildLocatorMenu(self, menu, parent):
        locMenu = pm.menuItem(p=menu, l='Locators', rp='W', subMenu=1)

        pm.menuItem(p=locMenu, l='Locator Command', c="")

    # E
    def _buildJointMenu(self, menu, parent):
        jntMenu = pm.menuItem(p=menu, l='Joints', rp='E', subMenu=1)

        pm.menuItem(p=jntMenu, l='Joint Command', c="")

def rebuildMarkingMenu(*args):
    '''This function assumes that this file has been imported in the userSetup.py
    and all it does is reload the module and initialize the markingMenu class which
    rebuilds our marking menu'''
    cmds.evalDeferred("""from mechRig_toolkit.marking_menu import mechRig_marking_menu;reload(mechRig_marking_menu);mechRig_marking_menu.markingMenu()""")
    LOG.info('Mech Rig Marking Menu reloaded successfully!')

markingMenu()
