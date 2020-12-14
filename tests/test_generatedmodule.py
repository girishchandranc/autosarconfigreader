import os, sys
import unittest
from resources.demo import demo
from resources.demo_other import demo_other

unittest.TestLoader.sortTestMethodsUsing = None
DESC_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'resources'), 'demo_desc.arxml')
SECOND_DESC_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'resources'), 'demo_desc_other.arxml')

class TestGeneratedModule(unittest.TestCase):
    def test_module_found(self):
        """
        Test that generated demo returns 
        the python object if the module
        'demo' is present inside the 
        configuration file
        """
        module = demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
        self.assertTrue(module is not None, "module is not None")
        self.assertEqual(module.get_short_name(), 'demo', "module name is demo")
    
    def test_module_not_found(self):
        """
        Test that generated demo returns 
        None if the module 'demo' is not 
        present inside the configuration file
        """
        module = demo.read_and_build_module_configuration(SECOND_DESC_FILE_LOCATION)
        self.assertTrue(module is None, "module is None")

    def test_container(self):
        """
        Test that generated demo returns the 
        containers present in the module configuration
        """
        module = demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
        contA = module.get_contA()
        self.assertEqual(contA.get_short_name(), 'ContA_conf', "container short name is ContA_conf")

        contB = module.get_contBs()
        self.assertEqual(len(contB), 2, "2 instance of contB is present")
        self.assertEqual(contB[0].get_short_name(), 'ContB_conf_0', "container short name is ContB_conf_0")
        self.assertEqual(contB[1].get_short_name(), 'ContB_conf_1', "container short name is ContB_conf_1")
        
        subConts = contB[0].get_subConts()
        self.assertEqual(len(subConts), 1, "only 1 instance of subCont is present")
        self.assertEqual(subConts[0].get_short_name(), 'subCont_conf', "container short name is subCont_conf")

    def test_parameter(self):
        """
        Test that generated demo returns the 
        parameters and its configured value 
        present in the module configuration
        """
        module = demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
        contA = module.get_contA()

        boolParam = contA.get_boolParam()
        self.assertEqual(boolParam.get_type(), demo.ParameterTypes.BOOLEAN, "type should be BOOLEAN")
        self.assertTrue(boolParam.get_value(), "Value of boolParam is True")
        self.assertEqual(boolParam.get_default_value(), False, "default value of boolParam is False")
        self.assertEqual(boolParam.get_short_name(), 'boolParam', "the parameter name is boolParam")

        enumParam = contA.get_enumParam()
        self.assertEqual(enumParam.get_value(), 'RED', "value of boolParam is RED")
        self.assertEqual(enumParam.get_type(), demo.ParameterTypes.ENUMERATION, "type should be ENUMERATION")
        self.assertEqual(enumParam.get_default_value(), 'GREEN', "default value of enumParam is GREEN")
        self.assertEqual(enumParam.get_short_name(), 'enumParam', "the parameter name is enumParam")
        self.assertEqual(enumParam.get_enum_literals(), ['RED', 'YELLOW', 'GREEN'], "literals of enumParam is ['RED', 'YELLOW', 'GREEN']")

        intParam = module.get_contBs()[0].get_subConts()[0].get_intParam()
        self.assertEqual(intParam.get_value(), 255, "value of intParam is 255")
        self.assertEqual(intParam.get_type(), demo.ParameterTypes.INTEGER, "type should be INTEGER")
        self.assertEqual(intParam.get_default_value(), None, "default value not present for intParam")
        self.assertEqual(intParam.get_short_name(), 'intParam', "the parameter name is intParam")
        self.assertEqual(intParam.get_min_value(), 0, "min value of intParam is 0")
        self.assertEqual(intParam.get_max_value(), 65535, "max value of intParam is 65535")

    def test_reference(self):
        """
        Test that generated demo returns the 
        references and its configured value 
        present in the module configuration
        """
        module = demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
        subCont = module.get_contBs()[0].get_subConts()[0]
        
        ref = subCont.get_ref1()
        self.assertEqual(ref.get_value(), '/ModuleConfig/demo_other/ContA_conf', "value of ref1 is /ModuleConfig/demo_other/ContA_conf")
        self.assertEqual(ref.get_type(), demo.ReferenceTypes.SIMPLE_REFERENCE, "type should be SIMPLE_REFERENCE")
        self.assertEqual(ref.get_destination_ref(), '/ModuleDef/demo_other/contA', "destinationref should be /ModuleDef/demo_other/contA")
        self.assertEqual(ref.get_short_name(), 'ref1', "the reference name is ref1")

        refs = subCont.get_ref2s()
        self.assertEqual(len(refs), 2, "2 values present for reference")
        
        ref = refs[0]
        self.assertEqual(ref.get_value(), '/ModuleConfig/demo/ContC_conf_0', "value of ref1 is /ModuleConfig/demo/ContC_conf_0")
        self.assertEqual(ref.get_type(), demo.ReferenceTypes.SIMPLE_REFERENCE, "type should be SIMPLE_REFERENCE")
        self.assertEqual(ref.get_destination_ref(), '/ModuleDef/demo/contC', "destinationref should be /ModuleDef/demo/contC")
        self.assertEqual(ref.get_short_name(), 'ref2', "the reference name is ref2")

        ref1 = refs[1]
        self.assertEqual(ref1.get_value(), '/ModuleConfig/demo/ContC_conf_1', "value of ref1 is /ModuleConfig/demo/ContC_conf_1")
        self.assertEqual(ref1.get_type(), demo.ReferenceTypes.SIMPLE_REFERENCE, "type should be SIMPLE_REFERENCE")
        self.assertEqual(ref1.get_destination_ref(), '/ModuleDef/demo/contC', "destinationref should be /ModuleDef/demo/contC")
        self.assertEqual(ref1.get_short_name(), 'ref2', "the reference name is ref2")

        foreignRef = subCont.get_foreignRef()
        self.assertEqual(foreignRef.get_value(), '/Autosar/Components/ComponentA', "value of foreignRef is /Autosar/Components/ComponentA")
        self.assertEqual(foreignRef.get_type(), demo.ReferenceTypes.FOREIGN_REFERENCE, "type should be FOREIGN_REFERENCE")
        self.assertEqual(foreignRef.get_destination_type(), 'SW-COMPONENT-PROTOTYPE', "destinationtype should be SW-COMPONENT-PROTOTYPE")
        self.assertEqual(foreignRef.get_short_name(), 'foreignRef', "the reference name is foreignRef")

    def test_get_path(self):
        """
        Test that the get_path method returns the 
        fully qualified path of module/container/
        parameter/reference node.
        """
        module = demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
        self.assertEqual(module.get_path(), '/ModuleConfig/demo', "path of demo is /ModuleConfig/demo")
        
        contA = module.get_contA()
        self.assertEqual(contA.get_path(), '/ModuleConfig/demo/ContA_conf', "path of contA is /ModuleConfig/demo/ContA_conf")
        self.assertEqual(contA.get_boolParam().get_path(), '/ModuleConfig/demo/ContA_conf/boolParam', "path of boolParam is /ModuleConfig/demo/ContA_conf/boolParam")
        
        contBs = module.get_contBs()
        self.assertEqual(contBs[0].get_path(), '/ModuleConfig/demo/ContB_conf_0', "path of contB is /ModuleConfig/demo/ContB_conf_0")
        self.assertEqual(contBs[1].get_path(), '/ModuleConfig/demo/ContB_conf_1', "path of contB is /ModuleConfig/demo/ContB_conf_1")
        self.assertEqual(contBs[0].get_subConts()[0].get_path(), '/ModuleConfig/demo/ContB_conf_0/subCont_conf', "path of subcont is /ModuleConfig/demo/ContB_conf_0/subCont_conf")

    def test_get_node(self):
        """
        Test that the get_node returns the object
        corresponding to the given path.
        """
        demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
        contB = demo.get_node('/ModuleConfig/demo/ContB_conf_0')
        self.assertTrue(contB is not None, "cannot be None")

        ref = demo.get_node('/ModuleConfig/demo/ContB_conf_1/subCont_conf/ref1')
        self.assertTrue(ref is not None, "cannot be None")

        randCont = demo.get_node('/ModuleConfig/demo/randCont')
        self.assertTrue(randCont is None, "should be None")
    
    def test_get_nodes_for_definition_path(self):
        """
        Test that the get_nodes_for_definition_path returns 
        the configuration nodes corresponding to the given path.
        """
        demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
        contA = demo.get_nodes_for_definition_path('/demo/contA')
        self.assertTrue(contA is not None, "cannot be None")
        self.assertEqual(len(contA), 1, "only 1 instance of contA is available")
        self.assertEqual(contA[0].get_short_name(), 'ContA_conf', "short name is ContA_conf")

        subCont = demo.get_nodes_for_definition_path('/demo/contB/subCont')
        self.assertTrue(subCont is not None, "cannot be None")
        self.assertEqual(len(subCont), 2, "2 instance of subCont expected(one from ContB_conf_0 and second from ContB_conf_1)")
        self.assertEqual(subCont[0].get_path(), '/ModuleConfig/demo/ContB_conf_0/subCont_conf', "path is /ModuleConfig/demo/ContB_conf_0/subCont_conf")
        self.assertEqual(subCont[1].get_path(), '/ModuleConfig/demo/ContB_conf_1/subCont_conf', "path is /ModuleConfig/demo/ContB_conf_1/subCont_conf")

        intParam = demo.get_nodes_for_definition_path('/demo/contB/subCont/intParam')
        self.assertTrue(intParam is not None, "cannot be None")
        self.assertEqual(len(intParam), 2, "2 instance of intParam expected(one from ContB_conf_0 and second from ContB_conf_1)")
        self.assertEqual(intParam[0].get_path(), '/ModuleConfig/demo/ContB_conf_0/subCont_conf/intParam', "path is /ModuleConfig/demo/ContB_conf_0/subCont_conf/intParam")
        self.assertEqual(intParam[0].get_value(), 255, "value should be 255")
        self.assertEqual(intParam[1].get_path(), '/ModuleConfig/demo/ContB_conf_1/subCont_conf/intParam', "path is /ModuleConfig/demo/ContB_conf_1/subCont_conf/intParam")
        self.assertEqual(intParam[1].get_value(), 1024, "value should be 1024")

        randCont = demo.get_nodes_for_definition_path('/demo/randCont')
        self.assertTrue(randCont is None, "should be None")

    def test_reference_value(self):
        """
        Test that the actual node could be obtained
        from the reference value.
        """
        module = demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
        demo_other.read_and_build_module_configuration(SECOND_DESC_FILE_LOCATION)
        subCont = module.get_contBs()[0].get_subConts()[0]
        
        ref = subCont.get_ref1()
        self.assertEqual(ref.get_value(), '/ModuleConfig/demo_other/ContA_conf', "value of ref1 is /ModuleConfig/demo_other/ContA_conf")
        actualRefNode = demo_other.get_node(ref.get_value())
        self.assertTrue(actualRefNode is not None, "the referenced node is not None")        
        self.assertEqual(actualRefNode.get_short_name(), 'ContA_conf', "the referenced container name is ContA_conf")

        ref2s = subCont.get_ref2s()
        self.assertEqual(len(ref2s), 2, "2 values present for reference ref2")
        
        ref2 = ref2s[0]
        self.assertEqual(ref2.get_value(), '/ModuleConfig/demo/ContC_conf_0', "value of ref2 is /ModuleConfig/demo/ContC_conf_0")
        actualRefNode = demo.get_node(ref2.get_value())
        self.assertTrue(actualRefNode is not None, "the referenced node is not None")        
        self.assertEqual(actualRefNode.get_short_name(), 'ContC_conf_0', "the referenced container name is ContC_conf_0")

        ref2 = ref2s[1]
        self.assertEqual(ref2.get_value(), '/ModuleConfig/demo/ContC_conf_1', "value of ref2 is /ModuleConfig/demo/ContC_conf_1")
        actualRefNode = demo.get_node(ref2.get_value())
        self.assertTrue(actualRefNode is None, "the referenced node is None")
    
    def test_get_parent(self):
        """
        Test that the get_parent returns the parent node
        of the container/prameter/reference.
        """
        module = demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
        contB = demo.get_node('/ModuleConfig/demo/ContB_conf_0')
        self.assertTrue(contB is not None, "cannot be None")
        self.assertTrue(contB.get_parent() is not None, "parent cannot be None")
        self.assertEqual(contB.get_parent().get_short_name(), 'demo' , "parents short name is demo")
        self.assertEqual(contB.get_parent(), module , "the nodes should be equal")

        ref = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/ref1')
        self.assertTrue(ref is not None, "cannot be None")
        self.assertTrue(ref.get_parent() is not None, "parent cannot be None")
        self.assertEqual(ref.get_parent().get_short_name(), 'subCont_conf' , "parents short name is subCont_conf")
        self.assertEqual(ref.get_parent().get_parent().get_parent(), module , "the nodes should be equal")
        self.assertEqual(ref.get_parent().get_parent(), module.get_contBs()[0] , "the nodes should be equal")

if __name__ == '__main__':
    unittest.main()