import maya.cmds as cmds

class pushJoint():

    @staticmethod
    def buildPushJoint(parentObject, inputObject, name):
        
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
        
        for attriute in pushAttributeList:

            print(attriute, len(attriute))

            if len(attriute) == 2:
                cmds.addAttr(ln = f"{attriute[0]}", at=f"{attriute[1]}", keyable = True)
            elif len(attriute) == 3:
                cmds.addAttr(ln = f"{attriute[0]}", at=f"{attriute[1]}", defaultValue = attriute[2], keyable = True)
            elif len(attriute) == 4:
                cmds.addAttr(ln = f"{attriute[0]}", at=f"{attriute[1]}", defaultValue = attriute[2], minValue = attriute[3][0], maxValue = attriute[3][1], keyable = True)

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

        #transpose input Wo Matrix
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
        cmds.connectAttr(f"{decomposeReferenceObjectTransposeWorldMatrixNode}.outputQuat", f"{quatDifferenceProductNode}.input1Quat")

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
        cmds.setAttr(f"{prepushVecotrMultNode}.input1Y", 1)
        cmds.connectAttr(f"{targetPushJoint}.{pushAttributeList[4][0]}", f"{prepushVecotrMultNode}.input2Y")

        #local PushVector Addition
        finalLocalPushVectorNode = cmds.createNode("plusMinusAverage", name = f"{name}_finalPushVector_add_fNode")
        cmds.connectAttr(f"{prepushVecotrMultNode}.outputY", f"{finalLocalPushVectorNode}.input3D[0].input3Dy")


        


        

