"""
The python file contains the different classes for accessing the containers and parameters of the 'demo' module.
This file is generated for the module 'demo' on Sat Dec 12 20:53:18 2020.
"""

from lxml import etree
from enum import Enum

# Enums for possible parameter and reference types
ParameterTypes = Enum('ParameterTypes', 'INTEGER FLOAT BOOLEAN STRING FUNCTION ENUMERATION')
ReferenceTypes = Enum('ReferenceTypes', 'SIMPLE_REFERENCE CHOICE_REFERENCE FOREIGN_REFERENCE')

# dict supposed to be used internally by the module to store the path and its corresponding autosar node
pathsToNodeDict = {}

def read_and_build_module_configuration(file):
    """
    Reads the module configuration and build the demo structure.

    @param file: The configuration arxml file.
    @return:  The built demo structure. May return None if the given 
              file do not contain the module configuration for
              demo.
    """
    rootAutosarNode = etree.parse(file)
    moduleConfNode = None
    #{*} is used to consider the wildcard namespace.
    for module in rootAutosarNode.findall('//{*}ECUC-MODULE-CONFIGURATION-VALUES'):
        definitionRef = module.find('{*}DEFINITION-REF').text
        if definitionRef is not None and definitionRef.split('/').pop() == 'demo':
            moduleConfNode = module
            break

    if moduleConfNode is not None:
        return demo(moduleConfNode)
    else:
        return None

def get_node(path):
    """
    Returns the autosar node for the corresponding path.

    @param path: The fully qualified autosar path for eg: /Autosar/Module/Container1.
    @return:  The node corresponding to the path or None if the node for path is not available.
    """
    if path in pathsToNodeDict:
        return pathsToNodeDict[path]
    else:
        return None

# Base class for all autosar nodes
class AutosarNode:
    def __init__(self, node, definitionName):
        self.node = node
        self.name = None
        shortNameNode = node.find('{*}SHORT-NAME')
        if shortNameNode is not None:
            self.name = shortNameNode.text
        else:
            self.name = definitionName
        self.definitionName = definitionName
        names = []
        names.append(self.name)
        self.__compute_path(node.getparent(), names)
        self.path = self.__build_path(names)
        pathsToNodeDict[self.path] = self

    def __compute_path(self, node, names):
        #get all path until the AUTOSAR root node
        if node.tag.endswith('AUTOSAR'):
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

    def get_short_name(self):
        return self.name

    def get_definition_name(self):
        return self.definitionName
    
    def get_node(self):
        return self.node
    
    def get_path(self):
        return self.path

# Module configuration node(root node for the respective module)
class demo(AutosarNode):
    def __init__(self, node):
        super().__init__(node, 'demo')
        
        self.contA = None
        self.contBs = []


        for container in node.findall('{*}CONTAINERS/{*}ECUC-CONTAINER-VALUE'):
            definitionRef = container.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'contA':
                    self.contA = contA(container)
                elif definitionName == 'contB':
                    self.contBs.append(contB(container))

    

    #Returns the configuration container contA
    def get_contA(self):
        return self.contA  

    #Returns the configuration container contB
    def get_contBs(self):
        return self.contBs  



# Container configuration node for contA
class contA(AutosarNode):
    def __init__(self, node):
        super().__init__(node, 'contA')
        self.isChoiceContainer = False
        #parameters
        self.boolParam_value = None
        self.enumParam_value = None

        for parameter in node.findall('{*}PARAMETER-VALUES/*'):
            definitionRef = parameter.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'boolParam':
                    self.boolParam_value = self.boolParam(parameter)
                elif definitionName == 'enumParam':
                    self.enumParam_value = self.enumParam(parameter)

    def is_choice_container(self):
        return self.isChoiceContainer


    #Returns the parameter boolParam
    def get_boolParam(self):
        return self.boolParam_value

    #Returns the parameter enumParam
    def get_enumParam(self):
        return self.enumParam_value



    # Parameter configuration node for boolParam
    class boolParam(AutosarNode):
        def __init__(self, node):
            super().__init__(node, 'boolParam')
            self.value = None
            valueNode = node.find('{*}VALUE')
            paramValue = valueNode.text if valueNode is not None else None
            if paramValue is not None and paramValue == '1':
                self.value = True
            else:
                self.value = False

            self.type = ParameterTypes.BOOLEAN
            self.isDefaultValueSet = True
            self.defaultValue = False

        #Get the parameter value
        def get_value(self):
            return self.value

        #Get the type of parameter(if INTEGER, BOOLEAN, STRING, FUNCTION, FLOAT or ENUMERATION)
        def get_type(self):
            return self.type
    
        def is_default_value_set(self):
            return self.isDefaultValueSet
    
        def get_default_value(self):
            return self.defaultValue
    



    # Parameter configuration node for enumParam
    class enumParam(AutosarNode):
        def __init__(self, node):
            super().__init__(node, 'enumParam')
            self.value = None
            valueNode = node.find('{*}VALUE')
            paramValue = valueNode.text if valueNode is not None else None
            self.value = paramValue
            self.type = ParameterTypes.ENUMERATION
            self.isDefaultValueSet = True
            self.defaultValue = 'GREEN'
            self.enumLiterals = ['RED', 'YELLOW', 'GREEN']

        #Get the parameter value
        def get_value(self):
            return self.value

        #Get the type of parameter(if INTEGER, BOOLEAN, STRING, FUNCTION, FLOAT or ENUMERATION)
        def get_type(self):
            return self.type
    
        def is_default_value_set(self):
            return self.isDefaultValueSet
    
        def get_default_value(self):
            return self.defaultValue
    

        def get_enum_literals(self):
            return self.enumLiterals



# Container configuration node for contB
class contB(AutosarNode):
    def __init__(self, node):
        super().__init__(node, 'contB')
        self.isChoiceContainer = False
        #containers
        self.subConts = []

        for subContainer in node.findall('{*}SUB-CONTAINERS/{*}ECUC-CONTAINER-VALUE'):
            definitionRef = subContainer.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'subCont':
                    self.subConts.append(subCont(subContainer))

    def is_choice_container(self):
        return self.isChoiceContainer


    #Returns the configuration container subCont
    def get_subConts(self):
        return self.subConts  


# Container configuration node for subCont
class subCont(AutosarNode):
    def __init__(self, node):
        super().__init__(node, 'subCont')
        self.isChoiceContainer = False
        #parameters
        self.intParam_value = None

        for parameter in node.findall('{*}PARAMETER-VALUES/*'):
            definitionRef = parameter.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'intParam':
                    self.intParam_value = self.intParam(parameter)
        #references
        self.ref1_value = None
        self.foreignRef_value = None

        for reference in node.findall('{*}REFERENCE-VALUES/*'):
            definitionRef = reference.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'ref1':
                    self.ref1_value = self.ref1(reference)
                elif definitionName == 'foreignRef':
                    self.foreignRef_value = self.foreignRef(reference)

    def is_choice_container(self):
        return self.isChoiceContainer


    #Returns the parameter intParam
    def get_intParam(self):
        return self.intParam_value

    #Returns the reference ref1
    def get_ref1(self):
        return self.ref1_value

    #Returns the reference foreignRef
    def get_foreignRef(self):
        return self.foreignRef_value



    # Parameter configuration node for intParam
    class intParam(AutosarNode):
        def __init__(self, node):
            super().__init__(node, 'intParam')
            self.value = None
            valueNode = node.find('{*}VALUE')
            paramValue = valueNode.text if valueNode is not None else None
            if paramValue is not None:
                self.value = int(paramValue)

            self.type = ParameterTypes.INTEGER
            self.isDefaultValueSet = False
            self.defaultValue = None
            self.isMinValueSet = True
            self.min = 0
            self.isMaxValueSet = True
            self.max = 65535


        #Get the parameter value
        def get_value(self):
            return self.value

        #Get the type of parameter(if INTEGER, BOOLEAN, STRING, FUNCTION, FLOAT or ENUMERATION)
        def get_type(self):
            return self.type
    
        def is_default_value_set(self):
            return self.isDefaultValueSet
    
        def get_default_value(self):
            return self.defaultValue
    

        def is_min_value_set(self):
            return self.isMinValueSet
    
        def get_min_value(self):
            return self.min
    
        def is_max_value_set(self):
            return self.isMaxValueSet
    
        def get_max_value(self):
            return self.max



    # Reference configuration node for ref1
    class ref1(AutosarNode):
        def __init__(self, node):
            super().__init__(node, 'ref1')
            valueNode = node.find('{*}VALUE-REF')
            self.value = valueNode.text if valueNode is not None else None
            self.type = ReferenceTypes.SIMPLE_REFERENCE
            self.destinationRef = '/ModuleDef/demo_other/contA'


        #Get the referenced node
        def get_value(self):
            return self.value

        #Get the type of reference(if SIMPLE_REFERENCE, CHOICE_REFERENCE or FOREIGN_REFERENCE)
        def get_type(self):
            return self.type
    

        #Gets the value of DESTINATION-REF from the definition file.
        def get_destination_ref(self):
            return self.destinationRef



    # Reference configuration node for foreignRef
    class foreignRef(AutosarNode):
        def __init__(self, node):
            super().__init__(node, 'foreignRef')
            valueNode = node.find('{*}VALUE-REF')
            self.value = valueNode.text if valueNode is not None else None
            self.type = ReferenceTypes.FOREIGN_REFERENCE
            self.destinationType = 'SW-COMPONENT-PROTOTYPE'

        #Get the referenced node
        def get_value(self):
            return self.value

        #Get the type of reference(if SIMPLE_REFERENCE, CHOICE_REFERENCE or FOREIGN_REFERENCE)
        def get_type(self):
            return self.type
    

        #Gets the value of DESTINATION-TYPE from the definition file for FOREIGN_REFERENCE.
        def get_destination_type(self):
            return self.destinationType


