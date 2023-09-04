#Module Import
import maya.cmds as cmds


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