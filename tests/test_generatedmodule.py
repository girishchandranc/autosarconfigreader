import os, sys
import pytest, filecmp

mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mod_path)

from tests.resources.demo import demo
from tests.resources.demo_other import demo_other

DESC_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'resources'), 'demo_desc.arxml')
SECOND_DESC_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'resources'), 'demo_desc_other.arxml')
TEST_OUT_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'resources'), 'test_out.arxml')

def teardown():
    try:
        os.remove(TEST_OUT_LOCATION)
    except:
        pass
    demo.reinit()

def test_module_found():
    """
    Test that generated demo returns 
    the python object if the module
    'demo' is present inside the 
    configuration file
    """
    module = demo.read(DESC_FILE_LOCATION)
    assert (module is not None), "module is not None"
    assert (module.name == 'demo'), "module name is demo"
    teardown()

def test_module_not_found():
    """
    Test that generated demo returns 
    None if the module 'demo' is not 
    present inside the configuration file
    """
    with pytest.raises(demo.ModuleNotFoundError) as cm:
        module = demo.read(SECOND_DESC_FILE_LOCATION)
        assert ('The module demo not found in the input file {}.'.format(SECOND_DESC_FILE_LOCATION) == str(cm.exception))
        assert (module is None), "module is None"

    teardown()

def test_container():
    """
    Test that generated demo returns the 
    containers present in the module configuration
    """
    module = demo.read(DESC_FILE_LOCATION)
    contA = module.get_contA()
    assert (contA.name == 'ContA_conf'), "container short name is ContA_conf"

    contB = module.get_contBs()
    assert (len(contB) == 2), "2 instance of contB is present"
    assert (contB[0].name == 'ContB_conf_0'), "container short name is ContB_conf_0"
    assert (contB[1].name == 'ContB_conf_1'), "container short name is ContB_conf_1"
    
    subConts = contB[0].get_subConts()
    assert (len(subConts) == 1), "only 1 instance of subCont is present"
    assert (subConts[0].name == 'subCont_conf'), "container short name is subCont_conf"
    teardown()

def test_parameter():
    """
    Test that generated demo returns the 
    parameters and its configured value 
    present in the module configuration
    """
    module = demo.read(DESC_FILE_LOCATION)
    contA = module.get_contA()

    boolParam = contA.get_boolParam()
    assert (boolParam.get_type() == demo.ParameterTypes.BOOLEAN), "type should be BOOLEAN"
    assert (boolParam.get_value()), "Value of boolParam is True"
    assert (boolParam.get_default_value() is False), "default value of boolParam is False"
    assert (boolParam.name == 'boolParam'), "the parameter name is boolParam"

    enumParam = contA.get_enumParam()
    assert (enumParam.get_value() == 'RED'), "value of boolParam is RED"
    assert (enumParam.get_type() == demo.ParameterTypes.ENUMERATION), "type should be ENUMERATION"
    assert (enumParam.get_default_value() == 'GREEN'), "default value of enumParam is GREEN"
    assert (enumParam.name == 'enumParam'), "the parameter name is enumParam"
    assert (enumParam.get_enum_literals() == ['RED', 'YELLOW', 'GREEN']), "literals of enumParam is ['RED', 'YELLOW', 'GREEN']"

    intParam = module.get_contBs()[0].get_subConts()[0].get_intParam()
    assert (intParam.get_value() == 255), "value of intParam is 255"
    assert (intParam.get_type() == demo.ParameterTypes.INTEGER), "type should be INTEGER"
    assert (intParam.name == 'intParam'), "the parameter name is intParam"
    assert (intParam.get_min_value() == 0), "min value of intParam is 0"
    assert (intParam.get_max_value() == 65535), "max value of intParam is 65535"
    teardown()

def test_reference():
    """
    Test that generated demo returns the 
    references and its configured value 
    present in the module configuration
    """
    module = demo.read(DESC_FILE_LOCATION)
    subCont = module.get_contBs()[0].get_subConts()[0]
    
    ref = subCont.get_ref1()
    assert (ref.get_value() == '/ModuleConfig/demo_other/ContA_conf'), "value of ref1 is /ModuleConfig/demo_other/ContA_conf"
    assert (ref.get_type() == demo.ReferenceTypes.SIMPLE_REFERENCE), "type should be SIMPLE_REFERENCE"
    assert (ref.get_destination_ref() == '/ModuleDef/demo_other/contA'), "destinationref should be /ModuleDef/demo_other/contA"
    assert (ref.name == 'ref1'), "the reference name is ref1"

    refs = subCont.get_ref2s()
    assert (len(refs) == 2), "2 values present for reference"
    
    ref = refs[0]
    assert (ref.get_value() == '/ModuleConfig/demo/ContC_conf_0'), "value of ref1 is /ModuleConfig/demo/ContC_conf_0"
    assert (ref.get_type() == demo.ReferenceTypes.SIMPLE_REFERENCE), "type should be SIMPLE_REFERENCE"
    assert (ref.get_destination_ref() == '/ModuleDef/demo/contC'), "destinationref should be /ModuleDef/demo/contC"
    assert (ref.name == 'ref2'), "the reference name is ref2"

    ref1 = refs[1]
    assert (ref1.get_value() == '/ModuleConfig/demo/ContC_conf_1'), "value of ref1 is /ModuleConfig/demo/ContC_conf_1"
    assert (ref1.get_type() == demo.ReferenceTypes.SIMPLE_REFERENCE), "type should be SIMPLE_REFERENCE"
    assert (ref1.get_destination_ref() == '/ModuleDef/demo/contC'), "destinationref should be /ModuleDef/demo/contC"
    assert (ref1.name == 'ref2'), "the reference name is ref2"

    foreignRef = subCont.get_foreignRef()
    assert (foreignRef.get_value() == '/Autosar/Components/ComponentA'), "value of foreignRef is /Autosar/Components/ComponentA"
    assert (foreignRef.get_type() == demo.ReferenceTypes.FOREIGN_REFERENCE), "type should be FOREIGN_REFERENCE"
    assert (foreignRef.get_destination_type() == 'SW-COMPONENT-PROTOTYPE'), "destinationtype should be SW-COMPONENT-PROTOTYPE"
    assert (foreignRef.name == 'foreignRef'), "the reference name is foreignRef"
    teardown()

def test_get_path():
    """
    Test that the get_path method returns the 
    fully qualified path of module/container/
    parameter/reference node.
    """
    module = demo.read(DESC_FILE_LOCATION)
    assert (module.path == '/ModuleConfig/demo'), "path of demo is /ModuleConfig/demo"
    
    contA = module.get_contA()
    assert (contA.path == '/ModuleConfig/demo/ContA_conf'), "path of contA is /ModuleConfig/demo/ContA_conf"
    assert (contA.get_boolParam().path == '/ModuleConfig/demo/ContA_conf/boolParam'), "path of boolParam is /ModuleConfig/demo/ContA_conf/boolParam"
    
    contBs = module.get_contBs()
    assert (contBs[0].path == '/ModuleConfig/demo/ContB_conf_0'), "path of contB is /ModuleConfig/demo/ContB_conf_0"
    assert (contBs[1].path == '/ModuleConfig/demo/ContB_conf_1'), "path of contB is /ModuleConfig/demo/ContB_conf_1"
    assert (contBs[0].get_subConts()[0].path == '/ModuleConfig/demo/ContB_conf_0/subCont_conf'), "path of subcont is /ModuleConfig/demo/ContB_conf_0/subCont_conf"
    teardown()

def test_get_node():
    """
    Test that the get_node returns the object
    corresponding to the given path.
    """
    demo.read(DESC_FILE_LOCATION)
    contB = demo.get_node('/ModuleConfig/demo/ContB_conf_0')
    assert (contB is not None), "cannot be None"

    ref = demo.get_node('/ModuleConfig/demo/ContB_conf_1/subCont_conf/ref1')
    assert (ref is not None), "cannot be None"

    randCont = demo.get_node('/ModuleConfig/demo/randCont')
    assert (randCont is None), "should be None"
    teardown()

def test_get_nodes_for_definition_path():
    """
    Test that the get_nodes_for_definition_path returns 
    the configuration nodes corresponding to the given path.
    """
    demo.read(DESC_FILE_LOCATION)
    contA = demo.get_nodes_for_definition_path('/demo/contA')
    assert (contA is not None), "cannot be None"
    assert (len(contA) == 1), "only 1 instance of contA is available"
    assert (contA[0].name == 'ContA_conf'), "short name is ContA_conf"

    subCont = demo.get_nodes_for_definition_path('/demo/contB/subCont')
    assert (subCont is not None), "cannot be None"
    assert (len(subCont) == 2), "2 instance of subCont expected(one from ContB_conf_0 and second from ContB_conf_1)"
    assert (subCont[0].path == '/ModuleConfig/demo/ContB_conf_0/subCont_conf'), "path is /ModuleConfig/demo/ContB_conf_0/subCont_conf"
    assert (subCont[1].path == '/ModuleConfig/demo/ContB_conf_1/subCont_conf'), "path is /ModuleConfig/demo/ContB_conf_1/subCont_conf"

    intParam = demo.get_nodes_for_definition_path('/demo/contB/subCont/intParam')
    assert (intParam is not None), "cannot be None"
    assert (len(intParam) == 2), "2 instance of intParam expected(one from ContB_conf_0 and second from ContB_conf_1)"
    assert (intParam[0].path == '/ModuleConfig/demo/ContB_conf_0/subCont_conf/intParam'), "path is /ModuleConfig/demo/ContB_conf_0/subCont_conf/intParam"
    assert (intParam[0].get_value() == 255), "value should be 255"
    assert (intParam[1].path == '/ModuleConfig/demo/ContB_conf_1/subCont_conf/intParam'), "path is /ModuleConfig/demo/ContB_conf_1/subCont_conf/intParam"
    assert (intParam[1].get_value() == 1024), "value should be 1024"

    randCont = demo.get_nodes_for_definition_path('/demo/randCont')
    assert (randCont is None), "should be None"
    teardown()

def test_reference_value():
    """
    Test that the actual node could be obtained
    from the reference value.
    """
    module = demo.read(DESC_FILE_LOCATION)
    demo_other.read(SECOND_DESC_FILE_LOCATION)
    subCont = module.get_contBs()[0].get_subConts()[0]
    
    ref = subCont.get_ref1()
    assert (ref.get_value() == '/ModuleConfig/demo_other/ContA_conf'), "value of ref1 is /ModuleConfig/demo_other/ContA_conf"
    actualRefNode = demo_other.get_node(ref.get_value())
    assert (actualRefNode is not None), "the referenced node is not None"
    assert (actualRefNode.name == 'ContA_conf'), "the referenced container name is ContA_conf"
    assert (actualRefNode.path == ref.get_value()), "the paths should be equal"

    ref2s = subCont.get_ref2s()
    assert (len(ref2s) == 2), "2 values present for reference ref2"
    
    ref2 = ref2s[0]
    assert (ref2.get_value() == '/ModuleConfig/demo/ContC_conf_0'), "value of ref2 is /ModuleConfig/demo/ContC_conf_0"
    actualRefNode = demo.get_node(ref2.get_value())
    assert (actualRefNode is not None), "the referenced node is not None"
    assert (actualRefNode.name == 'ContC_conf_0'), "the referenced container name is ContC_conf_0"

    ref2 = ref2s[1]
    assert (ref2.get_value() == '/ModuleConfig/demo/ContC_conf_1'), "value of ref2 is /ModuleConfig/demo/ContC_conf_1"
    actualRefNode = demo.get_node(ref2.get_value())
    assert (actualRefNode is None), "the referenced node is None"
    teardown()

def test_get_parent():
    """
    Test that the get_parent returns the parent node
    of the container/prameter/reference.
    """
    module = demo.read(DESC_FILE_LOCATION)
    contB = demo.get_node('/ModuleConfig/demo/ContB_conf_0')
    assert (contB is not None), "cannot be None"
    assert (contB.get_parent() is not None), "parent cannot be None"
    assert (contB.get_parent().name == 'demo') , "parents short name is demo"
    assert (contB.get_parent() == module) , "the nodes should be equal"

    ref = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/ref1')
    assert (ref is not None), "cannot be None"
    assert (ref.get_parent() is not None), "parent cannot be None"
    assert (ref.get_parent().name == 'subCont_conf'), "parents short name is subCont_conf"
    assert (ref.get_parent().get_parent().get_parent() == module), "the nodes should be equal"
    assert (ref.get_parent().get_parent() == module.get_contBs()[0]), "the nodes should be equal"
    teardown()

def test_set_value():
    """
    Test that the values are set properly for the parameters
    and references.
    """
    demo.read(DESC_FILE_LOCATION)
    enumParam = demo.get_node('/ModuleConfig/demo/ContA_conf/enumParam')
    assert (enumParam is not None), "cannot be None"
    enumParam.set_value('YELLOW')
    assert (enumParam.get_value() == 'YELLOW'), "value should be YELLOW"

    intParam = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/intParam')
    assert (intParam is not None), "cannot be None"
    intParam.set_value(1234)
    assert (intParam.get_value() == 1234), "value should be 1234"

    ref1 = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/ref1')
    assert (ref1 is not None), "cannot be None"
    ref1.set_value('/ModuleConfig/demo_other/ContA_conf_1234')
    assert (ref1.get_value() == '/ModuleConfig/demo_other/ContA_conf_1234') , "value should be /ModuleConfig/demo_other/ContA_conf_1234"

    with pytest.raises(demo.ValueNotPossibleError) as cm:
        intParam.set_value(65537)
        assert ('Cannot set the value 65537. Only the values between 0 and 65535 are possible' == str(cm.exception))
    
    with pytest.raises(demo.ValueNotPossibleError) as cm:
        enumParam.set_value('BLUE')
        assert ('Cannot set the value BLUE. Only the values [RED, YELLOW, GREEN] are possible' == str(cm.exception))
    teardown()

def test_model_modified():
    """
    Test that the model is modified when a parameter/reference value is changed.
    """
    module = demo.read(DESC_FILE_LOCATION)
    assert (module.is_model_modified() is False), "model is not modified"

    enumParam = demo.get_node('/ModuleConfig/demo/ContA_conf/enumParam')
    assert (enumParam is not None), "cannot be None"
    enumParam.set_value('YELLOW')
    assert (module.is_model_modified()), "model is modified"

    module = demo.read(DESC_FILE_LOCATION, ignore_previous_loaded_node=True)
    assert (module.is_model_modified() is False), "model is not modified"
    intParam = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/intParam')
    intParam.set_value(1234)
    assert (module.is_model_modified()), "model is modified"

    module = demo.read(DESC_FILE_LOCATION, ignore_previous_loaded_node=True)
    assert (module.is_model_modified() is False), "model is not modified"
    ref1 = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/ref1')
    assert (ref1 is not None), "cannot be None"
    ref1.set_value('/ModuleConfig/demo_other/ContA_conf_1234')
    assert (module.is_model_modified()), "model is modified"

    module = demo.read(DESC_FILE_LOCATION, ignore_previous_loaded_node=True)
    assert (module.is_model_modified() is False), "model is not modified"
    with pytest.raises(demo.ValueNotPossibleError) as cm:
        intParam.set_value(65537)
        assert ('Cannot set the value 65537. Only the values between 0 and 65535 are possible' == str(cm.exception))
        assert (module.is_model_modified() is False), "model is not modified"
    
    module = demo.read(DESC_FILE_LOCATION, ignore_previous_loaded_node=True)
    assert (module.is_model_modified() is False), "model is not modified"
    with pytest.raises(demo.ValueNotPossibleError) as cm:
        enumParam.set_value('BLUE')
        assert ('Cannot set the value BLUE. Only the values [RED, YELLOW, GREEN] are possible' == str(cm.exception))
        assert (module.is_model_modified() is False), "model is not modified"
    
    teardown()

def test_save():
    """
    Test that the model is saved to the location when requested by user.
    """
    module = demo.read(DESC_FILE_LOCATION)
    enumParam = demo.get_node('/ModuleConfig/demo/ContA_conf/enumParam')
    enumParam.set_value('YELLOW')
    intParam = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/intParam')
    intParam.set_value(1234)
    ref1 = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/ref1')
    ref1.set_value('/ModuleConfig/demo_other/ContA_conf_1234')
    
    module.save(TEST_OUT_LOCATION)
    assert (filecmp.cmp (DESC_FILE_LOCATION, TEST_OUT_LOCATION) is False), "file should be different"

    ##Read the saved file and check if the values are set properly        
    demo.read(TEST_OUT_LOCATION, ignore_previous_loaded_node=True)
    enumParam = demo.get_node('/ModuleConfig/demo/ContA_conf/enumParam')
    assert (enumParam.get_value() == 'YELLOW'), "value should be YELLOW"
    intParam = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/intParam')
    assert (intParam.get_value() == 1234), "value should be 1234"
    ref1 = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/ref1')
    assert (ref1.get_value() == '/ModuleConfig/demo_other/ContA_conf_1234'), "value should be /ModuleConfig/demo_other/ContA_conf_1234"
    teardown()

def test_new_file():
    """
    Test that the its possible to create new file for the module.
    """
    module = demo.new(TEST_OUT_LOCATION)
    assert (module is not None), 'module should not be None'
    assert (os.path.isfile(TEST_OUT_LOCATION)), 'file should be created'
    teardown()

def test_new_container_parameter_reference():
    """
    Tests that its possible to add new container
    """
    module = demo.new(TEST_OUT_LOCATION)
    assert (module is not None), 'module should not be None'
    cont = module.new_contB('newContB').new_subCont('subcont_0')
    assert (cont is not None), 'cont should not be None'
    param = cont.new_intParam()
    assert (param is not None), 'param should not be None'
    param.set_value(200)
    assert (param.get_value() == 200), 'param value should be 200'
    ref = cont.new_ref1()
    assert (ref is not None), 'ref should not be None'
    ref.set_value('/demo_other/demo_other/ContA_conf')
    assert (ref.get_value() == '/demo_other/demo_other/ContA_conf'), 'ref value should be /demo_other/demo_other/ContA_conf'
    foreignRef = cont.new_foreignRef()
    assert (foreignRef is not None), 'foreignRef should not be None'
    foreignRef.set_value('/swcs/CompA')
    assert (foreignRef.get_value() == '/swcs/CompA'), 'foreignRef value should be /swcs/CompA'
    module.save()

    newModule = demo.read(TEST_OUT_LOCATION,ignore_previous_loaded_node=True)
    contb = next(iter(newModule.get_contBs()))
    assert (contb is not None), 'contb should not be None'
    subCont = next(iter(contb.get_subConts()))
    assert (subCont is not None), 'subCont should not be None'
    intparam = subCont.get_intParam()
    assert (intparam is not None), 'intparam should not be None'
    assert (intparam.get_value() == 200), 'intparam value should be 200'
    ref1 = subCont.get_ref1()
    assert (ref1 is not None), 'intparam should not be None'
    assert (ref1.get_value() == '/demo_other/demo_other/ContA_conf'), 'ref1 value should be /demo_other/demo_other/ContA_conf'
    foreignRef1 = subCont.get_foreignRef()
    assert (foreignRef1 is not None), 'intparam should not be None'
    assert (foreignRef1.get_value() == '/swcs/CompA'), 'foreignRef1 value should be /swcs/CompA'
    teardown()

def test_new_module_create_mandatory_elements():
    """
    Tests that the new module creates all mandatory elements.
    """
    module = demo.new(TEST_OUT_LOCATION,add_mandatory_containers=True)
    assert (module.get_contA() is not None), 'cannot be None'
    assert (module.get_contA().get_boolParam() is not None), 'cannot be None'
    assert (module.get_contA().get_boolParam().get_value() is False), 'value is False(default value)'
    assert (module.get_contA().get_enumParam() is not None), 'cannot be None'
    assert (module.get_contA().get_enumParam().get_value() == 'GREEN'), 'value is GREEN'
    assert (len(module.get_contCs()) > 0), 'contc should be created'

    cont = module.new_contB('contb',add_mandatory_elements=True)
    assert (cont is not None), 'cannot be None'
    assert (len(cont.get_subConts()) > 0), 'subcont should be created'
    subcont = next(iter(cont.get_subConts()))
    assert (subcont is not None), 'cannot be None'
    assert (subcont.get_intParam() is not None), 'cannot be None'
    assert (subcont.get_intParam().get_value() is None), 'value is not available'
    assert (len(subcont.get_ref2s()) > 0), 'ref2 should be created'
    assert (next(iter(subcont.get_ref2s())).get_value() is None), 'value is not available'
    module.save()
    teardown()
