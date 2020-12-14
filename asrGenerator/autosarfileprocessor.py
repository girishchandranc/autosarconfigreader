from lxml import etree
from enum import Enum
import sys

FileReaderStatus = Enum('FileReaderStatus', 'MODULE_FOUND MODULE_NOT_FOUND')
ParameterTypes = Enum('ParameterTypes', 'INTEGER FLOAT BOOLEAN STRING FUNCTION ENUMERATION')
ReferenceTypes = Enum('ReferenceTypes', 'SIMPLE_REFERENCE CHOICE_REFERENCE FOREIGN_REFERENCE INSTANCE_REFERENCE')

class AutosarFileProcessor:
    def __init__(self, file, module):
        rootAutosarNode = etree.parse(file)
        self.status = FileReaderStatus.MODULE_NOT_FOUND
        self.moduleNodeForGeneration= None

        #{*} is used to consider the wildcard namespace.
        for moduleDefNode in rootAutosarNode.findall('//{*}ECUC-MODULE-DEF/{*}SHORT-NAME'):
            if moduleDefNode.text == module:
                self.moduleNodeForGeneration= moduleDefNode.getparent()
                self.status = FileReaderStatus.MODULE_FOUND
                break
    
    def get_status(self):
        return self.status
    
    def build_module(self):
        return Module(self.moduleNodeForGeneration) if self.moduleNodeForGeneration is not None else None

#Representation of any autosar node
class AutosarNode:
    def __init__(self, node):
        self.xmlNode = node
        self.name = node.find('{*}SHORT-NAME').text
        names = []
        names.append(self.name)
        self.__compute_path(node.getparent(), names)
        self.path = self.__build_path(names)

    def __compute_path(self, node, names):
        #get all path until the ELEMENTS root node
        if node.tag.endswith('ELEMENTS'):
            return names
        else:
            shortNameNode = node.find('{*}SHORT-NAME')
            if shortNameNode is not None:
                names.append(shortNameNode.text)

            return self.__compute_path(node.getparent(), names)
    
    def __build_path(self, names):
        returnValue = ''
        for name in reversed(names):
            returnValue = returnValue + '/' + name
        return returnValue

    def get_name(self):
        return self.name
    
    def get_path(self):
        return self.path
    
    def __str__(self):
        return self.name

#Representation of autosar module node
class Module(AutosarNode):
    def __init__(self, node):
        super().__init__(node)
        self.containers = []
        for containerNode in node.findall('{*}CONTAINERS/{*}ECUC-PARAM-CONF-CONTAINER-DEF'):
            self.containers.append(Container(containerNode, False))
        for containerNode in node.findall('{*}CONTAINERS/{*}ECUC-CHOICE-CONTAINER-DEF'):
            self.containers.append(Container(containerNode, True))

    def get_containers(self):
        return self.containers

#Representation of autosar container node
class Container(AutosarNode):
    def __init__(self, node, isChoiceContainer):
        super().__init__(node)
        self.isChoiceContainer = isChoiceContainer
        self.isMultiInstance = False

        multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY')
        if multiInstanceNode is not None and (multiInstanceNode.text == '*' or int(multiInstanceNode.text) > 1):
            self.isMultiInstance = True
        else:
            multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY-INFINITE')
            if multiInstanceNode is not None and multiInstanceNode.text == 'true':
                self.isMultiInstance = True

        self.subcontainers = []
        for containerNode in node.findall('{*}SUB-CONTAINERS/{*}ECUC-PARAM-CONF-CONTAINER-DEF'):
            self.subcontainers.append(Container(containerNode, False))
        for containerNode in node.findall('{*}SUB-CONTAINERS/{*}ECUC-CHOICE-CONTAINER-DEF'):
            self.subcontainers.append(Container(containerNode, True))
        for containerNode in node.findall('{*}CHOICES/{*}ECUC-PARAM-CONF-CONTAINER-DEF'):
            self.subcontainers.append(Container(containerNode, False))
        
        self.parameters = []
        self.__build_parameters(self.xmlNode)
        self.references = []
        self.__build_references(self.xmlNode)

    def __build_parameters(self, containerNode):
        parametersNode = containerNode.find('{*}PARAMETERS')
        if parametersNode is not None:
            for param in parametersNode.findall('{*}ECUC-INTEGER-PARAM-DEF'):
                self.parameters.append(Parameter(param, ParameterTypes.INTEGER))
            for param in parametersNode.findall('{*}ECUC-BOOLEAN-PARAM-DEF'):
                self.parameters.append(Parameter(param, ParameterTypes.BOOLEAN))
            for param in parametersNode.findall('{*}ECUC-FLOAT-PARAM-DEF'):
                self.parameters.append(Parameter(param, ParameterTypes.FLOAT))
            for param in parametersNode.findall('{*}ECUC-STRING-PARAM-DEF'):
                self.parameters.append(Parameter(param, ParameterTypes.STRING))
            for param in parametersNode.findall('{*}ECUC-ENUMERATION-PARAM-DEF'):
                self.parameters.append(Parameter(param, ParameterTypes.ENUMERATION))
            for param in parametersNode.findall('{*}ECUC-FUNCTION-PARAM-DEF'):
                self.parameters.append(Parameter(param, ParameterTypes.FUNCTION))

    def __build_references(self, containerNode):
        referencesNode = containerNode.find('{*}REFERENCES')
        if referencesNode is not None:
            for reference in referencesNode.findall('{*}ECUC-REFERENCE-DEF'):
                self.references.append(Reference(reference, ReferenceTypes.SIMPLE_REFERENCE))
            for reference in referencesNode.findall('{*}ECUC-CHOICE-REFERENCE-DEF'):
                self.references.append(Reference(reference, ReferenceTypes.CHOICE_REFERENCE))
            for reference in referencesNode.findall('{*}ECUC-FOREIGN-REFERENCE-DEF'):
                self.references.append(Reference(reference, ReferenceTypes.FOREIGN_REFERENCE))

    def is_choice_container(self):
        return self.isChoiceContainer

    def is_multi_instance_container(self):
        return self.isMultiInstance

    def get_sub_containers(self):
        return self.subcontainers

    def get_parameters(self):
        return self.parameters

    def get_references(self):
        return self.references

#Representation of autosar parameter node
class Parameter(AutosarNode):
    def __init__(self, node, parameterType):
        super().__init__(node)
        self.parameterType = parameterType
        
        self.defaultValue = None
        self.isDefaultSet = False
        self.__set_default_value(node)
        
        self.minValue = None
        self.isMinValueSet = False
        self.__set_min_max_value(node, True)

        self.maxValue = None
        self.isMaxValueSet = False
        self.__set_min_max_value(node, False)

        self.enumLiterals = []
        if parameterType == ParameterTypes.ENUMERATION:
            for literal in node.findall('{*}LITERALS/{*}ECUC-ENUMERATION-LITERAL-DEF/{*}SHORT-NAME'):
                self.enumLiterals.append(literal.text)

    def __set_default_value(self, node):
        defaultValueNode = node.find('{*}DEFAULT-VALUE')
        if defaultValueNode is not None:
            self.isDefaultSet = True
            if self.parameterType == ParameterTypes.BOOLEAN:
                self.defaultValue = True if defaultValueNode.text.lower() == 'true' else False
            elif self.parameterType == ParameterTypes.INTEGER or self.parameterType == ParameterTypes.FLOAT:
                self.defaultValue = defaultValueNode.text if defaultValueNode.text != '' else None
            else:
                self.defaultValue =  '\''+ defaultValueNode.text + '\'' if defaultValueNode.text != '' else None

    def __set_min_max_value(self, node, isMinValue):
        if self.parameterType == ParameterTypes.INTEGER or self.parameterType == ParameterTypes.FLOAT:            
            valueNode = node.find('{*}' + ('MIN' if isMinValue else 'MAX'))
            if valueNode is not None:
                if isMinValue:
                    self.minValue = valueNode.text
                    self.isMinValueSet = True
                else:
                    self.maxValue = sys.maxsize if valueNode.text.lower() == 'inf' else valueNode.text
                    self.isMaxValueSet = True

    def get_type(self):
        return self.parameterType

    #gets the default value if configured in the definition file
    def get_default_value(self):
        return self.defaultValue

    def is_default_value_set(self):
        return self.isDefaultSet

    #gets the min value of interger/float parameter if configured in the definition file
    def get_min_value(self):
        return self.minValue
    
    def is_min_value_set(self):
        return self.isMinValueSet

    #gets the max value of interger/float parameter if configured in the definition file
    def get_max_value(self):
        return self.maxValue
    
    def is_max_value_set(self):
        return self.isMaxValueSet
    
    def get_enum_literals(self):
        return self.enumLiterals

#Representation of autosar reference node
class Reference(AutosarNode):
    def __init__(self, node, referenceType):
        super().__init__(node)
        self.referenceType = referenceType
        self.targetRef = None
        self.targetRefs = []
        self.targetType = None
        self.__set_detinations(node)
        self.isMultiInstance = False

        multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY')
        if multiInstanceNode is not None and (multiInstanceNode.text == '*' or int(multiInstanceNode.text) > 1):
            self.isMultiInstance = True
        else:
            multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY-INFINITE')
            if multiInstanceNode is not None and multiInstanceNode.text == 'true':
                self.isMultiInstance = True

    def __set_detinations(self, node):
        if self.referenceType == ReferenceTypes.SIMPLE_REFERENCE:
            destinationRef = node.find('{*}DESTINATION-REF')
            if destinationRef is not None:
                self.targetRef = destinationRef.text

        if self.referenceType == ReferenceTypes.CHOICE_REFERENCE:
            for destinationRef in node.findall('{*}DESTINATION-REFS/{*}DESTINATION-REF'):
                if destinationRef is not None:
                    self.targetRefs.append(destinationRef.text)

        if self.referenceType == ReferenceTypes.FOREIGN_REFERENCE:
            destinationType = node.find('{*}DESTINATION-TYPE')
            if destinationType is not None:
                self.targetType = destinationType.text

    def get_type(self):
        return self.referenceType
    
    def is_multi_instance_reference(self):
        return self.isMultiInstance

    #gets the target reference for simple reference if configured in the definition file
    def get_destination(self):
        return self.targetRef
    
    #gets the target references for choice reference if configured in the definition file
    def get_destinations(self):
        return self.targetRefs
    
    #gets the target type for foreign reference if configured in the definition file
    def get_destination_type(self):
        return self.targetType
