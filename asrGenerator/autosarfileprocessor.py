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

        names.clear()
        names.append(self.__name)
        self.__compute_path(node.getparent(), names, process_until_root=True)
        self.full_path_until_root = self.__build_path(names)

        self.is_optional = True
        self.upper_multiplicity = 1
        self.is_upper_multiplicity_infinite = False

        multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY')
        if multiInstanceNode is not None: 
            if multiInstanceNode.text == '*':
                self.is_upper_multiplicity_infinite = True
            elif int(multiInstanceNode.text) > 1:
                self.upper_multiplicity = int(multiInstanceNode.text)
        else:
            multiInstanceNode = node.find('{*}UPPER-MULTIPLICITY-INFINITE')
            if multiInstanceNode is not None and (multiInstanceNode.text == 'true' or multiInstanceNode.text == '1'):
                self.is_upper_multiplicity_infinite = True

        lowerMulNode = node.find('{*}LOWER-MULTIPLICITY')
        if lowerMulNode is not None and int(lowerMulNode.text) > 0:
            self.is_optional = False

        self.__className = self.__name if isinstance(self, (Module, Parameter, Reference)) else AutosarNode.__identify_class_name(self.__name)


    def __compute_path(self, node, names, process_until_root = False):
        if etree.QName(node).localname == 'ELEMENTS' and process_until_root is False:
            return names
        elif etree.QName(node).localname == 'AUTOSAR':
            return names
        else:
            shortNameNode = node.find('{*}SHORT-NAME')
            if shortNameNode is not None:
                names.append(shortNameNode.text)

            return self.__compute_path(node.getparent(), names, process_until_root)


    def __build_path(self, names):
        returnValue = ''
        for name in reversed(names):
            returnValue = returnValue + '/' + name
        return returnValue


    def get_name(self):
        return self.__name
    
    def get_path(self):
        return self.__path

    def is_multi_instance(self):
        return self.is_upper_multiplicity_infinite or (self.upper_multiplicity > 1)

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

    def any_mandatory_containers(self):
        return any((con.is_optional is False) for con in self.__containers)

#Representation of autosar container node
class Container(AutosarNode):
    def __init__(self, node, isChoiceContainer):
        super().__init__(node)
        self.__isChoiceContainer = isChoiceContainer        

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
                self.__parameters.append(Parameter(param, ParameterTypes.INTEGER, 'ECUC-INTEGER-PARAM-DEF'))
            for param in parametersNode.findall('{*}ECUC-BOOLEAN-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.BOOLEAN, 'ECUC-BOOLEAN-PARAM-DEF'))
            for param in parametersNode.findall('{*}ECUC-FLOAT-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.FLOAT, 'ECUC-FLOAT-PARAM-DEF'))
            for param in parametersNode.findall('{*}ECUC-STRING-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.STRING, 'ECUC-STRING-PARAM-DEF'))
            for param in parametersNode.findall('{*}ECUC-ENUMERATION-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.ENUMERATION, 'ECUC-ENUMERATION-PARAM-DEF'))
            for param in parametersNode.findall('{*}ECUC-FUNCTION-PARAM-DEF'):
                self.__parameters.append(Parameter(param, ParameterTypes.FUNCTION, 'ECUC-FUNCTION-PARAM-DEF'))

    def __build_references(self, containerNode):
        referencesNode = containerNode.find('{*}REFERENCES')
        if referencesNode is not None:
            for reference in referencesNode.findall('{*}ECUC-REFERENCE-DEF'):
                self.__references.append(Reference(reference, ReferenceTypes.SIMPLE_REFERENCE, 'ECUC-REFERENCE-DEF'))
            for reference in referencesNode.findall('{*}ECUC-CHOICE-REFERENCE-DEF'):
                self.__references.append(Reference(reference, ReferenceTypes.CHOICE_REFERENCE, 'ECUC-CHOICE-REFERENCE-DEF'))
            for reference in referencesNode.findall('{*}ECUC-FOREIGN-REFERENCE-DEF'):
                self.__references.append(Reference(reference, ReferenceTypes.FOREIGN_REFERENCE, 'ECUC-FOREIGN-REFERENCE-DEF'))
            for reference in referencesNode.findall('{*}ECUC-INSTANCE-REFERENCE-DEF'):
                self.__references.append(Reference(reference, ReferenceTypes.INSTANCE_REFERENCE, 'ECUC-INSTANCE-REFERENCE-DEF'))

    def is_choice_container(self):
        return self.__isChoiceContainer

    def get_sub_containers(self):
        return self.__subcontainers

    def any_mandatory_sub_containers_or_parameters_or_references(self):
        return any((con.is_optional is False) for con in self.__subcontainers) or any((con.is_optional is False) for con in self.__parameters) or any((con.is_optional is False) for con in self.__references)

    def get_parameters(self):
        return self.__parameters

    def get_references(self):
        return self.__references

    def get_tag(self):
        return 'ECUC-CHOICE-CONTAINER-DEF' if self.__isChoiceContainer else 'ECUC-PARAM-CONF-CONTAINER-DEF'

#Representation of autosar parameter node
class Parameter(AutosarNode):
    def __init__(self, node, parameterType, tag):
        super().__init__(node)
        self.__parameterType = parameterType
        self.tag = tag
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
    def __init__(self, node, referenceType, tag):
        super().__init__(node)
        self.__referenceType = referenceType
        self.tag = tag
        self.__targetRef = None
        self.__targetRefs = []
        self.__targetType = None
        self.__set_detinations(node)

    def __set_detinations(self, node):
        if self.__referenceType == ReferenceTypes.SIMPLE_REFERENCE:
            destinationRef = node.find('{*}DESTINATION-REF')
            if destinationRef is not None:
                self.__targetRef = destinationRef.text

        if self.__referenceType == ReferenceTypes.CHOICE_REFERENCE:
            for destinationRef in node.findall('{*}DESTINATION-REFS/{*}DESTINATION-REF'):
                if destinationRef is not None:
                    self.__targetRefs.append(destinationRef.text)

        if self.__referenceType == ReferenceTypes.FOREIGN_REFERENCE or self.__referenceType == ReferenceTypes.INSTANCE_REFERENCE:
            destinationType = node.find('{*}DESTINATION-TYPE')
            if destinationType is not None:
                self.__targetType = destinationType.text

    def get_type(self):
        return self.__referenceType

    def get_destination(self):
        """
        gets the target reference for simple reference if configured in the definition file
        """
        return self.__targetRef

    def get_destinations(self):
        """
        gets the target references for choice reference if configured in the definition file
        """
        return self.__targetRefs

    def get_destination_type(self):
        """
        gets the target type for foreign reference if configured in the definition file
        """
        return self.__targetType

    def get_dest_tag_for_ref_value(self):
        if self.__referenceType == ReferenceTypes.SIMPLE_REFERENCE or self.__referenceType == ReferenceTypes.CHOICE_REFERENCE:
            return "ECUC-CONTAINER-VALUE"
        else:
            # Update the if/else branch when more ref types are supported.
            return self.__targetType
