"""
The python file contains the different classes for accessing/creating the 
containers and parameters of the 'demo_other' module.
This file is generated for the module 'demo_other' on Fri Jan  8 11:13:18 2021.
"""

from lxml import etree
from enum import Enum
import os

# Enums for possible parameter and reference types
ParameterTypes = Enum('ParameterTypes', 'INTEGER FLOAT BOOLEAN STRING FUNCTION ENUMERATION')
ReferenceTypes = Enum('ReferenceTypes', 'SIMPLE_REFERENCE CHOICE_REFERENCE FOREIGN_REFERENCE')

# dict supposed to be used internally by the module to store the path and its corresponding autosar node
__pathsToNodeDict__ = {}
# dict supposed to be used internally by the module to store the instances of autosar node for the definition path
__definitionPathToNodesDict__ = {}

# demo_other node
__demo_otherNode__ = None


# namespace for autosar arxml files
__autosarNsMap__ = {None: "http://autosar.org/schema/r4.0", 'xsi': "http://www.w3.org/2001/XMLSchema-instance"}
__rootSchemaAttr__ = {'{http://www.w3.org/2001/XMLSchema-instance}schemaLocation': 'http://autosar.org/schema/r4.0 AUTOSAR_00049.xsd'}


def read(file, ignore_previous_loaded_node=False):
    """
    Reads the module configuration and build the demo_other structure.

    :param file: The configuration arxml file.
    :param ignore_previous_loaded_node: Set True to ignore the previously loaded demo_other 
                                        via 'read'/'new' method.
    :return:  The built demo_other structure. May return None if the given 
              file do not contain the module configuration for demo_other.
    
    :raise: ModuleAlreadyLoaded, if the module is already loaded and the argument 
                                 'ignore_previous_loaded_node' is False
    :raise: ModuleNotFoundError, if the module is not found in the input 'file'
    """
    global __demo_otherNode__
    # Clearing the cache if any before building the module
    __pathsToNodeDict__.clear()
    __definitionPathToNodesDict__.clear()

    if __demo_otherNode__ is not None and ignore_previous_loaded_node is False:
        raise ModuleAlreadyLoaded('The module demo_other is already loaded. To ignore the previously loaded module, please set True for argument ignore_previous_loaded_node.')

    rootAutosarNode = etree.parse(file, etree.XMLParser(remove_blank_text=True))
    moduleConfNode = None
    # {*} is used to consider the wildcard namespace.
    for module in rootAutosarNode.findall('//{*}ECUC-MODULE-CONFIGURATION-VALUES'):
        definitionRef = module.find('{*}DEFINITION-REF').text
        if definitionRef is not None and definitionRef.split('/').pop() == 'demo_other':
            moduleConfNode = module
            break

    if moduleConfNode is not None:
        __demo_otherNode__ = demo_other(file, rootAutosarNode, moduleConfNode)
    else:
        raise ModuleNotFoundError('The module demo_other not found in the input file {}.'.format(file))

    return __demo_otherNode__


def new(path, ignore_previous_loaded_node=False, over_write=False, add_mandatory_containers=False):
    """
    Creates a new file and return the demo_other..

    :param path: The absolute path where the file needs to be created.
    :param ignore_previous_loaded_node: Set True to ignore the previously loaded demo_other 
                                        via 'read'/'new' method.
    :param over_write: Pass True if the new file should overwrite if
                      a file is already present in the given path.
    :param add_mandatory_containers: Pass True if the the mandatory containers for the 
                                     module should be created(please note that this 
                                     depends on the attribute "LOWER-MULTIPLICITY" of 
                                     the respective containers from the definition file. 
                                     This option has no relevance if there are no container
                                     with "LOWER-MULTIPLICITY" greater than 0).

    :return: The built demo_other structure.

    :raise: ModuleAlreadyLoaded, if the module is already loaded and the argument 
                                 'ignore_previous_loaded_node' is False
    :raise: FileExistsError, file already exist when the argument overWrite is 
                              not provided or is False
    """
    global __demo_otherNode__
    if __demo_otherNode__ is not None and ignore_previous_loaded_node is False:
        raise ModuleAlreadyLoaded('The module demo_other is already loaded. To ignore the previously loaded module, please set True for argument ignore_previous_loaded_node.')

    if os.path.isfile(path) and over_write is False:
        raise FileExistsError('File {} already exists. If it needs overwriting, then please set True for argument over_write.'.format(path))

    # Create file
    root = etree.Element('AUTOSAR', nsmap=__autosarNsMap__, attrib=__rootSchemaAttr__)
    arpackages = etree.SubElement(root, 'AR-PACKAGES')

    arpackage = AutosarNode._create_node('AR-PACKAGE', short_name='demo_other')
    arpackages.append(arpackage)
    
    elements = etree.SubElement(arpackage, 'ELEMENTS')
    moduleConf = AutosarNode._create_node('ECUC-MODULE-CONFIGURATION-VALUES', short_name='demo_other', dest='ECUC-MODULE-DEF', definition_ref='/ModuleDef/demo_other')
    elements.append(moduleConf)
    et = etree.ElementTree(root)

    # Now create the demo_other object
    __demo_otherNode__ = demo_other(path, et, moduleConf)
    # Adding mandatory containers
    if add_mandatory_containers:
        __demo_otherNode__.new_contA('contA_0', add_mandatory_containers)

    et.write(path, pretty_print=True, xml_declaration=True,   encoding="utf-8")

    return __demo_otherNode__


def get_node(path):
    """
    Returns the autosar node for the corresponding path.

    :param path: The fully qualified autosar path for eg: /Autosar/Module/Container1.
    :return:  The node corresponding to the path or None if the node for path is not available.
    """
    if path in __pathsToNodeDict__:
        return __pathsToNodeDict__[path]
    else:
        return None


def get_nodes_for_definition_path(path):
    """
    Returns the autosar nodes for the corresponding definition path.

    :param path: The fully qualified autosar path starting from the module name 
                 and avoiding the Ar-package(eg: /Module/Container1).
    :return:  The nodes corresponding to the path or None if the node for path is not available.
    """
    if path in __definitionPathToNodesDict__:
        return __definitionPathToNodesDict__[path]
    else:
        return None


def reinit():
    """
    Re-initialize the package. All the loaded model entities(from input
    /newly created files, modified/new model objects) will be removed.
    """
    global __demo_otherNode__
    __demo_otherNode__ = None # Reinit the module.
    __pathsToNodeDict__.clear() # Clearing the cache
    __definitionPathToNodesDict__.clear()



# Base class for all autosar nodes
class AutosarNode:
    def __init__(self, parent, node, definitionName, definitionPath):
        """
        Constructor for any Autosar node.

        :param parent: The parent node under which the autosar node needs to be created.
        :param node: The xml node for which the autosar node needs to be created.
        :param definitionName: The definition short name of the node.
        :param definitionPath: The fully qualified path of the definition node.
        """
        self._parent = parent
        self._node = node
        self.name = None
        shortNameNode = node.find('{*}SHORT-NAME')
        if shortNameNode is not None:
            self.name = shortNameNode.text
        else:
            self.name = definitionName

        self.definitionName = definitionName
        self.definitionPath = definitionPath

        self.path = ''
        if parent is not None:
            self.path = parent.path + '/' + self.name
        else:
            names = []
            names.append(self.name)
            self.__compute_path(node.getparent(), names)
            self.path = self.__build_path(reversed(names))
        __pathsToNodeDict__[self.path] = self

        if definitionPath == self.__get_definition_path_of_node(node):
            if definitionPath not in __definitionPathToNodesDict__:
                nodes = []
                __definitionPathToNodesDict__[definitionPath] = nodes

            __definitionPathToNodesDict__[definitionPath].append(self)


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


    def __compute_path(self, node, names):
        #get all path until the AUTOSAR root node
        if etree.QName(node).localname == 'AUTOSAR':
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


    def get_node(self):
        return self._node


    def get_parent(self):
        return self._parent


    def _set_model_modified(self, value):
        """ 
        To be set when a model is modified. It calls 
        the parent until the module node is found. 
        Please check the module sub class for more info.
        """
        self._parent._set_model_modified(value)


    @staticmethod
    def _add_or_get_xml_node(parentNode, tag_name, dest=None):
        """
        Get or create a new xml node with the tagName.
        :param tag_name: The tag name which needs to be created.
        :param dest: optional DEST attribte for the tags.
        """
        xmlNode = parentNode.find('{*}' + tag_name)
        if xmlNode is None:
            xmlNode = etree.SubElement(parentNode, tag_name, attrib = ({'DEST' : dest} if dest is not None else None))

        return xmlNode


    @staticmethod
    def _create_node(tag_name, short_name=None, dest=None, definition_ref=None):
        element = etree.Element(tag_name)
        if short_name is not None:
            shortNameNode = etree.SubElement(element , 'SHORT-NAME')
            shortNameNode.text = short_name
        if dest is not None and definition_ref is not None:
            defRef = etree.SubElement(element , 'DEFINITION-REF', attrib = {'DEST' : dest})
            defRef.text = definition_ref

        return element


    def __repr__(self):
        return (self.__class__.__name__ + '(' + self.path + ')')


    def __hash__(self):
        return hash(self.path)


    def __eq__(self, other):
        return (self.path == other.path)


# Module configuration node(root node for the respective module)
class demo_other(AutosarNode):
    def __init__(self, file, rootNode, node):
        """
        Constructor for demo_other node.

        :param file: The input file used to create the module.
        :param rootNode: The root node corresponding to the file.
        :param node: The xml node for which the autosar node needs to be created.
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


    def get_contA(self):
        return self.__contA

    def remove_contA(self):
        containers = AutosarNode._add_or_get_xml_node(self._node, 'CONTAINERS')
        containers.remove(self.__contA._node)
        self.__contA = None
        self._set_model_modified(True)


    def new_contA(self, name, add_mandatory_elements=False):
        """
        Creates a new contA with the given name.
        :param: The name of the container
        :param add_mandatory_elements: Pass True if the the mandatory sub-containers/parameters/references 
                                       for should be created(please note that this depends on the attribute 
                                       "LOWER-MULTIPLICITY" of the respective containers/parameters/references 
                                       from the definition file. This option has no relevance if there are no 
                                       containers/parameters/references with "LOWER-MULTIPLICITY" greater than 0).
        :raise InvalidChildNodeException: If a container with same name already exists, 
                                          or if the maximum allowed instance is reached.
        """
        if self.__contA is not None:
            raise InvalidChildNodeException('Operation not possible. contA already exists. Use get_contA to access the container.')

        containers = AutosarNode._add_or_get_xml_node(self._node, 'CONTAINERS')
        xmlNode = AutosarNode._create_node('ECUC-CONTAINER-VALUE', short_name=name, dest='ECUC-PARAM-CONF-CONTAINER-DEF', definition_ref='/ModuleDef/demo_other')
        containers.append(xmlNode)
        self.__contA = contA(self, xmlNode)
        self._set_model_modified(True)
        return self.__contA

    


    def get_contBs(self):
        return self.__contBs

    def __add_contB(self, value):
        """
        Adds a new contB.
        :raise InvalidChildNodeException: If a container with same name already exists, 
                                          or if the maximum allowed instance is reached.
        """
        if value in self.__get_children():
            raise InvalidChildNodeException('Operation not possible. A container with name {} already present in {}.'.format(value.name, self))

        containers = AutosarNode._add_or_get_xml_node(self._node, 'CONTAINERS')
        self.__contBs.append(value)
        containers.append(value._node)
        self._set_model_modified(True)

    def remove_contB(self, value):
        if value is not None:
            containers = AutosarNode._add_or_get_xml_node(self._node, 'CONTAINERS')
            containers.remove(value._node)
            self.__contBs.remove(value)
            self._set_model_modified(True)

    def removeAll_contB(self):
        for cont in self.__contBs:
            self.remove_contB(cont)


    def new_contB(self, name, add_mandatory_elements=False):
        """
        Creates a new contB with the given name.
        :param: The name of the container
        :param add_mandatory_elements: Pass True if the the mandatory sub-containers/parameters/references 
                                       for should be created(please note that this depends on the attribute 
                                       "LOWER-MULTIPLICITY" of the respective containers/parameters/references 
                                       from the definition file. This option has no relevance if there are no 
                                       containers/parameters/references with "LOWER-MULTIPLICITY" greater than 0).
        :raise InvalidChildNodeException: If a container with same name already exists, 
                                          or if the maximum allowed instance is reached.
        """
        xmlNode = AutosarNode._create_node('ECUC-CONTAINER-VALUE', short_name=name, dest='ECUC-PARAM-CONF-CONTAINER-DEF', definition_ref='/ModuleDef/demo_other/contB')
        value = contB(self, xmlNode)
        self.__add_contB(value)
        return value

    



    def __get_children(self):
        children = []
        if self.__contA is not None:
            children.append(self.__contA)
        children.extend(self.__contBs)
        return children


    def save(self, file=None):
        """
        Saves the configuration:
            - To the file passed as argument
            - Overwrite the existing file if no argument is provided
        
        :param file: The file location where the configuration needs to be saved.
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

        :param parent: The parent node under which the autosar node needs to be created.
        :param node: The xml node for which the autosar node needs to be created.
        """
        super().__init__(parent, node, 'contA', '/demo_other/contA')
        self.__isChoiceContainer = False
        # parameters
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



    def __get_children(self):
        children = []
        return children


    def get_boolParam(self):
        return self.__boolParam_value

    def new_boolParam(self):
        """
        Creates a new boolParam.
        :raise InvalidChildNodeException: If the parameter already exists.
        """
        if self.__boolParam_value is not None:
            raise InvalidChildNodeException('Operation not possible. boolParam already exists. Use get_boolParam to access the parameter.')

        paremeters = AutosarNode._add_or_get_xml_node(self._node, 'PARAMETER-VALUES')
        xmlNode = AutosarNode._create_node('ECUC-NUMERICAL-PARAM-VALUE', dest='ECUC-BOOLEAN-PARAM-DEF', definition_ref='/ModuleDef/demo_other/contA/boolParam')
        
        paremeters.append(xmlNode)
        value = AutosarNode._add_or_get_xml_node(self._node, 'VALUE')
        # set default value if available
        value.text = '0'
        
        xmlNode.append(value)

        self.__boolParam_value = self.boolParam(self, xmlNode)
        self._set_model_modified(True)
        return self.__boolParam_value


    def get_enumParam(self):
        return self.__enumParam_value

    def new_enumParam(self):
        """
        Creates a new enumParam.
        :raise InvalidChildNodeException: If the parameter already exists.
        """
        if self.__enumParam_value is not None:
            raise InvalidChildNodeException('Operation not possible. enumParam already exists. Use get_enumParam to access the parameter.')

        paremeters = AutosarNode._add_or_get_xml_node(self._node, 'PARAMETER-VALUES')
        xmlNode = AutosarNode._create_node('ECUC-TEXTUAL-PARAM-VALUE', dest='ECUC-ENUMERATION-PARAM-DEF', definition_ref='/ModuleDef/demo_other/contA/enumParam')
        paremeters.append(xmlNode)
        value = AutosarNode._add_or_get_xml_node(self._node, 'VALUE')
        # set default value if available
        value.text = str('GREEN')
        xmlNode.append(value)

        self.__enumParam_value = self.enumParam(self, xmlNode)
        self._set_model_modified(True)
        return self.__enumParam_value




    # Parameter configuration node for boolParam
    class boolParam(AutosarNode):
        def __init__(self, parent, node):
            """
            Constructor for boolParam node.

            :param parent: The parent node under which the autosar node needs to be created.
            :param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'boolParam', '/demo_other/contA/boolParam')
            self.__value = None
            self.__valueNode = node.find('{*}VALUE')
            paramValue = self.__valueNode.text if self.__valueNode is not None else None
            self.__valueNode = AutosarNode._add_or_get_xml_node(node, 'VALUE') if self.__valueNode is None else self.__valueNode
            if paramValue is not None and paramValue == '1':
                self.__value = True
            else:
                self.__value = False

            self.__type = ParameterTypes.BOOLEAN
            self.__isDefaultValueSet = True
            self.__defaultValue = False

        def get_value(self):
            """
            Returns the parameter value
            """
            return self.__value
        
        def set_value(self, value):
            """
            Set a new value for the parameter
            """
            self.__value = value
            self.__valueNode.text = '1' if value else '0'
            self._set_model_modified(True)

        def get_type(self):
            """
            Returns the type of parameter(if INTEGER, BOOLEAN, STRING, FUNCTION, FLOAT or ENUMERATION)
            """
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

            :param parent: The parent node under which the autosar node needs to be created.
            :param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'enumParam', '/demo_other/contA/enumParam')
            self.__value = None
            self.__valueNode = node.find('{*}VALUE')
            paramValue = self.__valueNode.text if self.__valueNode is not None else None
            self.__valueNode = AutosarNode._add_or_get_xml_node(node, 'VALUE') if self.__valueNode is None else self.__valueNode
            self.__value = paramValue
            self.__type = ParameterTypes.ENUMERATION
            self.__isDefaultValueSet = True
            self.__defaultValue = 'GREEN'
            self.__enumLiterals = ['RED', 'YELLOW', 'GREEN']

        def get_value(self):
            """
            Returns the parameter value
            """
            return self.__value
        
        def set_value(self, value):
            """
            Set a new value for the parameter
            """
            if value in self.__enumLiterals:
                self.__value = value
                self.__valueNode.text = value
                self._set_model_modified(True)
            else:
                raise ValueNotPossibleError(message = 'Cannot set the value {}. Only the values {} are possible'.format(value, str(self.__enumLiterals)))

        def get_type(self):
            """
            Returns the type of parameter(if INTEGER, BOOLEAN, STRING, FUNCTION, FLOAT or ENUMERATION)
            """
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

        :param parent: The parent node under which the autosar node needs to be created.
        :param node: The xml node for which the autosar node needs to be created.
        """
        super().__init__(parent, node, 'contB', '/demo_other/contB')
        self.__isChoiceContainer = False
        # containers
        self.__subConts = []

        for subContainer in node.findall('{*}SUB-CONTAINERS/{*}ECUC-CONTAINER-VALUE'):
            definitionRef = subContainer.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'subCont':
                    self.__subConts.append(subCont(self, subContainer))

    def is_choice_container(self):
        return self.__isChoiceContainer


    def get_subConts(self):
        return self.__subConts

    def __add_subCont(self, value):
        """
        Adds a new subCont.
        :raise InvalidChildNodeException: If a container with same name already exists, 
                                          or if the maximum allowed instance is reached.
        """
        if value in self.__get_children():
            raise InvalidChildNodeException('Operation not possible. A container with name {} already present in {}.'.format(value.name, self))

        subContainers = AutosarNode._add_or_get_xml_node(self._node, 'SUB-CONTAINERS')
        self.__subConts.append(value)
        subContainers.append(value._node)

    def remove_subCont(self, value):
        if value is not None:
            subContainers = AutosarNode._add_or_get_xml_node(self._node, 'SUB-CONTAINERS')
            subContainers.remove(value._node)
            self.__subConts.remove(value)

    def removeAll_subCont(self):
        for cont in self.__subConts:
            self.remove_subCont(cont)


    def new_subCont(self, name, add_mandatory_elements=False):
        """
        :param: The name of the container
        :param add_mandatory_elements: Pass True if the the mandatory sub-containers/parameters/references 
                                       for should be created(please note that this depends on the attribute 
                                       "LOWER-MULTIPLICITY" of the respective containers/parameters/references 
                                       from the definition file. This option has no relevance if there are no 
                                       containers/parameters/references with "LOWER-MULTIPLICITY" greater than 0).
        Creates a new subCont with the given name.
        :raise InvalidChildNodeException: If a container with same name already exists, 
                                          or if the maximum allowed instance is reached.
        """
        xmlNode = AutosarNode._create_node('ECUC-CONTAINER-VALUE', short_name=name, dest='ECUC-PARAM-CONF-CONTAINER-DEF', definition_ref='/ModuleDef/demo_other/contB/subCont')
        value = subCont(self, xmlNode)
        self.__add_subCont(value)
        return value

    def __add_mandatory_elements_for_subCont(self, newCont, add_mandatory_elements):
        newCont.new_intParam()


    def __get_children(self):
        children = []
        children.extend(self.__subConts)
        return children



# Container configuration node for subCont
class subCont(AutosarNode):
    def __init__(self, parent, node):
        """
        Constructor for subCont node.

        :param parent: The parent node under which the autosar node needs to be created.
        :param node: The xml node for which the autosar node needs to be created.
        """
        super().__init__(parent, node, 'subCont', '/demo_other/contB/subCont')
        self.__isChoiceContainer = False
        # parameters
        self.__intParam_value = None

        for parameter in node.findall('{*}PARAMETER-VALUES/*'):
            definitionRef = parameter.find('{*}DEFINITION-REF').text
            if definitionRef is not None:
                definitionName = definitionRef.split('/').pop()
                if definitionName == 'intParam':
                    self.__intParam_value = self.intParam(self, parameter)
        # references
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



    def __get_children(self):
        children = []
        return children


    def get_intParam(self):
        return self.__intParam_value

    def new_intParam(self):
        """
        Creates a new intParam.
        :raise InvalidChildNodeException: If the parameter already exists.
        """
        if self.__intParam_value is not None:
            raise InvalidChildNodeException('Operation not possible. intParam already exists. Use get_intParam to access the parameter.')

        paremeters = AutosarNode._add_or_get_xml_node(self._node, 'PARAMETER-VALUES')
        xmlNode = AutosarNode._create_node('ECUC-NUMERICAL-PARAM-VALUE', dest='ECUC-INTEGER-PARAM-DEF', definition_ref='/ModuleDef/demo_other/contB/subCont/intParam')
        
        paremeters.append(xmlNode)
        value = AutosarNode._add_or_get_xml_node(self._node, 'VALUE')
        xmlNode.append(value)

        self.__intParam_value = self.intParam(self, xmlNode)
        self._set_model_modified(True)
        return self.__intParam_value


    def get_ref1(self):
        return self.__ref1_value

    def remove_ref1(self, value):
        if value is not None:
            references = AutosarNode._add_or_get_xml_node(self._node, 'REFERENCE-VALUES')
            references.remove(self.__ref1_value._node)
            self.__ref1_value = None
            self._set_model_modified(True)

    def new_ref1(self):
        """
        Creates a new ref1.
        :raise InvalidChildNodeException: If the reference already exists for 
                                          single reference value.
        """
        if self.__ref1_value is not None:
            raise InvalidChildNodeException('Operation not possible. ref1 already exists. Use get_ref1 to access the reference.')

        references = AutosarNode._add_or_get_xml_node(self._node, 'REFERENCE-VALUES')
        xmlNode = AutosarNode._create_node('ECUC-REFERENCE-VALUE', dest='ECUC-REFERENCE-DEF', definition_ref='/ModuleDef/demo_other/contB/subCont/ref1')
        references.append(xmlNode)
        self.__ref1_value = self.ref1(self, xmlNode)
        self._set_model_modified(True)
        return self.__ref1_value


    def get_foreignRef(self):
        return self.__foreignRef_value

    def remove_foreignRef(self, value):
        if value is not None:
            references = AutosarNode._add_or_get_xml_node(self._node, 'REFERENCE-VALUES')
            references.remove(self.__foreignRef_value._node)
            self.__foreignRef_value = None
            self._set_model_modified(True)

    def new_foreignRef(self):
        """
        Creates a new foreignRef.
        :raise InvalidChildNodeException: If the reference already exists for 
                                          single reference value.
        """
        if self.__foreignRef_value is not None:
            raise InvalidChildNodeException('Operation not possible. foreignRef already exists. Use get_foreignRef to access the reference.')

        references = AutosarNode._add_or_get_xml_node(self._node, 'REFERENCE-VALUES')
        xmlNode = AutosarNode._create_node('ECUC-REFERENCE-VALUE', dest='ECUC-FOREIGN-REFERENCE-DEF', definition_ref='/ModuleDef/demo_other/contB/subCont/foreignRef')
        references.append(xmlNode)
        self.__foreignRef_value = self.foreignRef(self, xmlNode)
        self._set_model_modified(True)
        return self.__foreignRef_value




    # Parameter configuration node for intParam
    class intParam(AutosarNode):
        def __init__(self, parent, node):
            """
            Constructor for intParam node.

            :param parent: The parent node under which the autosar node needs to be created.
            :param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'intParam', '/demo_other/contB/subCont/intParam')
            self.__value = None
            self.__valueNode = node.find('{*}VALUE')
            paramValue = self.__valueNode.text if self.__valueNode is not None else None
            self.__valueNode = AutosarNode._add_or_get_xml_node(node, 'VALUE') if self.__valueNode is None else self.__valueNode
            if paramValue is not None:
                self.__value = int(paramValue)

            self.__type = ParameterTypes.INTEGER
            self.__isDefaultValueSet = False
            self.__defaultValue = None
            self.__isMinValueSet = True
            self.__min = 0
            self.__isMaxValueSet = True
            self.__max = 65535


        def get_value(self):
            """
            Returns the parameter value
            """
            return self.__value
        
        def set_value(self, value):
            """
            Set a new value for the parameter
            """
            if value >= self.__min and value <= self.__max:
                self.__value = value
                self.__valueNode.text = str(value)
                self._set_model_modified(True)
            else:
                raise ValueNotPossibleError(message = 'Cannot set the value {}. Only the values between {} and {} are possible'.format(str(value), str(self.__min), str(self.__max)))

        def get_type(self):
            """
            Returns the type of parameter(if INTEGER, BOOLEAN, STRING, FUNCTION, FLOAT or ENUMERATION)
            """
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

            :param parent: The parent node under which the autosar node needs to be created.
            :param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'ref1', '/demo_other/contB/subCont/ref1')
            self.__valueNode = node.find('{*}VALUE-REF')
            self.__value = self.__valueNode.text if self.__valueNode is not None else None
            self.__valueNode = AutosarNode._add_or_get_xml_node(node, 'VALUE-REF', dest='ECUC-CONTAINER-VALUE') if self.__valueNode is None else self.__valueNode
            self.__type = ReferenceTypes.SIMPLE_REFERENCE
            self.__destinationRef = '/ModuleDef/demo_other/contA'


        def get_value(self):
            """
            Returns the value of the reference as string(path)
            """
            return self.__value

        def set_value(self, value):
            """
            Sets a new value as string(path) for the reference
            """
            self.__value = value
            self.__valueNode.text = value
            self._set_model_modified(True)

        def get_type(self):
            """
            Returns the type of reference(if SIMPLE_REFERENCE, CHOICE_REFERENCE or FOREIGN_REFERENCE)
            """
            return self.__type
    

        def get_destination_ref(self):
            """
            Returns the value of 'DESTINATION-REF' from the definition file
            """
            return self.__destinationRef



    # Reference configuration node for foreignRef
    class foreignRef(AutosarNode):
        def __init__(self, parent, node):
            """
            Constructor for foreignRef node.

            :param parent: The parent node under which the autosar node needs to be created.
            :param node: The xml node for which the autosar node needs to be created.
            """
            super().__init__(parent, node, 'foreignRef', '/demo_other/contB/subCont/foreignRef')
            self.__valueNode = node.find('{*}VALUE-REF')
            self.__value = self.__valueNode.text if self.__valueNode is not None else None
            self.__valueNode = AutosarNode._add_or_get_xml_node(node, 'VALUE-REF', dest='SW-COMPONENT-PROTOTYPE') if self.__valueNode is None else self.__valueNode
            self.__type = ReferenceTypes.FOREIGN_REFERENCE
            self.__destinationType = 'SW-COMPONENT-PROTOTYPE'

        def get_value(self):
            """
            Returns the value of the reference as string(path)
            """
            return self.__value

        def set_value(self, value):
            """
            Sets a new value as string(path) for the reference
            """
            self.__value = value
            self.__valueNode.text = value
            self._set_model_modified(True)

        def get_type(self):
            """
            Returns the type of reference(if SIMPLE_REFERENCE, CHOICE_REFERENCE or FOREIGN_REFERENCE)
            """
            return self.__type
    

        def get_destination_type(self):
            """
            Returns the value of DESTINATION-TYPE from the definition file for FOREIGN_REFERENCE
            """
            return self.__destinationType




# Exception classes
class ValueNotPossibleError(Exception):
    """Exception raised when the provided value is not possible to set for the parameter"""
    def __init__(self, message):
        super().__init__(message)


class ModuleAlreadyLoaded(Exception):
    """Exception raised when the module is already created/loaded"""
    def __init__(self, message):
        super().__init__(message)


class ModuleNotFoundError(Exception):
    """Exception raised if the module is not found in the input file"""
    def __init__(self, message):
        super().__init__(message)

class InvalidChildNodeException(Exception):
    """Exception raised when an invalid node is set."""
    def __init__(self, message):
        super().__init__(message)