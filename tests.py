import unittest, os
from asrGenerator.autosarfileprocessor import AutosarFileProcessor, FileReaderStatus, ParameterTypes, ReferenceTypes
from test_resources.demo import demo
from test_resources.demo_other import demo_other

unittest.TestLoader.sortTestMethodsUsing = None
DEF_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'test_resources'), 'demo_def.arxml')
DESC_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'test_resources'), 'demo_desc.arxml')
SECOND_DEF_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'test_resources'), 'demo_def_other.arxml')
SECOND_DESC_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'test_resources'), 'demo_desc_other.arxml')

class TestAutosarFileProcessor(unittest.TestCase):

    def test_module_found(self):
        """
        Test that AutosarFileProcessor returns 
        the status MODULE_FOUND if module is 
        found in the given file
        """
        fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
        self.assertEqual(fileProcessor.get_status(), FileReaderStatus.MODULE_FOUND, "status should be MODULE_FOUND")

    def test_module_not_found(self):
        """
        Test that AutosarFileProcessor returns 
        the status MODULE_NOT_FOUND if module is 
        not found in the given file
        """
        fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo_other')
        self.assertEqual(fileProcessor.get_status(), FileReaderStatus.MODULE_NOT_FOUND, "status should be MODULE_NOT_FOUND")
    
    def test_module_node(self):
        """
        Test that AutosarFileProcessor returns 
        the right module node
        """
        fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
        module = fileProcessor.build_module()
        self.assertTrue(module is not None, "module cannot be None")
        self.assertEqual(module.get_name(), 'demo', "module name should be demo")

        fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo_other')
        module = fileProcessor.build_module()
        self.assertTrue(module is None, "module should be None")
    
    def test_container_node(self):
        """
        Test that AutosarFileProcessor builds 
        the container node
        """
        fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
        module = fileProcessor.build_module()
        self.assertEqual(len(module.get_containers()), 2, "2 containers expected")

        contA = module.get_containers()[0]
        self.assertEqual(contA.get_name(), 'contA', "first container name should be contA")

        contB = module.get_containers()[1]
        self.assertEqual(contB.get_name(), 'contB', "second container name should be contB")
        self.assertTrue(contB.is_multi_instance_container(), "contB is a multi instance container")

        subCont = contB.get_sub_containers()[0]
        self.assertEqual(subCont.get_name(), 'subCont', "sub container name should be subCont")

    def test_parameter_node(self):
        """
        Test that AutosarFileProcessor builds 
        the parameter node
        """
        fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
        module = fileProcessor.build_module()
        
        contA = module.get_containers()[0]        
        self.assertEqual(len(contA.get_parameters()), 2, "2 parameters present in contA")

        boolParam = contA.get_parameters()[0]
        self.assertEqual(boolParam.get_name(), 'boolParam', "first parameter name should be boolParam")
        self.assertTrue(boolParam.is_default_value_set(), "default value is set for boolParam")
        self.assertEqual(boolParam.get_default_value(), False, "default value for boolParam is False")

        enumParam = contA.get_parameters()[1]
        self.assertEqual(enumParam.get_name(), 'enumParam', "second parameter name should be enumParam")
        self.assertTrue(enumParam.is_default_value_set(), "default value is set for enumParam")
        self.assertEqual(enumParam.get_default_value(), '\'GREEN\'', "default value for enumParam is GREEN")
        self.assertEqual(enumParam.get_enum_literals(), ['RED','YELLOW','GREEN'], "enum literals are [RED, YELLOW, GREEN]")

        contB = module.get_containers()[1]
        subCont = contB.get_sub_containers()[0]
        self.assertEqual(len(subCont.get_parameters()), 1, "only 1 parameter present in subCont")

        intParam = subCont.get_parameters()[0]
        self.assertEqual(intParam.get_name(), 'intParam', "parameter name should be intParam")
        self.assertFalse(intParam.is_default_value_set(), "default value is not set for intParam")
        self.assertTrue(intParam.get_default_value() is None, "default value not available for intParam")

        self.assertTrue(intParam.is_min_value_set(), "min value is set for intParam")
        self.assertEqual(intParam.get_min_value(), '0', "min value for intParam is 0")
        self.assertTrue(intParam.is_max_value_set(), "max value is set for intParam")
        self.assertEqual(intParam.get_max_value(), '65535', "max value for intParam is 65535")
    
    def test_reference_node(self):
        """
        Test that AutosarFileProcessor builds 
        the parameter node
        """
        fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
        module = fileProcessor.build_module()
        contB = module.get_containers()[1]
        subCont = contB.get_sub_containers()[0]
        self.assertEqual(len(subCont.get_references()), 2, "2 references present in subCont")

        ref1 = subCont.get_references()[0]
        self.assertEqual(ref1.get_name(), 'ref1', "reference name should be ref1")
        self.assertEqual(ref1.get_destination(), '/ModuleDef/demo_other/contA', "destinationRef for ref1 is /ModuleDef/demo/contA")

        foreignRef = subCont.get_references()[1]
        self.assertEqual(foreignRef.get_name(), 'foreignRef', "reference name should be foreignRef")
        self.assertEqual(foreignRef.get_destination(), None, "destinationRef is not applicable for foreign reference")
        self.assertEqual(foreignRef.get_destination_type(), 'SW-COMPONENT-PROTOTYPE', "destinationType for foreignRef is SW-COMPONENT-PROTOTYPE")


class TestGenerateModule(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()