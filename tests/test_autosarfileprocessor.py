import os, sys
mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mod_path)

import pytest
from asrGenerator.autosarfileprocessor import AutosarFileProcessor, FileReaderStatus, ParameterTypes, ReferenceTypes

DEF_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'resources'), 'demo_def.arxml')
DEF_FILE_DUPLICATE_CONTAINERS_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'resources'), 'demo_def_duplicate_containers.arxml')

def test_module_found():
    """
    Test that AutosarFileProcessor returns 
    the status MODULE_FOUND if module is 
    found in the given file
    """
    fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
    assert (fileProcessor.get_status() == FileReaderStatus.MODULE_FOUND), "status should be MODULE_FOUND"

def test_module_not_found():
    """
    Test that AutosarFileProcessor returns 
    the status MODULE_NOT_FOUND if module is 
    not found in the given file
    """
    fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo_other')
    assert (fileProcessor.get_status() == FileReaderStatus.MODULE_NOT_FOUND), "status should be MODULE_NOT_FOUND"

def test_module_node():
    """
    Test that AutosarFileProcessor returns 
    the right module node
    """
    fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
    module = fileProcessor.build_module()
    assert (module is not None), "module cannot be None"
    assert (module.get_name() == 'demo'), "module name should be demo"

    fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo_other')
    module = fileProcessor.build_module()
    assert (module is None), "module should be None"

def test_container_node():
    """
    Test that AutosarFileProcessor builds 
    the container node
    """
    fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
    module = fileProcessor.build_module()
    assert (len(module.get_containers()) == 3), "3 containers expected"

    contA = module.get_containers()[0]
    assert (contA.get_name() == 'contA'), "first container name should be contA"

    contB = module.get_containers()[1]
    assert (contB.get_name() == 'contB'), "second container name should be contB"
    assert (contB.is_multi_instance_container()), "contB is a multi instance container"

    subCont = contB.get_sub_containers()[0]
    assert(subCont.get_name() == 'subCont'), "sub container name should be subCont"

    contC = module.get_containers()[2]
    assert (contC.get_name() == 'contC'), "third container name should be contC"
    assert (contC.is_multi_instance_container()), "contC is a multi instance container"

def test_parameter_node():
    """
    Test that AutosarFileProcessor builds 
    the parameter node
    """
    fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
    module = fileProcessor.build_module()
    
    contA = module.get_containers()[0]        
    assert (len(contA.get_parameters()) == 2), "2 parameters present in contA"

    boolParam = contA.get_parameters()[0]
    assert (boolParam.get_name() == 'boolParam'), "first parameter name should be boolParam"
    assert (boolParam.is_default_value_set()), "default value is set for boolParam"
    assert (boolParam.get_default_value() == False), "default value for boolParam is False"

    enumParam = contA.get_parameters()[1]
    assert (enumParam.get_name() == 'enumParam'), "second parameter name should be enumParam"
    assert (enumParam.is_default_value_set()), "default value is set for enumParam"
    assert (enumParam.get_default_value() == '\'GREEN\''), "default value for enumParam is GREEN"
    assert (enumParam.get_enum_literals() == ['RED','YELLOW','GREEN']), "enum literals are [RED, YELLOW, GREEN]"

    contB = module.get_containers()[1]
    subCont = contB.get_sub_containers()[0]
    assert (len(subCont.get_parameters()) == 1), "only 1 parameter present in subCont"

    intParam = subCont.get_parameters()[0]
    assert (intParam.get_name() == 'intParam'), "parameter name should be intParam"
    assert (intParam.is_default_value_set() == False), "default value is not set for intParam"
    assert (intParam.get_default_value() is None), "default value not available for intParam"

    assert (intParam.is_min_value_set()), "min value is set for intParam"
    assert (intParam.get_min_value() == '0'), "min value for intParam is 0"
    assert (intParam.is_max_value_set()), "max value is set for intParam"
    assert (intParam.get_max_value() == '65535'), "max value for intParam is 65535"

def test_reference_node():
    """
    Test that AutosarFileProcessor builds 
    the parameter node
    """
    fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
    module = fileProcessor.build_module()
    contB = module.get_containers()[1]
    subCont = contB.get_sub_containers()[0]
    assert (len(subCont.get_references()) == 3), "3 references present in subCont"

    ref1 = subCont.get_references()[0]
    assert (ref1.get_name() == 'ref1'), "reference name should be ref1"
    assert (ref1.get_destination() == '/ModuleDef/demo_other/contA'), "destinationRef for ref1 is /ModuleDef/demo_other/contA"
    
    ref2 = subCont.get_references()[1]
    assert (ref2.get_name() == 'ref2'), "reference name should be ref2"
    assert (ref2.is_multi_instance_reference()), "ref2 can have multiple values"
    assert (ref2.get_destination() == '/ModuleDef/demo/contC'), "destinationRef for ref1 is /ModuleDef/demo/contC"

    foreignRef = subCont.get_references()[2]
    assert (foreignRef.get_name() == 'foreignRef'), "reference name should be foreignRef"
    assert (foreignRef.get_destination() is None), "destinationRef is not applicable for foreign reference"
    assert (foreignRef.get_destination_type() == 'SW-COMPONENT-PROTOTYPE'), "destinationType for foreignRef is SW-COMPONENT-PROTOTYPE"

def test_get_path():
    """
    Test that AutosarFileProcessor builds the correct path
    for the autosar node
    """
    fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
    module = fileProcessor.build_module()
    assert (module.get_path() == '/demo'), "path /demo expected"

    contA = module.get_containers()[0]
    assert (contA.get_path() == '/demo/contA'), "path /demo/contA expected"

    contB = module.get_containers()[1]
    assert (contB.get_path() == '/demo/contB'), "path /demo/contB expected"

    subCont = contB.get_sub_containers()[0]
    assert (subCont.get_path() == '/demo/contB/subCont'), "path /demo/contB/subCont"

    boolParam = contA.get_parameters()[0]
    assert (boolParam.get_path() == '/demo/contA/boolParam'), "path /demo/contA/boolParam expected"

def test_duplicate_container_names():
    """
    Test that AutosarFileProcessor creates unique classes
    if there exists multiple containers with same name
    """
    fileProcessor = AutosarFileProcessor(DEF_FILE_DUPLICATE_CONTAINERS_LOCATION, 'demo')
    module = fileProcessor.build_module()
    
    contA = module.get_containers()[0]
    contB = module.get_containers()[1]
    contC = module.get_containers()[2]
    subContA = contA.get_sub_containers()[0]
    subContB = contB.get_sub_containers()[0]
    subContC = contC.get_sub_containers()[0]

    assert (subContA.get_name() == 'subCont'), "subcontainer name should be subCont"
    assert (subContB.get_name() == 'subCont'), "subcontainer name should be subCont"
    assert (subContC.get_name() == 'subCont'), "subcontainer name should be subCont"
    assert (subContA.get_path() == '/demo/contA/subCont'), "path /demo/contA/subCont"
    assert (subContB.get_path() == '/demo/contB/subCont'), "path /demo/contB/subCont"
    assert (subContC.get_path() == '/demo/contC/subCont'), "path /demo/contC/subCont"
    assert (subContA.get_class_name() == 'subCont'), "class name should be subCont"
    assert (subContB.get_class_name() == 'subCont1'), "class name should be subCont1"
    assert (subContC.get_class_name() == 'subCont2'), "class name should be subCont2"
