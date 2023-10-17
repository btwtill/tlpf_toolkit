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

    cmds.button(label="RenameListABC", align = "center", command = lambda _: BatchRenameABC(cmds.textField(batchRenameInputString, query = True, text = True)))

    cmds.text(label="", height=10)

    cmds.button(label="RenameList123", align = "center", command = lambda _: BatchRename123(cmds.textField(batchRenameInputString, query = True, text = True)))

    cmds.text(label="", height=20)

    cmds.text(label="Replace Sides", height=20, backgroundColor = [.2, .2, .2])

    cmds.button(label="Replace L -> R", command = lambda _: ReplaceLeftForRight())

    cmds.text(label="", height=10)

    cmds.button(label="Replace R -> L", command = lambda _: ReplaceRightForLeft())

    cmds.text(label="", height=20)

    cmds.text(label="Replace Last", height=20, backgroundColor = [.2, .2, .2])

    cmds.button(label="Delete Last", command = lambda _: ReplaceLast())

    cmds.text(label="", height=20)

    cmds.text(label="Suffix", height=20, backgroundColor = [.2, .2, .2])

    suffixInputString = cmds.textField(width = windowWidth, height=20 )
    
    cmds.button(label="Suffix Selected", command = lambda _: suffixSelected(cmds.textField(suffixInputString, query=True, text=True)))
    
    
    cmds.text(label="", height=20)

    cmds.text(label="Prefix", height=20, backgroundColor = [.2, .2, .2])

    prefixInputString = cmds.textField(width = windowWidth, height=20 )

    cmds.button(label="Prefix Selected", command = lambda _: PrefixSelected(cmds.textField(prefixInputString, query=True, text=True)))

    cmds.showWindow(batchRenameConfigWindow)

    

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