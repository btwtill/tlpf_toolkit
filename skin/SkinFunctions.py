
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



##=======================================
## Disclaimer END
##=======================================



def NamespaceSkinClusterTransferConfigInterface():
    configwindow = cmds.window(title="NamespaceSkinTransfer", widthHeight= (220, 50), sizeable=True)

    cmds.rowColumnLayout( adjustableColumn = True)

    AllNamespaces = cmds.namespaceInfo(listOnlyNamespaces=True)

    if "UI" in AllNamespaces:
        AllNamespaces.remove("UI")
    if "shared" in AllNamespaces:
        AllNamespaces.remove("shared")

    NamespaceInputList = []


    for i in range(len(AllNamespaces)):
        counter = str(i)
        cmds.text(label="Namespace " + counter, height=30)
        newNamesSpaceInput = buildUserInputGrp("set Namespace: " + AllNamespaces[i], "Not Jet Set", 30, AllNamespaces[i])
        NamespaceInputList.append(newNamesSpaceInput)

    cmds.button(label="Transfer Skincluster", command=lambda _: TransferSkinlusterBetweenNamespaceModels(NamespaceInputList))

    cmds.showWindow(configwindow)


def buildUserInputGrp(buttonLabel, displayLabelText, displayLabelHeight, _NamespaceName):
    cmds.text(label="", height=10, backgroundColor=[0.0,0.0,0.0])
    cmds.button(label=buttonLabel, height=40, command=lambda _: updateLabel(labelname, _NamespaceName))
    labelname = cmds.text(label=displayLabelText, height=displayLabelHeight, backgroundColor=[0.6, 0.1, 0.1])
    return labelname

def updateLabel(_label, _newLabelText):
    rgbColor = [0.3, 0.8, 0.2]
    cmds.text(_label, edit=True, label=_newLabelText, backgroundColor=rgbColor)

def getValidNamespaces(_NamespaceInputs):
    ValidNamespaces = []
    for i in _NamespaceInputs:
        color = cmds.text(i, query=True, backgroundColor=True)

        color[0] = round(color[0], 1)
        color[1] = round(color[1], 1)
        color[2] = round(color[2], 1)


        if color == [0.3, 0.8, 0.2]:
            ValidNamespaces.append(cmds.text(i, query=True, label=True))
    return ValidNamespaces

def TransferSkinlusterBetweenNamespaceModels(_NamespaceInputs):
    validNamespaces = getValidNamespaces(_NamespaceInputs)
    print(validNamespaces)
    if len(validNamespaces) <= 2 or len(validNamespaces) != 0:

        NamespaceAObjects = []
        for i in validNamespaces:
            NamespaceAObjects.append(cmds.namespaceInfo(i, listNamespace=True))
            # TODO Filter for only Mesh Objects --> onlyMesh = [i for i in sel if "_MeshShape" in i] 
        print(NamespaceAObjects)
        
    print(validNamespaces)
