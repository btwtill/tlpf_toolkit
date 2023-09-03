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