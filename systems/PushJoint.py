import maya.cmds as cmds


from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets

from tlpf_toolkit import global_variables

class pushJoint(QtWidgets.QWidget):

    def __init__(self, parent = None):


        super(pushJoint, self).__init__(parent=parent)

        self.setWindowFlags(QtCore.Qt.Window)

        #load UI File
        self.widgetPath = global_variables.CURRENT_DIRECTORY + "/ui/QtUIs/"

        self.widget = QtUiTools.QUiLoader().load(self.widgetPath + 'PushJoint_Ui.ui')
        
        self.widget.setParent(self)

        # set initial window size
        self.resize(400, 300)

        # locate UI widgets
        self.builtBtn = self.widget.findChild(QtWidgets.QPushButton, 'buildBtn') 
        self.pushAxisComboB = self.widget.findChild(QtWidgets.QComboBox, 'PushAxisSelector')

        self._pushAxis = self.pushAxisComboB.currentText()

        self.aimAxisComboB = self.widget.findChild(QtWidgets.QComboBox, 'AimAxisSelector')

        self._aimAxis = self.aimAxisComboB.currentText()

        self.jointAmountSpinBox = self.widget.findChild(QtWidgets.QSpinBox, 'targetAmount')

        self._numberOfJoints = self.jointAmountSpinBox.value()

        self.baseNameLineEdit = self.widget.findChild(QtWidgets.QLineEdit, 'BaseName')

        self._baseName = ""

        self.parentObjectSelectorBtn = self.widget.findChild(QtWidgets.QPushButton, 'parentObjectSelector')
        self.parentObjectLabel = self.widget.findChild(QtWidgets.QLabel, 'ParentObjectLabel')

        self._parentObject = "No Object Selected"

        self.inputObjectSelectorBtn = self.widget.findChild(QtWidgets.QPushButton, 'InputObjectSelector')
        self.inputObjectLabel = self.widget.findChild(QtWidgets.QLabel, 'InputObjectLabel')

        self._inputObject= "No Object Selected"



        # assign functionality to buttons
        self.builtBtn.clicked.connect(self.buildPushJointUIConfig)
        self.pushAxisComboB.currentIndexChanged.connect(self.updatePushAxisValue)
        self.aimAxisComboB.currentIndexChanged.connect(self.updateAimAxisValue)
        self.jointAmountSpinBox.valueChanged.connect(self.updateNumberOfPushJoints)
        self.baseNameLineEdit.textChanged.connect(self.updateBaseName)
        self.parentObjectSelectorBtn.clicked.connect(self.updateParentObject)
        self.inputObjectSelectorBtn.clicked.connect(self.updateInputObject)


    def updatePushAxisValue(self):
        self.pushAxis = self.pushAxisComboB.currentText()
        # print(f"The new Push Axis is set to: {self.pushAxis}")

    def updateAimAxisValue(self):
        self.aimAxis = self.aimAxisComboB.currentText()
        # print(f"The new Aim Axis is set to: {self.aimAxis}")

    def updateNumberOfPushJoints(self):
        self.numberOfJoints = self.jointAmountSpinBox.value()
        # print(f"The new Number of Joints to create is set to: {self.numberOfJoints}")
    
    def updateBaseName(self):
        self.baseName = self.baseNameLineEdit.text()
        # print(f"The Current Base Name for the Push Joint is: {self.baseName}")

    def updateParentObject(self):
        newParentObject= cmds.ls(sl=True)[0]
        self.parentObject = newParentObject
        self.parentObjectSelectorBtn.setStyleSheet("background-color: green; color: white")
        self.parentObjectLabel.setText(self.parentObject)

    def updateInputObject(self):
        newInputObject= cmds.ls(sl=True)[0]
        self.inputObject = newInputObject
        self.inputObjectSelectorBtn.setStyleSheet("background-color: green; color: white")
        self.inputObjectLabel.setText(self.inputObject)

    def buildPushJointUIConfig(self):
        
        # Validate if input and parent objects exist
        if not (cmds.objExists(self.parentObject)):
            self.raiseErrorMessage("Obj Not Found", "The Selected Objects Existence Could not be validated, please check again!")
            return
        
        if not (cmds.objExists(self.inputObject)):
            self.raiseErrorMessage("Obj Not Found", "The Selected Objects Existence Could not be validated, please check again!")
            return
        
        if self.parentObject == self.inputObject:
            self.raiseErrorMessage("Input Selection Error", "The Input Object and Parent Object cannot be the same! Plesae change selection")
            return
        
        if self.baseName == "":
            self.raiseErrorMessage("Naming Error", "Please enter a base name to make the created nodes unique!")
            return
        
        # Validate that The aim and Push Axis are not the same
        if self.aimAxis == self.pushAxis:
            self.raiseErrorMessage("Axis Orientation Error", "The Push and the Aim Axis cannot be the same, please check again and match the orientation Axis!")
            return

        pushJoint.buildPushJointArray(self.parentObject, self.inputObject, self.numberOfJoints, self.pushAxis, self.aimAxis, self.baseName)
    
    def resizeEvent(self, event):
        """
        Called on automatically generated resize event
        """
        self.widget.resize(self.width(), self.height())

    def raiseErrorMessage(self, title, decription):
        error_dialog = QtWidgets.QMessageBox(self)
        error_dialog.setIcon(QtWidgets.QMessageBox.Critical)  # Set the icon to show it's an error
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(title)
        error_dialog.setInformativeText("Please check your input and try again.")
        error_dialog.setDetailedText(f"Error Details: {decription}")
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)

        error_dialog.exec_()
        
    def closeWindow(self):
        """
        Close window.
        """
        print ('closing window')
        self.destroy()
    
    @property
    def pushAxis(self): return self._pushAxis
    @pushAxis.setter
    def pushAxis(self, newPushAxis):
        self._pushAxis = newPushAxis
        
    @property
    def aimAxis(self): return self._aimAxis
    @aimAxis.setter
    def aimAxis(self, newAimAxis):
        self._aimAxis = newAimAxis
        
    @property
    def numberOfJoints(self): return self._numberOfJoints
    @numberOfJoints.setter
    def numberOfJoints(self, newNumberOfJoints):
        self._numberOfJoints = newNumberOfJoints

    @property
    def baseName(self): return self._baseName
    @baseName.setter
    def baseName(self, newBaseName):
        self._baseName = newBaseName

    @property
    def parentObject(self): return self._parentObject
    @parentObject.setter
    def parentObject(self, newParentObject):
        self._parentObject = newParentObject

    @property
    def inputObject(self): return self._inputObject
    @inputObject.setter
    def inputObject(self, newInputObject):
        self._inputObject = newInputObject

    @staticmethod
    def buildPushJointArray(parentObject, inputObject, numOfJoints, pushAxis, rotAxis, baseName):

        rotationAmount = 360 / numOfJoints

        for num in range(numOfJoints):

            print(type(float(num)))
            print(type(rotationAmount))

            pushJoint.buildPushJoint(parentObject, inputObject, float(num) * rotationAmount, pushAxis, rotAxis, (baseName + str(num)))

    @staticmethod
    def buildPushJoint(parentObject, inputObject, defaultRotOffset = 0, pushAxis ="Y", rotAxis = "X", name = "newPushJoint"):
        
        #create Reference Oject
        referenceObject = cmds.createNode("transform", name = f"{name}_referenceObject_srt")

        #match reference to inputObject
        cmds.matchTransform(referenceObject, inputObject)

        #parent reference object to parent Object
        cmds.parent(referenceObject, parentObject)

            #Lock reference Object down

        #create targetPush Joint
        cmds.select(clear=True)
        targetPushJoint = cmds.joint(name = f"{name}_targetPushJoint_srt")

        cmds.parent(targetPushJoint, parentObject)
        cmds.select(clear=True)

        #Add control Attributes
        pushAttributeList = [["RotBlend", "float", 0.5, (0, 1)], 
                             ["XRotateOff", "float"],  
                             ["YRotateOff", "float"],
                             ["ZRotateOff", "float"],
                             ["DefaultPush", "float", 2],
                             ["PushX", "float", 2],
                             ["PushXNeg", "float", 2],
                             ["PushY", "float", 2],
                             ["PushYNeg", "float", 2],
                             ["PushZ", "float", 2],
                             ["PushZNeg", "float", 2]]
        
        #define Push Attribute array
        pushAxisAttributeList = ["PushX", "PushY", "PushZ"]

        for attriute in pushAttributeList:

            print(attriute, len(attriute))

            if len(attriute) == 2:
                cmds.addAttr(targetPushJoint, ln = f"{attriute[0]}", at=f"{attriute[1]}", keyable = True)
            elif len(attriute) == 3:
                cmds.addAttr(targetPushJoint, ln = f"{attriute[0]}", at=f"{attriute[1]}", defaultValue = attriute[2], keyable = True)
            elif len(attriute) == 4:
                cmds.addAttr(targetPushJoint, ln = f"{attriute[0]}", at=f"{attriute[1]}", defaultValue = attriute[2], minValue = attriute[3][0], maxValue = attriute[3][1], keyable = True)

        #decomposed inputWoldMatrix
        decomposeInputObjectWorldMatrixNode = cmds.createNode("decomposeMatrix", name = f"{name}_input_WrldMtx_dcm_fNode")
        cmds.connectAttr(f"{inputObject}.worldMatrix[0]", f"{decomposeInputObjectWorldMatrixNode}.inputMatrix")

        decomposeReferenceObjectWorldMatrixNode = cmds.createNode("decomposeMatrix", name = f"{name}_reference_WrldMtx_dcm_fNode")
        cmds.connectAttr(f"{referenceObject}.worldMatrix[0]", f"{decomposeReferenceObjectWorldMatrixNode}.inputMatrix")

        #implement Rotation Offset Quaterniens
        xRotationOffsetQuatNode = cmds.createNode("axisAngleToQuat", name = f"{name}_X_RotationOffsetQuat_fNode")
        cmds.setAttr(f"{xRotationOffsetQuatNode}.inputAxisX", 1)
        cmds.connectAttr(f"{targetPushJoint}.{pushAttributeList[1][0]}", f"{xRotationOffsetQuatNode}.inputAngle")

        yRotationOffsetQuatNode = cmds.createNode("axisAngleToQuat", name = f"{name}_Y_RotationOffsetQuat_fNode")
        cmds.setAttr(f"{yRotationOffsetQuatNode}.inputAxisY", 1)
        cmds.connectAttr(f"{targetPushJoint}.{pushAttributeList[2][0]}", f"{yRotationOffsetQuatNode}.inputAngle")

        zRotationOffsetQuatNode = cmds.createNode("axisAngleToQuat", name = f"{name}_Z_RotationOffsetQuat_fNode")
        cmds.setAttr(f"{zRotationOffsetQuatNode}.inputAxisZ", 1)
        cmds.connectAttr(f"{targetPushJoint}.{pushAttributeList[3][0]}", f"{zRotationOffsetQuatNode}.inputAngle")

        multiplyXYRotQuat = cmds.createNode("quatProd", name = f"{name}_XY_RotationOffsetQuatProduct_fNode")
        cmds.connectAttr(f"{xRotationOffsetQuatNode}.outputQuat", f"{multiplyXYRotQuat}.input1Quat")
        cmds.connectAttr(f"{yRotationOffsetQuatNode}.outputQuat", f"{multiplyXYRotQuat}.input2Quat")

        mutliplyXYZRotQuat = cmds.createNode("quatProd", name = f"{name}_XYZ_RotationOffsetQuatProduct_fNode")
        cmds.connectAttr(f"{multiplyXYRotQuat}.outputQuat", f"{mutliplyXYZRotQuat}.input1Quat")
        cmds.connectAttr(f"{zRotationOffsetQuatNode}.outputQuat", f"{mutliplyXYZRotQuat}.input2Quat")

        #interpolate input and Reference Quaternions
        inpterpolateInputReferenceQuatNode = cmds.createNode("quatSlerp", name = f"{name}_inputReference_QuatSlerp_fNode")
        cmds.connectAttr(f"{decomposeInputObjectWorldMatrixNode}.outputQuat", f"{inpterpolateInputReferenceQuatNode}.input1Quat")
        cmds.connectAttr(f"{decomposeReferenceObjectWorldMatrixNode}.outputQuat", f"{inpterpolateInputReferenceQuatNode}.input2Quat")
        cmds.connectAttr(f"{targetPushJoint}.{pushAttributeList[0][0]}", f"{inpterpolateInputReferenceQuatNode}.inputT")

        #compute Result Quaterinon
        multiplyResultQuatNode = cmds.createNode("quatProd", name = f"{name}_ResultQuatMult_InterpOffset_fNode")
        cmds.connectAttr(f"{mutliplyXYZRotQuat}.outputQuat", f"{multiplyResultQuatNode}.input1Quat")
        cmds.connectAttr(f"{inpterpolateInputReferenceQuatNode}.outputQuat", f"{multiplyResultQuatNode}.input2Quat")

        #convert Quaternion to Euler
        resultQuatToEulerNode = cmds.createNode("quatToEuler", name = f"{name}_ResultQuatToEuler_fNode")
        cmds.connectAttr(f"{multiplyResultQuatNode}.outputQuat", f"{resultQuatToEulerNode}.inputQuat")

        #configure Orientation Matrix
        orientationMatrixComposeNode = cmds.createNode("composeMatrix", name = f"{name}_orientationMatrix_cm_fNode")
        cmds.connectAttr(f"{resultQuatToEulerNode}.outputRotate", f"{orientationMatrixComposeNode}.inputRotate")
        cmds.connectAttr(f"{multiplyResultQuatNode}.outputQuat", f"{orientationMatrixComposeNode}.inputQuat")
        cmds.connectAttr(f"{decomposeInputObjectWorldMatrixNode}.outputScale", f"{orientationMatrixComposeNode}.inputScale")
        cmds.connectAttr(f"{decomposeInputObjectWorldMatrixNode}.outputTranslate", f"{orientationMatrixComposeNode}.inputTranslate")
        
        #set Default Rotation Offset 
        #solve for input Object aim Axis !!!!Needs Improvement

        cmds.setAttr(f"{targetPushJoint}.{rotAxis}RotateOff", defaultRotOffset)

        #transpose input Matrix
        inputObjectTransposeWorldMatrixNode = cmds.createNode("transposeMatrix", name = f"{name}_inputTransposeWrldMtx_fNode")
        cmds.connectAttr(f"{inputObject}.worldMatrix[0]", f"{inputObjectTransposeWorldMatrixNode}.inputMatrix")

        decomposeInputObjectTransposeWorldMatrixNode = cmds.createNode("decomposeMatrix", name = f"{name}_dcm_inputTransposeWrldMtx_fNode")
        cmds.connectAttr(f"{inputObjectTransposeWorldMatrixNode}.outputMatrix", f"{decomposeInputObjectTransposeWorldMatrixNode}.inputMatrix")

        #transpose reference World Matrix
        referenceObjectTransposeWorldMatrixNode = cmds.createNode("transposeMatrix", name = f"{name}_referenceTransposeWrldMtx_fNode")
        cmds.connectAttr(f"{referenceObject}.worldMatrix[0]", f"{referenceObjectTransposeWorldMatrixNode}.inputMatrix")

        decomposeReferenceObjectTransposeWorldMatrixNode = cmds.createNode("decomposeMatrix", name = f"{name}_dcm_referenceTransposeWrldMtx_fNode")
        cmds.connectAttr(f"{referenceObjectTransposeWorldMatrixNode}.outputMatrix", f"{decomposeReferenceObjectTransposeWorldMatrixNode}.inputMatrix")

        #compute quaternion Difference Value
        #invert Input ObjectQuat
        inputObjectTransposeQuatInvNode = cmds.createNode("quatInvert", name = f"{name}_inputObjectTransposeQuatInvers_fNode")
        cmds.connectAttr(f"{decomposeInputObjectTransposeWorldMatrixNode}.outputQuat", f"{inputObjectTransposeQuatInvNode}.inputQuat")

        #calculate the quatDiff Value
        quatDifferenceProductNode = cmds.createNode("quatProd", name = f"{name}_quatDiffProd_fNode")
        cmds.connectAttr(f"{inputObjectTransposeQuatInvNode}.outputQuat", f"{quatDifferenceProductNode}.input1Quat")
        cmds.connectAttr(f"{decomposeReferenceObjectTransposeWorldMatrixNode}.outputQuat", f"{quatDifferenceProductNode}.input2Quat")

        quatDifferenceProductInvNode = cmds.createNode("quatInvert", name = f"{name}_quatDiffProdInvers_fNode")
        cmds.connectAttr(f"{quatDifferenceProductNode}.outputQuat", f"{quatDifferenceProductInvNode}.inputQuat")

        #configure condition to flip quaternion on negative w value
        quatDifferenceProductConditonNode = cmds.createNode("condition", name = f"{name}_quatDiffProdCondition_fNode")
        cmds.setAttr(f"{quatDifferenceProductConditonNode}.operation", 4)
        cmds.connectAttr(f"{quatDifferenceProductNode}.outputQuatW", f"{quatDifferenceProductConditonNode}.firstTerm")

        cmds.connectAttr(f"{quatDifferenceProductNode}.outputQuatX", f"{quatDifferenceProductConditonNode}.colorIfFalseR")
        cmds.connectAttr(f"{quatDifferenceProductNode}.outputQuatY", f"{quatDifferenceProductConditonNode}.colorIfFalseG")
        cmds.connectAttr(f"{quatDifferenceProductNode}.outputQuatZ", f"{quatDifferenceProductConditonNode}.colorIfFalseB")

        cmds.connectAttr(f"{quatDifferenceProductInvNode}.outputQuatX", f"{quatDifferenceProductConditonNode}.colorIfTrueR")
        cmds.connectAttr(f"{quatDifferenceProductInvNode}.outputQuatY", f"{quatDifferenceProductConditonNode}.colorIfTrueG")
        cmds.connectAttr(f"{quatDifferenceProductInvNode}.outputQuatZ", f"{quatDifferenceProductConditonNode}.colorIfTrueB")

        #implement Prepush Vector
        prepushVecotrMultNode = cmds.createNode("multiplyDivide", name = f"{name}_prepushVec_mult_fNode")
        cmds.setAttr(f"{prepushVecotrMultNode}.input1{pushAxis}", 1)
        cmds.connectAttr(f"{targetPushJoint}.{pushAttributeList[4][0]}", f"{prepushVecotrMultNode}.input2{pushAxis}")

        #local PushVector Addition
        finalLocalPushVectorNode = cmds.createNode("plusMinusAverage", name = f"{name}_finalPushVector_add_fNode")
        cmds.connectAttr(f"{prepushVecotrMultNode}.output{pushAxis}", f"{finalLocalPushVectorNode}.input3D[0].input3D{pushAxis.lower()}")

        #create push Multiplication per axis
        for index, axisAttribute,  in enumerate(pushAxisAttributeList):

            #base Vector Node
            pushAxisBaseVectorNode = cmds.createNode("multiplyDivide", name = f"{name}_{axisAttribute}_baseVector_mult_fNode")
            cmds.setAttr(f"{pushAxisBaseVectorNode}.operation", 1)
            cmds.setAttr(f"{pushAxisBaseVectorNode}.input1{pushAxis}", 1)

            pushNegativeAxisBaseVectorNode = cmds.createNode("multiplyDivide", name = f"{name}_{axisAttribute}Neg_basevector_mult_fNode")
            cmds.setAttr(f"{pushNegativeAxisBaseVectorNode}.operation", 1)
            cmds.setAttr(f"{pushNegativeAxisBaseVectorNode}.input1{pushAxis}", 1)

            #configure base Vectors
            cmds.connectAttr(f"{targetPushJoint}.{axisAttribute}", f"{pushAxisBaseVectorNode}.input2X")
            cmds.connectAttr(f"{targetPushJoint}.{axisAttribute}", f"{pushAxisBaseVectorNode}.input2Y")
            cmds.connectAttr(f"{targetPushJoint}.{axisAttribute}", f"{pushAxisBaseVectorNode}.input2Z")

            cmds.connectAttr(f"{targetPushJoint}.{axisAttribute}Neg", f"{pushNegativeAxisBaseVectorNode}.input2X")
            cmds.connectAttr(f"{targetPushJoint}.{axisAttribute}Neg", f"{pushNegativeAxisBaseVectorNode}.input2Y")
            cmds.connectAttr(f"{targetPushJoint}.{axisAttribute}Neg", f"{pushNegativeAxisBaseVectorNode}.input2Z")

            #create multiplication for neg base Vector with quat difference Value
            pushAxisMultiplyQuatDiffNode = cmds.createNode("multiplyDivide", name = f"{name}_{axisAttribute}_multPushVector_quatDiff_fNode")
            cmds.connectAttr(f"{pushNegativeAxisBaseVectorNode}.outputX", f"{pushAxisMultiplyQuatDiffNode}.input1X")
            cmds.connectAttr(f"{pushNegativeAxisBaseVectorNode}.outputY", f"{pushAxisMultiplyQuatDiffNode}.input1Y")
            cmds.connectAttr(f"{pushNegativeAxisBaseVectorNode}.outputZ", f"{pushAxisMultiplyQuatDiffNode}.input1Z")

            #create multiplication for  base Vector with quat difference Value
            pushNegativeAxisMultiplyQuatDiffNode = cmds.createNode("multiplyDivide", name = f"{name}_{axisAttribute}_multNegPushVector_quatDiff_fNode")
            cmds.connectAttr(f"{pushAxisBaseVectorNode}.outputX", f"{pushNegativeAxisMultiplyQuatDiffNode}.input1X")
            cmds.connectAttr(f"{pushAxisBaseVectorNode}.outputY", f"{pushNegativeAxisMultiplyQuatDiffNode}.input1Y")
            cmds.connectAttr(f"{pushAxisBaseVectorNode}.outputZ", f"{pushNegativeAxisMultiplyQuatDiffNode}.input1Z")

            pushAxisBaseVectorInvertQuatValueNode = cmds.createNode("multiplyDivide", name = f"{name}_{axisAttribute}_negateQuatDiffValue_fNode")
            cmds.setAttr(f"{pushAxisBaseVectorInvertQuatValueNode}.operation", 1)
            cmds.setAttr(f"{pushAxisBaseVectorInvertQuatValueNode}.input2X", -1)


            #solve for socket and connect quat diff value to multiply nodes

            if "X" in axisAttribute:
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorR", f"{pushAxisMultiplyQuatDiffNode}.input2X")
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorR", f"{pushAxisMultiplyQuatDiffNode}.input2Y")
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorR", f"{pushAxisMultiplyQuatDiffNode}.input2Z")

                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorR", f"{pushAxisBaseVectorInvertQuatValueNode}.input1X")

            elif "Y" in axisAttribute:
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorG", f"{pushAxisMultiplyQuatDiffNode}.input2X")
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorG", f"{pushAxisMultiplyQuatDiffNode}.input2Y")
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorG", f"{pushAxisMultiplyQuatDiffNode}.input2Z")

                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorG", f"{pushAxisBaseVectorInvertQuatValueNode}.input1X")

            else:
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorB", f"{pushAxisMultiplyQuatDiffNode}.input2X")
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorB", f"{pushAxisMultiplyQuatDiffNode}.input2Y")
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorB", f"{pushAxisMultiplyQuatDiffNode}.input2Z")

                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorB", f"{pushAxisBaseVectorInvertQuatValueNode}.input1X")

            cmds.connectAttr(f"{pushAxisBaseVectorInvertQuatValueNode}.outputX", f"{pushNegativeAxisMultiplyQuatDiffNode}.input2X")
            cmds.connectAttr(f"{pushAxisBaseVectorInvertQuatValueNode}.outputX", f"{pushNegativeAxisMultiplyQuatDiffNode}.input2Y")
            cmds.connectAttr(f"{pushAxisBaseVectorInvertQuatValueNode}.outputX", f"{pushNegativeAxisMultiplyQuatDiffNode}.input2Z")
            

            #create Absolute condition Node
            pushVectorOutputConditionNode = cmds.createNode("condition", name = f"{name}_{axisAttribute}_abs_condition_fNode")
            cmds.setAttr(f"{pushVectorOutputConditionNode}.operation", 4)

            #configure condition node
            cmds.connectAttr(f"{pushAxisMultiplyQuatDiffNode}.outputX", f"{pushVectorOutputConditionNode}.colorIfFalseR")
            cmds.connectAttr(f"{pushAxisMultiplyQuatDiffNode}.outputY", f"{pushVectorOutputConditionNode}.colorIfFalseG")
            cmds.connectAttr(f"{pushAxisMultiplyQuatDiffNode}.outputZ", f"{pushVectorOutputConditionNode}.colorIfFalseB")

            cmds.connectAttr(f"{pushNegativeAxisMultiplyQuatDiffNode}.outputX", f"{pushVectorOutputConditionNode}.colorIfTrueR")
            cmds.connectAttr(f"{pushNegativeAxisMultiplyQuatDiffNode}.outputY", f"{pushVectorOutputConditionNode}.colorIfTrueG")
            cmds.connectAttr(f"{pushNegativeAxisMultiplyQuatDiffNode}.outputZ", f"{pushVectorOutputConditionNode}.colorIfTrueB")

            if "X" in axisAttribute:
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorR", f"{pushVectorOutputConditionNode}.firstTerm")
            elif "Y" in axisAttribute:
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorG", f"{pushVectorOutputConditionNode}.firstTerm")
            else:
                cmds.connectAttr(f"{quatDifferenceProductConditonNode}.outColorB", f"{pushVectorOutputConditionNode}.firstTerm")

            cmds.connectAttr(f"{pushVectorOutputConditionNode}.outColorR", f"{finalLocalPushVectorNode}.input3D[{index + 1}].input3Dx")
            cmds.connectAttr(f"{pushVectorOutputConditionNode}.outColorG", f"{finalLocalPushVectorNode}.input3D[{index + 1}].input3Dy")
            cmds.connectAttr(f"{pushVectorOutputConditionNode}.outColorB", f"{finalLocalPushVectorNode}.input3D[{index + 1}].input3Dz")

        #convert push Vector to Matrix
        pushVectorComposeMatrixNode = cmds.createNode("composeMatrix", name = f"{name}_pushVector_cm_fNode")
        cmds.connectAttr(f"{finalLocalPushVectorNode}.output3D", f"{pushVectorComposeMatrixNode}.inputTranslate")

        #factor the orientation matrix into the system
        multiplyPushVectorOrientationMatrixNode = cmds.createNode("multMatrix", name = f"{name}_multPushVecMtx_OrientMtx_fNode")
        cmds.connectAttr(f"{pushVectorComposeMatrixNode}.outputMatrix", f"{multiplyPushVectorOrientationMatrixNode}.matrixIn[0]")
        cmds.connectAttr(f"{orientationMatrixComposeNode}.outputMatrix", f"{multiplyPushVectorOrientationMatrixNode}.matrixIn[1]")

        
        #multply the local result matrix into the parent space of the input object

        # multiplyFinalOutputMatrixNode = cmds.createNode("multMatrix", name = f"{name}_multFinalOutputWrldMtx_fNode")
        # cmds.connectAttr(f"{multiplyPushVectorOrientationMatrixNode}.matrixSum", f"{multiplyFinalOutputMatrixNode}.matrixIn[0]")
        # cmds.connectAttr(f"{inputObject}.parentInverseMatrix[0]", f"{multiplyFinalOutputMatrixNode}.matrixIn[1]")

        decomposeFinalOutputMatrixNode = cmds.createNode("decomposeMatrix", name = f"{name}_finalOutput_dcmWrldMtx_fNode")
        cmds.connectAttr(f"{multiplyPushVectorOrientationMatrixNode}.matrixSum", f"{decomposeFinalOutputMatrixNode}.inputMatrix")

        # unparent input joint
        cmds.parent(targetPushJoint, world = True)

        #connect final matrix to output object
        #Translation
        cmds.connectAttr(f"{decomposeFinalOutputMatrixNode}.outputTranslate", f"{targetPushJoint}.translate")
        cmds.connectAttr(f"{resultQuatToEulerNode}.outputRotate", f"{targetPushJoint}.rotate")


def openWindow():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QtWidgets.QApplication.allWindows()):
            if 'PushJointWindow' in win.objectName(): # update this name to match name below
                win.destroy()

    #QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    pushJoint.window = pushJoint(parent = mayaMainWindow)
    pushJoint.window.setObjectName('PushJointWindow') # code above uses this to ID any existing windows
    pushJoint.window.setWindowTitle('Push Joint Builder')
    pushJoint.window.show()