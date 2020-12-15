from lxml import etree
from enum import Enum
import sys

FileReaderStatus = Enum('FileReaderStatus', 'MODULE_FOUND MODULE_NOT_FOUND')
ParameterTypes = Enum('ParameterTypes', 'INTEGER FLOAT BOOLEAN STRING FUNCTION ENUMERATION')
ReferenceTypes = Enum('ReferenceTypes', 'SIMPLE_REFERENCE CHOICE_REFERENCE FOREIGN_REFERENCE INSTANCE_REFERENCE')

class AutosarFileProcessor:
    def __init__(self, file, module):
        rootAutosarNode = etree.parse(file)
        self.__status = FileReaderStatus.MODULE_NOT_FOUND
        self.__moduleNodeForGeneration= None
        AutosarNode.clear() # clears any cache it exists

        #{*} is used to consider the wildcard namespace.
        for moduleDefNode in rootAutosarNode.findall('//{*}ECUC-MODULE-DEF/{*}SHORT-NAME'):
            if moduleDefNode.text.lower() == module.lower():
                self.__moduleNodeForGeneration= moduleDefNode.getparent()
                self.__status = FileReaderStatus.MODULE_FOUND
                break
    
    def get_status(self):
        return self.__status
    
    def build_module(self):
        return Module(self.__moduleNodeForGeneration) if self.__moduleNodeForGeneration is not None else None

#Representation of any autosar node
class AutosarNode:
    __classNames = [] #static list with names of all class names of containers/parameters/references.Kept to avoid duplicate naming

    def __init__(self, node):
        self.__xmlNode = node
        self.__name = node.find('{*}SHORT-NAME').text
        names = []
        names.append(self.__name)
        self.__compute_path(node.getparent(), names)
        self.__path = self.__build_path(names)
        self.__className = self.__name if isinstance(self, (Module, Parameter, Reference)) else AutosarNode.__identify_class_name(self.__name)

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
        return self.__name
    
    def get_path(self):
        return self.__path

    def get_class_name(self):
        return self.__className
    
    @staticmethod
    def __identify_class_name(name,count=None):
        if name not in AutosarNode.__classNames:
            AutosarNode.__classNames.append(name)
            return name
        else:
            count = 1 if count is None else (count + 1)
            name = (name + str(count)) if count == 1 else (name[:-1] + str(count)) 
            return AutosarNode.__identify_class_name(name, count)
    
    @staticmethod
    def clear():
        AutosarNode.__classNames.clear()

    def __str__(self):
        return self.__name

#Representation of autosar module node
class Module(AutosarNode):
    def __init__(self, node):
        super().__init__(node)
        self.__containers = []
        for containerNode in node.findall('{*}CONTAINERS/{*}ECUC-PARAM-CONF-CONTAINER-DEF'):
            self.__containers.append(Container(containerNode, False))
        for containerNode in node.findall('{*}CONTAINERS/{*}ECUC-CHOICE-CONTAINER-DEF'):
            self.__containers.append(Container(containerNode, True))

    def get_containers(self):
        return self.__containers

#Representation of autosar container node
class Container(AutosarNode):
    def __init__(self, node, isChoiceContainer):
        super().__init__(node)
        self.__isChoiceContainer = isChoiceContainer
        self.__isMultiInstance = False

        multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY')
        if multiInstanceNode is not None and (multiInstanceNode.text == '*' or int(multiInstanceNode.text) > 1):
            self.__isMultiInstance = True
        else:
            multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY-INFINITE')
            if multiInstanceNode is not None and multiInstanceNode.text == 'true':
                self.__isMultiInstance = True

        self.__subcontainers = []
        for containerNode in node.findall('{*}SUB-CONTAINERS/{*}ECUC-PARAM-CONF-CONTAINER-DEF'):
            self.__subcontainers.append(Container(containerNode, False))
        for containerNode in node.findall('{*}SUB-CONTAINERS/{*}ECUC-CHOICE-CONTAINER-DEF'):
            self.__subcontainers.append(Container(containerNode, True))
        for containerNode in node.findall('{*}CHOICES/{*}ECUC-PARAM-CONF-CONTAINER-DEF'):
            self.__subcontainers.append(Container(containerNode, False))
        
        self.__parameters = []
        self.__build_parameters(node)
        self.__references = []
        self.__build_references(node)

    def __build_parameters(self, containerNode):
        parametersNode = containerNode.find('{*}PARAMETERS')
        if parametersNode is not None:
            for param in parametersNode.findall('{*}ECUC-INTEGER-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.INTEGER))
            for param in parametersNode.findall('{*}ECUC-BOOLEAN-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.BOOLEAN))
            for param in parametersNode.findall('{*}ECUC-FLOAT-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.FLOAT))
            for param in parametersNode.findall('{*}ECUC-STRING-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.STRING))
            for param in parametersNode.findall('{*}ECUC-ENUMERATION-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.ENUMERATION))
            for param in parametersNode.findall('{*}ECUC-FUNCTION-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.FUNCTION))

    def __build_references(self, containerNode):
        referencesNode = containerNode.find('{*}REFERENCES')
        if referencesNode is not None:
            for reference in referencesNode.findall('{*}ECUC-REFERENCE-DEF'):
                self.__references.append(Reference(reference, ReferenceTypes.SIMPLE_REFERENCE))
            for reference in referencesNode.findall('{*}ECUC-CHOICE-REFERENCE-DEF'):
                self.__references.append(Reference(reference, ReferenceTypes.CHOICE_REFERENCE))
            for reference in referencesNode.findall('{*}ECUC-FOREIGN-REFERENCE-DEF'):
                self.__references.append(Reference(reference, ReferenceTypes.FOREIGN_REFERENCE))

    def is_choice_container(self):
        return self.__isChoiceContainer

    def is_multi_instance_container(self):
        return self.__isMultiInstance

    def get_sub_containers(self):
        return self.__subcontainers

    def get_parameters(self):
        return self.__parameters

    def get_references(self):
        return self.__references

#Representation of autosar parameter node
class Parameter(AutosarNode):
    def __init__(self, node, parameterType):
        super().__init__(node)
        self.__parameterType = parameterType
        
        self.__defaultValue = None
        self.__isDefaultSet = False
        self.__set_default_value(node)
        
        self.__minValue = None
        self.__isMinValueSet = False
        self.__set_min_max_value(node, True)

        self.__maxValue = None
        self.__isMaxValueSet = False
        self.__set_min_max_value(node, False)

        self.__enumLiterals = []
        if parameterType == ParameterTypes.ENUMERATION:
            for literal in node.findall('{*}LITERALS/{*}ECUC-ENUMERATION-LITERAL-DEF/{*}SHORT-NAME'):
                self.__enumLiterals.append(literal.text)

    def __set_default_value(self, node):
        defaultValueNode = node.find('{*}DEFAULT-VALUE')
        if defaultValueNode is not None:
            self.__isDefaultSet = True
            if self.__parameterType == ParameterTypes.BOOLEAN:
                self.__defaultValue = True if defaultValueNode.text.lower() == 'true' else False
            elif self.__parameterType == ParameterTypes.INTEGER or self.__parameterType == ParameterTypes.FLOAT:
                self.__defaultValue = defaultValueNode.text if defaultValueNode.text != '' else None
            else:
                self.__defaultValue =  '\''+ defaultValueNode.text + '\'' if defaultValueNode.text != '' else None

    def __set_min_max_value(self, node, isMinValue):
        if self.__parameterType == ParameterTypes.INTEGER or self.__parameterType == ParameterTypes.FLOAT:            
            valueNode = node.find('{*}' + ('MIN' if isMinValue else 'MAX'))
            if valueNode is not None:
                if isMinValue:
                    self.__minValue = (-sys.maxsize - 1) if valueNode.text.lower() == '-inf' else valueNode.text
                    self.__isMinValueSet = True
                else:
                    self.__maxValue = sys.maxsize if valueNode.text.lower() == 'inf' else valueNode.text
                    self.__isMaxValueSet = True

    def get_type(self):
        return self.__parameterType

    #gets the default value if configured in the definition file
    def get_default_value(self):
        return self.__defaultValue

    def is_default_value_set(self):
        return self.__isDefaultSet

    #gets the min value of interger/float parameter if configured in the definition file
    def get_min_value(self):
        return self.__minValue
    
    def is_min_value_set(self):
        return self.__isMinValueSet

    #gets the max value of interger/float parameter if configured in the definition file
    def get_max_value(self):
        return self.__maxValue
    
    def is_max_value_set(self):
        return self.__isMaxValueSet
    
    def get_enum_literals(self):
        return self.__enumLiterals

#Representation of autosar reference node
class Reference(AutosarNode):
    def __init__(self, node, referenceType):
        super().__init__(node)
        self.__referenceType = referenceType
        self.__targetRef = None
        self.__targetRefs = []
        self.__targetType = None
        self.__set_detinations(node)
        self.__isMultiInstance = False

        multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY')
        if multiInstanceNode is not None and (multiInstanceNode.text == '*' or int(multiInstanceNode.text) > 1):
            self.__isMultiInstance = True
        else:
            multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY-INFINITE')
            if multiInstanceNode is not None and multiInstanceNode.text == 'true':
                self.__isMultiInstance = True

    def __set_detinations(self, node):
        if self.__referenceType == ReferenceTypes.SIMPLE_REFERENCE:
            destinationRef = node.find('{*}DESTINATION-REF')
            if destinationRef is not None:
                self.__targetRef = destinationRef.text

        if self.__referenceType == ReferenceTypes.CHOICE_REFERENCE:
            for destinationRef in node.findall('{*}DESTINATION-REFS/{*}DESTINATION-REF'):
                if destinationRef is not None:
                    self.__targetRefs.append(destinationRef.text)

        if self.__referenceType == ReferenceTypes.FOREIGN_REFERENCE:
            destinationType = node.find('{*}DESTINATION-TYPE')
            if destinationType is not None:
                self.__targetType = destinationType.text

    def get_type(self):
        return self.__referenceType
    
    def is_multi_instance_reference(self):
        return self.__isMultiInstance

    #gets the target reference for simple reference if configured in the definition file
    def get_destination(self):
        return self.__targetRef
    
    #gets the target references for choice reference if configured in the definition file
    def get_destinations(self):
        return self.__targetRefs
    
    #gets the target type for foreign reference if configured in the definition file
    def get_destination_type(self):
        return self.__targetType
