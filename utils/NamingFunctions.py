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

    batchRenameConfigWindow = cmds.window(title = "AbcRename", iconName="abcRename", widthHeight=(600, 200))

    cmds.rowColumnLayout( adjustableColumn=True ) 
    cmds.text(label="Type your Input Name string with a -*- at the location u want the Alphabetic ordering to start", align = "center", height= 20,
              backgroundColor = [.2, .2, .2])
    batchRenameInputString = cmds.textField(width = 400, height=20 )

    cmds.button(label="RenameListABC", align = "center", command = lambda _: BatchRenameABC(cmds.textField(batchRenameInputString, query = True, text = True)))

    cmds.button(label="RenameList123", align = "center", command = lambda _: BatchRename123(cmds.textField(batchRenameInputString, query = True, text = True)))

    cmds.showWindow(batchRenameConfigWindow)

    

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