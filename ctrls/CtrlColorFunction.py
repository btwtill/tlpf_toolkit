#Module Import
import maya.cmds as cmds


#=======================================
## CTRL Color Function
#=======================================

def ColorSettingWindow():

    #initilizing the window to pick the color
    configurationWindow = cmds.window(title="Animation Ctrl Color", iconName="CTRl Color", widthHeight=(200, 200), sizeable=True)

    #set Window Layout
    cmds.rowColumnLayout(adjustableColumn=True)

    #User Color Input
    color_widget_input = cmds.colorInputWidgetGrp( label='Color', rgb=(1, 0, 0) )

    doRecolorOutliner = cmds.checkBox(label="Recolor Zero Node in Outliner", value=False)

    #button to hand rgb value to function that executes the recoloring
    getColorButton = cmds.button(label="Set Color", command=lambda _: setCtrlShapeColorAttribute(cmds.colorInputWidgetGrp(color_widget_input, query=True, rgb=True), cmds.checkBox(doRecolorOutliner, query=True, value=True)))

    #Show the Configuration Window
    cmds.showWindow(configurationWindow)


def setCtrlShapeColorAttribute(_color, _recolorOutliner):
    colorRGB = _color

    sel = cmds.ls(sl = 1)

    for node in sel:
        #get shape Nodes
        shapes = cmds.listRelatives(node, s = 1)
        if shapes:
            for shp in shapes:
                try:
                    ## Add Color and Node Connection
                    cmds.setAttr(shp + '.overrideEnabled', 1)
                    cmds.setAttr(shp + '.overrideRGBColors', 1)
                    cmds.setAttr(shp + '.overrideColorR', colorRGB[0])
                    cmds.setAttr(shp + '.overrideColorG', colorRGB[1])
                    cmds.setAttr(shp + '.overrideColorB', colorRGB[2])

                    if _recolorOutliner:
                        
                        parentNode = cmds.listRelatives(node, parent=True)
                        parentNodeName = "".join(parentNode)
                        
                        cmds.setAttr(parentNodeName + ".useOutlinerColor", True)
                        cmds.setAttr(parentNodeName + ".outlinerColorR", colorRGB[0])
                        cmds.setAttr(parentNodeName + ".outlinerColorG", colorRGB[1])
                        cmds.setAttr(parentNodeName + ".outlinerColorB", colorRGB[2])
                        
                except:
                    pass
#=======================================
## CTRL Color Function - END
#=======================================