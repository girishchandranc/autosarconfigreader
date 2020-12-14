"""
The python file contains the different classes for accessing the containers and parameters of the 'demo_other' module.
This file is generated for the module 'demo_other' on Mon Dec 14 22:46:56 2020.
"""

from lxml import etree
from enum import Enum

# Enums for possible parameter and reference types
ParameterTypes = Enum('ParameterTypes', 'INTEGER FLOAT BOOLEAN STRING FUNCTION ENUMERATION')
ReferenceTypes = Enum('ReferenceTypes', 'SIMPLE_REFERENCE CHOICE_REFERENCE FOREIGN_REFERENCE')

# dict supposed to be used internally by the module to store the path and its corresponding autosar node
pathsToNodeDict = {}
# dict supposed to be used internally by the module to store the instances of autosar node for the definition path
definitionPathToNodesDict = {}

def read_and_build_module_configuration(file):
    """
    Reads the module configuration and build the demo_other structure.

    @param file: The configuration arxml file.
    @return:  The built demo_other structure. May return None if the given 
              file do not contain the module configuration for
              demo_other.
    """
    #Clearing the cache if any before building the module
    pathsToNodeDict.clear()
    definitionPathToNodesDict.clear()

    rootAutosarNode = etree.parse(file)
    moduleConfNode = None
    #{*} is used to consider the wildcard namespace.
    for module in rootAutosarNode.findall('//{*}ECUC-MODULE-CONFIGURATION-VALUES'):
        definitionRef = module.find('{*}DEFINITION-REF').text
        if definitionRef is not None and definitionRef.split('/').pop() == 'demo_other':
            moduleConfNode = module
            break

    if moduleConfNode is not None:
        return demo_other(file, rootAutosarNode, moduleConfNode)
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

def get_nodes_for_definition_path(path):
    """
    Returns the autosar nodes for the corresponding definition path.

    @param path: The fully qualified autosar path starting from the module name 
                 and avoiding the Ar-package(eg: /Module/Container1).
    @return:  The nodes corresponding to the path or None if the node for path is not available.
    """
    if path in definitionPathToNodesDict:
        return definitionPathToNodesDict[path]
    else:
        return None

# Base class for all autosar nodes
class AutosarNode:
    def __init__(self, parent, node, definitionName, definitionPath):
        """
        Constructor for any Autosar node.

        @param parent: The parent node under which the autosar node needs to be created.
        @param node: The xml node for which the autosar node needs to be created.
        @param definitionName: The definition short name of the node.
        @param definitionPath: The fully qualified path of the definition node.
        """
        self.__parent = parent
        self.__node = node
        self.__name = None
        shortNameNode = node.find('{*}SHORT-NAME')
        if shortNameNode is not None:
            self.__name = shortNameNode.text
        else:
            self.__name = definitionName
        self.__definitionName = definitionName
        names = []
        names.append(self.__name)
        self.__compute_path(node.getparent(), names)
        self.__path = self.__build_path(reversed(names))
        pathsToNodeDict[self.__path] = self

        if definitionPath == self.__get_definition_path_of_node(node):
            if definitionPath not in definitionPathToNodesDict:
                nodes = []
                definitionPathToNodesDict[definitionPath] = nodes

            definitionPathToNodesDict[definitionPath].append(self)

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
        for name in names:
            returnValue = returnValue + '/' + name
        return returnValue
    
    def __get_definition_path_of_node(self, node):
        definitionPath = None
        definitionRef = node.find('{*}DEFINITION-REF').text
        if definitionRef is not None:
            defNameList = definitionRef.split('/')
            resulantDefNames = []
            moduleFound = False
            for name in defNameList:
                if name == 'demo_other':
                    moduleFound = True
                if moduleFound:
                    resulantDefNames.append(name)
            definitionPath = self.__build_path(resulantDefNames)
        return definitionPath

    def get_parent(self):
        return self.__parent

    def get_short_name(self):
        return self.__name

    def get_definition_name(self):
        return self.__definitionName
    
    def get_node(self):
        return self.__node
    
    def get_path(self):
        return self.__path

    def _set_model_modified(self, value):
        """ 
        To be set when a model is modified. It calls 
        the parent until the module node is found. 
        Please check the module sub class for more info.
        """
        self.__parent._set_model_modified(value)

# Module configuration node(root node for the respective module)
class demo_other(AutosarNode):
    def __init__(self, file, rootNode, node):
        """
        Constructor for demo_other node.

        @param file: The input file used to create the module.
        @param rootNode: The root node corresponding to the file.
        @param node: The xml node for which the autosar node needs to be created.
        """
        super().__init__(None, node, 'demo_other', '/demo_other')
        self.__rootNode = rootNode
        self.__file = file
        self.__isModelModified = False
        
        self.__contA = None
        self.__contBs = []


        for container in node.findall('{*}CONTAINERS/{*}ECUC-CONTAINER-VALUE'):
            definitionRef = container.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'contA':
                    self.__contA = contA(self, container)
                elif definitionName == 'contB':
                    self.__contBs.append(contB(self, container))

    def _set_model_modified(self, value):
        self.__isModelModified = True
    
    def is_model_modified(self):
        return self.__isModelModified


    #Returns the configuration container contA
    def get_contA(self):
        return self.__contA  

    #Returns the configuration container contB
    def get_contBs(self):
        return self.__contBs  


    def save(self, file = None):
        """
        Saves the configuration:
            - To the file passed as argument
            - Overwrite the existing file if no argument is provided
        
        Raises an exception if save() is called without a module

        @param file: The file location where the configuration needs to be saved.
        """
        if self.__isModelModified is False:
            return 'The model is not changed. Ignoring the save request!'
        elif file is not None:
            self.__rootNode.write(file, pretty_print=True, xml_declaration=True,   encoding="utf-8")
        else:
            self.__rootNode.write(self.__file, pretty_print=True, xml_declaration=True,   encoding="utf-8")
        return 'The model saved!'


# Container configuration node for contA
class contA(AutosarNode):
    def __init__(self, parent, node):
        """
        Constructor for contA node.

        @param parent: The parent node under which the autosar node needs to be created.
        @param node: The xml node for which the autosar node needs to be created.
        """
        super().__init__(parent, node, 'contA', '/demo_other/contA')
        self.__isChoiceContainer = False
        #parameters
        self.__boolParam_value = None
        self.__enumParam_value = None

        for parameter in node.findall('{*}PARAMETER-VALUES/*'):
            definitionRef = parameter.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'boolParam':
                    self.__boolParam_value = self.boolParam(self, parameter)
                elif definitionName == 'enumParam':
                    self.__enumParam_value = self.enumParam(self, parameter)

    def is_choice_container(self):
        return self.__isChoiceContainer


    #Returns the parameter boolParam
    def get_boolParam(self):
        return self.__boolParam_value

    #Returns the parameter enumParam
    def get_enumParam(self):
        return self.__enumParam_value



    # Parameter configuration node for boolParam
    class boolParam(AutosarNode):
        def __init__(self, parent, node):
            """
            Constructor for boolParam node.

            @param parent: The parent node under which the autosar node needs to be created.
            @param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'boolParam', '/demo_other/contA/boolParam')
            self.__value = None
            self.__valueNode = node.find('{*}VALUE')
            paramValue = self.__valueNode.text if self.__valueNode is not None else None
            if paramValue is not None and paramValue == '1':
                self.__value = True
            else:
                self.__value = False

            self.__type = ParameterTypes.BOOLEAN
            self.__isDefaultValueSet = True
            self.__defaultValue = False

        #Get the parameter value
        def get_value(self):
            return self.__value
        
        #set the parameter value
        def set_value(self, value):
            self.__value = value
            self.__valueNode.text = '1' if value else '0'
            self._set_model_modified(True)

        #Get the type of parameter(if INTEGER, BOOLEAN, STRING, FUNCTION, FLOAT or ENUMERATION)
        def get_type(self):
            return self.__type
    
        def is_default_value_set(self):
            return self.__isDefaultValueSet
    
        def get_default_value(self):
            return self.__defaultValue
    



    # Parameter configuration node for enumParam
    class enumParam(AutosarNode):
        def __init__(self, parent, node):
            """
            Constructor for enumParam node.

            @param parent: The parent node under which the autosar node needs to be created.
            @param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'enumParam', '/demo_other/contA/enumParam')
            self.__value = None
            self.__valueNode = node.find('{*}VALUE')
            paramValue = self.__valueNode.text if self.__valueNode is not None else None
            self.__value = paramValue
            self.__type = ParameterTypes.ENUMERATION
            self.__isDefaultValueSet = True
            self.__defaultValue = 'GREEN'
            self.__enumLiterals = ['RED', 'YELLOW', 'GREEN']

        #Get the parameter value
        def get_value(self):
            return self.__value
        
        #set the parameter value
        def set_value(self, value):
            if value in self.__enumLiterals:
                self.__value = value
                self.__valueNode.text = value
                self._set_model_modified(True)
            else:
                raise ValueNotPossibleError(message = 'Cannot set the value {}. Only the values {} are possible'.format(value, str(self.__enumLiterals)))

        #Get the type of parameter(if INTEGER, BOOLEAN, STRING, FUNCTION, FLOAT or ENUMERATION)
        def get_type(self):
            return self.__type
    
        def is_default_value_set(self):
            return self.__isDefaultValueSet
    
        def get_default_value(self):
            return self.__defaultValue
    

        def get_enum_literals(self):
            return self.__enumLiterals



# Container configuration node for contB
class contB(AutosarNode):
    def __init__(self, parent, node):
        """
        Constructor for contB node.

        @param parent: The parent node under which the autosar node needs to be created.
        @param node: The xml node for which the autosar node needs to be created.
        """
        super().__init__(parent, node, 'contB', '/demo_other/contB')
        self.__isChoiceContainer = False
        #containers
        self.__subConts = []

        for subContainer in node.findall('{*}SUB-CONTAINERS/{*}ECUC-CONTAINER-VALUE'):
            definitionRef = subContainer.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'subCont':
                    self.__subConts.append(subCont(self, subContainer))

    def is_choice_container(self):
        return self.__isChoiceContainer


    #Returns the configuration container subCont
    def get_subConts(self):
        return self.__subConts  


# Container configuration node for subCont
class subCont(AutosarNode):
    def __init__(self, parent, node):
        """
        Constructor for subCont node.

        @param parent: The parent node under which the autosar node needs to be created.
        @param node: The xml node for which the autosar node needs to be created.
        """
        super().__init__(parent, node, 'subCont', '/demo_other/contB/subCont')
        self.__isChoiceContainer = False
        #parameters
        self.__intParam_value = None

        for parameter in node.findall('{*}PARAMETER-VALUES/*'):
            definitionRef = parameter.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'intParam':
                    self.__intParam_value = self.intParam(self, parameter)
        #references
        self.__ref1_value = None
        self.__foreignRef_value = None

        for reference in node.findall('{*}REFERENCE-VALUES/*'):
            definitionRef = reference.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'ref1':
                    self.__ref1_value = self.ref1(self, reference)
                elif definitionName == 'foreignRef':
                    self.__foreignRef_value = self.foreignRef(self, reference)

    def is_choice_container(self):
        return self.__isChoiceContainer


    #Returns the parameter intParam
    def get_intParam(self):
        return self.__intParam_value

    #Returns the reference ref1
    def get_ref1(self):
        return self.__ref1_value

    #Returns the reference foreignRef
    def get_foreignRef(self):
        return self.__foreignRef_value



    # Parameter configuration node for intParam
    class intParam(AutosarNode):
        def __init__(self, parent, node):
            """
            Constructor for intParam node.

            @param parent: The parent node under which the autosar node needs to be created.
            @param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'intParam', '/demo_other/contB/subCont/intParam')
            self.__value = None
            self.__valueNode = node.find('{*}VALUE')
            paramValue = self.__valueNode.text if self.__valueNode is not None else None
            if paramValue is not None:
                self.__value = int(paramValue)

            self.__type = ParameterTypes.INTEGER
            self.__isDefaultValueSet = False
            self.__defaultValue = None
            self.__isMinValueSet = True
            self.__min = 0
            self.__isMaxValueSet = True
            self.__max = 65535


        #Get the parameter value
        def get_value(self):
            return self.__value
        
        #set the parameter value
        def set_value(self, value):
            if value >= self.__min and value <= self.__max:
                self.__value = value
                self.__valueNode.text = str(value)
                self._set_model_modified(True)
            else:
                raise ValueNotPossibleError(message = 'Cannot set the value {}. Only the values between {} and {} are possible'.format(str(value), str(self.__min), str(self.__max)))

        #Get the type of parameter(if INTEGER, BOOLEAN, STRING, FUNCTION, FLOAT or ENUMERATION)
        def get_type(self):
            return self.__type
    
        def is_default_value_set(self):
            return self.__isDefaultValueSet
    
        def get_default_value(self):
            return self.__defaultValue
    

        def is_min_value_set(self):
            return self.__isMinValueSet
    
        def get_min_value(self):
            return self.__min
    
        def is_max_value_set(self):
            return self.__isMaxValueSet
    
        def get_max_value(self):
            return self.__max



    # Reference configuration node for ref1
    class ref1(AutosarNode):
        def __init__(self, parent, node):
            """
            Constructor for ref1 node.

            @param parent: The parent node under which the autosar node needs to be created.
            @param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'ref1', '/demo_other/contB/subCont/ref1')
            self.__valueNode = node.find('{*}VALUE-REF')
            self.__value = self.__valueNode.text if self.__valueNode is not None else None
            self.__type = ReferenceTypes.SIMPLE_REFERENCE
            self.__destinationRef = '/ModuleDef/demo_other/contA'


        #Get the reference value
        def get_value(self):
            return self.__value

        #set the reference value
        def set_value(self, value):
            self.__value = value
            self.__valueNode.text = value
            self._set_model_modified(True)

        #Get the type of reference(if SIMPLE_REFERENCE, CHOICE_REFERENCE or FOREIGN_REFERENCE)
        def get_type(self):
            return self.__type
    

        #Gets the value of DESTINATION-REF from the definition file.
        def get_destination_ref(self):
            return self.__destinationRef



    # Reference configuration node for foreignRef
    class foreignRef(AutosarNode):
        def __init__(self, parent, node):
            """
            Constructor for foreignRef node.

            @param parent: The parent node under which the autosar node needs to be created.
            @param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'foreignRef', '/demo_other/contB/subCont/foreignRef')
            self.__valueNode = node.find('{*}VALUE-REF')
            self.__value = self.__valueNode.text if self.__valueNode is not None else None
            self.__type = ReferenceTypes.FOREIGN_REFERENCE
            self.__destinationType = 'SW-COMPONENT-PROTOTYPE'

        #Get the reference value
        def get_value(self):
            return self.__value

        #set the reference value
        def set_value(self, value):
            self.__value = value
            self.__valueNode.text = value
            self._set_model_modified(True)

        #Get the type of reference(if SIMPLE_REFERENCE, CHOICE_REFERENCE or FOREIGN_REFERENCE)
        def get_type(self):
            return self.__type
    

        #Gets the value of DESTINATION-TYPE from the definition file for FOREIGN_REFERENCE.
        def get_destination_type(self):
            return self.__destinationType




# Exception classes
class ValueNotPossibleError(Exception):
    """Exception raised when the provided value is not possible to set for the parameter"""
    def __init__(self, message):
        super().__init__(message)

class FileSaveError(Exception):
    """Exception raised when the file is unable to save"""
    def __init__(self, message):
        super().__init__(message)