#Module Import
import maya.cmds as cmds
import string

ALPHABET = list(string.ascii_uppercase)

#=======================================
## Add Suffix Function
#=======================================
def SuffixConfigurationWindow():
 #basic Window creation
    configWindow = cmds.window(title="Suffix", iconName='Suffix', widthHeight=(200, 55), sizeable=True)
    
    #Window Layout
    cmds.rowColumnLayout( adjustableColumn=True )
    
    #Label
    cmds.text( label='Enter Suffix' )
    
    #Input Field Sotring the Stirng value
    name = cmds.textField()
    
    #Building the switch execution button
    cmds.button( label='OK', command=lambda _: suffixSelected(cmds.textField(name, query=True, text=True)))
    

    #Display The window
    cmds.showWindow(configWindow)


def suffixSelected(_suffix):

    #get user Selection
    sel = cmds.ls(selection=True)

    #add suffix to the selected Items
    for i in sel:
        cmds.rename(i, i + _suffix)
#=======================================
## Add Suffix Function - END
#=======================================


def BatchRenameABCUI():

    windowWidth = 300

    batchRenameConfigWindow = cmds.window(title = "AbcRename", iconName="abcRename", widthHeight=(windowWidth, 600))

    cmds.rowColumnLayout( adjustableColumn=True ) 
    cmds.text(label="* as Placeholder for incrementation", align = "center", height= 20, backgroundColor = [.2, .2, .2])
    batchRenameInputString = cmds.textField(width = windowWidth, height=20 )

    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])

    cmds.button(label="RenameListABC", align = "center", width = 150, command = lambda _: BatchRenameABC(cmds.textField(batchRenameInputString, query = True, text = True)))

    cmds.button(label="RenameList123", align = "center", width = 150, command = lambda _: BatchRename123(cmds.textField(batchRenameInputString, query = True, text = True)))

    cmds.setParent('..')

    cmds.rowColumnLayout( adjustableColumn=True ) 
    #Space Divider
    cmds.text(label="", height=10)

    cmds.text(label="Replace Sides", height=20, backgroundColor = [.2, .2, .2])

    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])

    cmds.button(label="Replace L -> R", width = 150, command = lambda _: ReplaceLeftForRight())

    cmds.button(label="Replace R -> L", width = 150, command = lambda _: ReplaceRightForLeft())

    cmds.setParent('..')
    cmds.rowColumnLayout( adjustableColumn=True ) 

    #Space Divider
    cmds.text(label="", height=10)

    cmds.text(label="Replace Last", height=20, backgroundColor = [.2, .2, .2])

    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])

    cmds.button(label="Delete Last",width = 150,  command = lambda _: ReplaceLast())
    cmds.button(label="Delete First", width = 150, command = lambda _: ReplaceFirst())

    cmds.setParent('..')
    cmds.rowColumnLayout( adjustableColumn=True ) 

    #Space Divider
    cmds.text(label="", height=10)

    cmds.text(label="Suffix", height=20, backgroundColor = [.2, .2, .2])

    suffixInputString = cmds.textField(width = windowWidth, height=20 )
    
    cmds.button(label="Suffix Selected", command = lambda _: suffixSelected(cmds.textField(suffixInputString, query=True, text=True)))
    
    
    cmds.text(label="", height=20)

    cmds.text(label="Prefix", height=20, backgroundColor = [.2, .2, .2])

    prefixInputString = cmds.textField(width = windowWidth, height=20 )

    cmds.button(label="Prefix Selected", command = lambda _: PrefixSelected(cmds.textField(prefixInputString, query=True, text=True)))

    #Space Divider
    cmds.text(label="", height=10)

    copyNameLabel = cmds.text(label="Copy Name to Target", height = 20, backgroundColor = [.3, .3, .3])
    instructionLabel = cmds.text(label = "Selecte Source --> Target")

    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])
    cmds.text(label = "Search Term", width = 150, height = 20, backgroundColor = [.3, .3, .3])
    cmds.text(label = "replace Term", width = 150, height = 20, backgroundColor = [.3, .3, .3])
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])
    searchTermInput = cmds.textField(width=150)
    replaceTermInput = cmds.textField(width = 150)
    cmds.setParent('..')
    cmds.rowLayout(numberOfColumns = 2, columnWidth2 = [150, 150])

    copyName = cmds.button(label = "Copy Name", width = 150, command = lambda _: copyNameSingle(cmds.textField(searchTermInput, query = True, text = True),
                                                                                   cmds.textField(replaceTermInput, query = True, text = True)))
    batchCopyName = cmds.button(label = "Copy Batch Name", width = 150, command = lambda _: copyNameBatch(cmds.textField(searchTermInput, query = True, text = True),
                                                                                   cmds.textField(replaceTermInput, query = True, text = True)))

    cmds.showWindow(batchRenameConfigWindow)

def copyNameBatch(searchTerm, replacement):
    selection = cmds.ls(sl=True)

    for item1, item2 in zip(selection[::2], selection[1::2]):
        cmds.rename(item2, f"{item1.replace(searchTerm, replacement)}")


def copyNameSingle(searchTerm, replacement):

    sourceNode = cmds.ls(sl = True)[0]
    targetNode = cmds.ls(sl=True)[1]

    cmds.rename(targetNode, f"{sourceNode.replace(searchTerm, replacement)}")

def PrefixSelected(_prefixInputString):
    selected = cmds.ls(selection=True)

    for i in selected:
        if _prefixInputString[-1] == "_":
            cmds.rename(i, _prefixInputString + i)
        else:
            cmds.rename(i, _prefixInputString + "_" + i)

def ReplaceLast():
    selection = cmds.ls(selection = True)

    for i in selection:
        cmds.rename(i, i[:-1])

def ReplaceFirst():
    selection = cmds.ls(selection = True)

    for i in selection:
        cmds.rename(i, i[1:])

def ReplaceLeftForRight():
    selection = cmds.ls(selection=True)

    for i in selection:
        cmds.rename(i, i.replace("l_", "r_"))

def ReplaceRightForLeft():
    selection = cmds.ls(selection=True)

    for i in selection:
        cmds.rename(i, i.replace("r_", "l_"))

def BatchRename123(inputString):
    selection = cmds.ls(selection=True)

    for i in range(len(selection)):
        cmds.rename(selection[i], inputString.replace("*", str(i)))

def BatchRenameABC(inputString):

    selection = cmds.ls(selection=True)

    for i in range(len(selection)):
        cmds.rename(selection[i], inputString.replace("*", ALPHABET[i]))


#=======================================
## batchRenameMenu - END
#=======================================