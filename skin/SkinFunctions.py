
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


##=======================================
## Transfer SkinKluster between Namespaces
##=======================================

##Interface to Select the Namespaces that will be used to transfer the SkinCluster between
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


def getselectedNamespaces(_NamespaceInputs):
    selectedNamespaces = []
    for i in _NamespaceInputs:
        color = cmds.text(i, query=True, backgroundColor=True)

        color[0] = round(color[0], 1)
        color[1] = round(color[1], 1)
        color[2] = round(color[2], 1)

        if color == [0.3, 0.8, 0.2]:
            selectedNamespaces.append(cmds.text(i, query=True, label=True))
    return selectedNamespaces

def getComparedNamespaceObjects(_listA, _listB):
    resultList = []

    for i in _listA:
        for j in _listB:
            if i == j:
                resultList.append([i, j])

    return resultList

def getPrefixStrippedNamespaceContents(_namespace, prefix):
    resultList = []
    for i in _namespace:
        resultList.append(i.replace(prefix + ":", ""))
    return resultList

def getSourceNamespace(refObjectA, refObjectB, namespaceNameA, namespaceNameB):

    AOBjectSkinCluster = mel.eval('findRelatedSkinCluster("{}")'.format(refObjectA[0]))

    BOBjectSkinCluster = mel.eval('findRelatedSkinCluster("{}")'.format(refObjectB[0]))

    log.info("SkinCluster A: {}".format(AOBjectSkinCluster))
    log.info("SkinCluster B: {}".format(BOBjectSkinCluster))
    
    log.info("Ref Object A : {}".format(refObjectA))
    log.info("Ref Object B : {}".format(refObjectB))
    
    
    if AOBjectSkinCluster:
        if namespaceNameA in refObjectA[0]:
            return namespaceNameA
        elif namespaceNameB in refObjectA[0]:
            return namespaceNameB
    elif BOBjectSkinCluster:
        if namespaceNameA in refObjectB[0]:
            return namespaceNameA
        elif namespaceNameB in refObjectB[0]:
            return namespaceNameB
    else:
        return "NO Skincluster Detected"


def getParentObjectsFromList(targetList):
    parentList = []

    log.info("TargetList: {}".format(targetList))

    for i in targetList:
        
        cmds.select(clear=True)
        cmds.select(i[0])
        newFirstParentEntry = cmds.pickWalk(direction="Up")
        
        cmds.select(clear=True)
        cmds.select(i[1])
        newSecondParentEntry = cmds.pickWalk(direction="Up")

        parentList.append([newFirstParentEntry, newSecondParentEntry])

    return parentList


def TransferSkinlusterBetweenNamespaceModels(_NamespaceInputs):

    selectedNamespaces = getselectedNamespaces(_NamespaceInputs)

    log.info("Selected Namespaces: {}".format(selectedNamespaces))
    log.info("Namespace List Lenght: {}".format(len(selectedNamespaces)))

    if len(selectedNamespaces) == 2:
        NamespaceAObjects = cmds.namespaceInfo(selectedNamespaces[0], listNamespace=True)
        NamespaceBObjects = cmds.namespaceInfo(selectedNamespaces[1], listNamespace=True)
        

        log.info("Namespace A Contents: {}".format(NamespaceAObjects))
        log.info("Namespace B Contents: {}".format(NamespaceBObjects))

        # Filter Only the Mesh Shapes from the Out of the Namspace Contents

        cmds.select(clear=True)

        cmds.select(NamespaceAObjects)

        NamespaceAMesh = cmds.findType(deep=False, type="mesh")

        cmds.select(clear=True)

        cmds.select(NamespaceBObjects)

        NamespaceBMesh = cmds.findType(deep=False, type="mesh")
        
        cmds.select(clear=True)

        NamespaceAMesh = getPrefixStrippedNamespaceContents(NamespaceAMesh, selectedNamespaces[0])

        NamespaceBMesh = getPrefixStrippedNamespaceContents(NamespaceBMesh, selectedNamespaces[1])

        log.info("Namespace A Mesh Content: {}".format(NamespaceAMesh))
        log.info("Namespace B Mesh Content: {}".format(NamespaceBMesh))

        MatchedNamespaceObjects = getComparedNamespaceObjects(NamespaceAMesh, NamespaceBMesh)

    
        for i in range(len(MatchedNamespaceObjects)):
            MatchedNamespaceObjects[i][0] = selectedNamespaces[0] + ":" + MatchedNamespaceObjects[i][0]
            MatchedNamespaceObjects[i][1] = selectedNamespaces[1] + ":" + MatchedNamespaceObjects[i][1]

        MatchedNamespaceObjects = getParentObjectsFromList(MatchedNamespaceObjects)

        sourceNamespace = getSourceNamespace(MatchedNamespaceObjects[0][0], MatchedNamespaceObjects[0][1], selectedNamespaces[0], selectedNamespaces[1])

        log.info("Matched Namespace Objects: {}".format(MatchedNamespaceObjects))
        log.info("Source Namespace: {}".format(sourceNamespace))
        if sourceNamespace == None or sourceNamespace == "NO Skincluster Detected":
            log.error("No Source Skincluster Detected")
        else:
            if sourceNamespace == selectedNamespaces[0]:
                for i in MatchedNamespaceObjects:
                    transfer_skin(i[0][0], i[1][0])
            elif sourceNamespace == selectedNamespaces[1]:
                for i in MatchedNamespaceObjects:
                    transfer_skin(i[1][0], i[0][0])
    else:
        log.warning("The Number of Namespace u can select to transfer SKincluster needs to be 2!!")

##=======================================
## Transfer SkinKluster between Namespaces - END
##=======================================