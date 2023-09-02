#Modules Import
import maya.cmds as cmds


#=======================================
## Twist Joints Function
#=======================================
def twistSetupConfigInterface():
    #create window and store
    configWindow = cmds.window(title="TwistJoints", iconName="TwistJoints", widthHeight=(200, 55), sizeable=True)

    #set layout
    cmds.rowColumnLayout( adjustableColumn=True )

    #create label
    cmds.text(label="Select number of Twist Joints")

    #create visible variable to show how many joints will be created based on user input
    global label
    label = cmds.text(label="0")

    #create slider for twist joint amount selection by user
    slider = cmds.floatSlider(min=0, max=30, value=0, step=1, changeCommand=update_label)

    #button for executing the function to build the twist joints
    cmds.button(label="Create Twist Joints", command=lambda _:createTwistSetup(cmds.floatSlider(slider, query=True, value=True)))

    #build and show the window
    cmds.showWindow(configWindow)



#function to set the new user input into the label of how many twist joints are selected
def update_label(value):
    cmds.text(label, edit=True, label=str(int(value)))

#main function to order the creation of the twist joints
def createTwistSetup(_numberOfJoints):

    #store user selection number of twist joint in local variable
    numberOfJoints = int(_numberOfJoints)
    
    #get user selected joints
    sel = cmds.ls(selection=True)

    #store selection beginning and end into different variables
    p1 = sel[0]
    p2 = sel[1]

    #store parent name string
    name = "".join(p1)

    #create the Individual twist joint and store there returned selector list in a variable
    twistJoints = createJoints(numberOfJoints, name, p1)

    #create two lists with the different weight values to later drive the constraint nodes weights
    weights01 , weights02 = getWeights(numberOfJoints)

    #create the constraints for each twist joint
    createTwistJointPointConstraints(twistJoints, p1, p2, weights01, weights02)

    #parent the twist joint under the Parent joint
    parentTwistJoints(twistJoints, p1)


#Function to parent a list of objects to a different given Object
def parentTwistJoints(_twistJoinst, _p1):
    for i in _twistJoinst:
        cmds.parent(i, _p1)

#Function to create the joints to function as twist joints
def createJoints(_numberOfJoints, _name, _p1):
    #return List of the selectors for later use
    twistJoints = []

    #joint creation
    for i in range(_numberOfJoints):
        cmds.select(clear=True)
        newJoint = cmds.rename(cmds.joint(), _name + "_Twist")

        #matching Transforms to parent
        cmds.matchTransform(newJoint, _p1)

        #freezing translations
        cmds.makeIdentity(newJoint, apply=True, rotate=True, translate=True, scale=True)

        #add joints to return List
        twistJoints.append(newJoint)

    #return Joint selector list
    return twistJoints
        
#Function taking a list of object, two parent objects and two weight lists
def createTwistJointPointConstraints(_twistJoints, _p1, _p2, _weights01, _weights02):
    for i in range(len(_twistJoints)):
        #create the constraints
        pointConstraint = cmds.pointConstraint(_p1, _p2, _twistJoints[i])

        #set weights for ech constraint
        cmds.setAttr(pointConstraint[0] + "." + _p1 + "W0", _weights02[i])
        cmds.setAttr(pointConstraint[0] + "." + _p2 + "W1", _weights01[i])

#Function to receive two list 
def getWeights(_numberOfJoints):

    #initilize two lists to store the weights
    weights01 = []
    weights02 = []

    
    for i in range(_numberOfJoints - 1):

        #caluculate the first list of weights
        weight = (i + 1) / (_numberOfJoints - 1)

        #push the weight into its corresponding list
        weights01.append(round(weight, 2))

    #set the last weight to be 0.95
    for i in range(len(weights01)):
        if weights01[i] == 1:
            weights01[i] = 0.95
    #set the lowest weight in the weight list
    weights01.insert(0, 0.05)

    #invert weights and put them into the weights2 list
    for i in weights01:
        weights02.append(round(abs(i - 1),2))
        
    #return both weight lists
    return weights01, weights02
#=======================================
## Twist Joints Function - ENd
#=======================================