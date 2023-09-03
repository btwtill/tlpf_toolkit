
#=======================================
## Disclaimer
#  The following code is from the MechRig Toolkit Provided 
#  By Tim Coleman and Martin Lanton at CGMA and can be found on Github at 
#  https://github.com/martinlanton/mechRig_toolkit
#  Huge Thanks!!
#
#=======================================


#Module Import
import logging
import os

from maya import cmds, mel

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)




#=======================================
## Transfer Skin Cluster Function 
#=======================================
def do_transfer_skin():
    """Transfer skin of first selected object to second selected object"""

    selection = cmds.ls(selection=True)

    if len(selection) == 2:
        transfer_skin(selection[0], selection[1])
    else:
        log.error('Please select source and target object to transfer skin')
        return


def transfer_skin(source, target):
    """Transfer the skinning from source object to target object"""
    src_geom = source
    src_skin = mel.eval('findRelatedSkinCluster("{}")'.format(src_geom))

    if src_skin:
        src_infs = cmds.skinCluster(src_skin, query=True, influence=True)

        tgt_geom = target
        tgt_skin = mel.eval('findRelatedSkinCluster("{}")'.format(tgt_geom))
        if tgt_skin:
            cmds.delete(tgt_skin)
        tgt_skin = cmds.skinCluster(src_infs, tgt_geom, name=tgt_geom + '_skinCluster', toSelectedBones=True)[0]
        cmds.copySkinWeights(sourceSkin=src_skin, destinationSkin=tgt_skin, surfaceAssociation='closestPoint', influenceAssociation='oneToOne', noMirror=True, smooth=False)

        log.info('Successfully transferred skinning from {} to {}'.format(source, target))

    else:
        log.error('No skinCluster found on {}'.format(source))
        return
#=======================================
## Transfer Skin Cluster Function - END
#=======================================


#=======================================
## Import Skin weights on Selected
#=======================================
def import_skin_weights_selected():
    """Imports skin weights on selected meshes from Maya Project's "data" directory
    using Maya's deformerWeights command.

    Skin weights should be exported using the meshes name, for instance, the skin weight
    file for the mesh "cn_head_mesh" should be exported as "cn_head_mesh.xml'

    If a skin weight file is not found, the process is skipped without error
    """
    PROJ_PATH = cmds.workspace(query=True, rd=True)
    DATA_PATH = PROJ_PATH + 'data/'

    selection = cmds.ls(selection=True)
    if selection:
        for mesh in selection:
            # Check if there's a skin cluster on mesh
            sc = mel.eval('findRelatedSkinCluster("{}")'.format(mesh))
            if sc:
                # Check if the skin weight xml file exist
                if os.path.exists(DATA_PATH+"{}.xml".format(mesh)):
                    cmds.deformerWeights("{}.xml".format(mesh), im=True, method='index', deformer=sc, path=DATA_PATH)
                    cmds.skinCluster(sc, edit=True, forceNormalizeWeights=True)
                    log.info('Imported skin weight file {}'.format((DATA_PATH + "{}.xml".format(mesh))))
                else:
                    log.warning('No skin weight XML file found for {}'.format(mesh))
            else:
                log.warning('No skin cluster found on {}'.format(mesh))
#=======================================
## Import Skin weights on Selected - END
#=======================================


#=======================================
## Export Skin weights on Selected
#=======================================
def export_skin_weights_selected():
    """Exports skin weights on selected meshes to Maya Project's "data" directory
    using Maya's deformerWeights command.

    Skin weights are exported using the meshes name, for instance, the skin weight
    file for the mesh "cn_head_mesh" would be exported as "cn_head_mesh.xml'

    If a skin cluster is not found on a mesh, the process is skipped without error
    """
    PROJ_PATH = cmds.workspace(query=True, rd=True)
    DATA_PATH = PROJ_PATH + 'data/'

    selection = cmds.ls(selection=True)
    if selection:
        for mesh in selection:
            # Check if there's a skin cluster on mesh
            sc = mel.eval('findRelatedSkinCluster("{}")'.format(mesh))
            if sc:
                # Check if the skin weight xml file exist
                if os.path.exists(DATA_PATH):
                    cmds.deformerWeights("{}.xml".format(mesh), export=True, method='index', deformer=sc, path=DATA_PATH)
                    log.info('Exported skin weight data to {}'.format((DATA_PATH + "{}.xml".format(mesh))))
                else:
                    log.warning('No data directory found under {} to save skin weight file to'.format(PROJ_PATH))
            else:
                log.warning('No skin cluster found on {}'.format(mesh))
#=======================================
## Export Skin weights on Selected - END
#=======================================