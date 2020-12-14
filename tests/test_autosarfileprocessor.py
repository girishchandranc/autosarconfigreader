import os, sys
mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mod_path)

import unittest
from asrGenerator.autosarfileprocessor import AutosarFileProcessor, FileReaderStatus, ParameterTypes, ReferenceTypes

unittest.TestLoader.sortTestMethodsUsing = None
DEF_FILE_LOCATION = os.path.join(os.path.join(os.path.dirname(__file__), 'resources'), 'demo_def.arxml')

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
        self.assertEqual(len(module.get_containers()), 3, "3 containers expected")

        contA = module.get_containers()[0]
        self.assertEqual(contA.get_name(), 'contA', "first container name should be contA")

        contB = module.get_containers()[1]
        self.assertEqual(contB.get_name(), 'contB', "second container name should be contB")
        self.assertTrue(contB.is_multi_instance_container(), "contB is a multi instance container")

        subCont = contB.get_sub_containers()[0]
        self.assertEqual(subCont.get_name(), 'subCont', "sub container name should be subCont")

        contC = module.get_containers()[2]
        self.assertEqual(contC.get_name(), 'contC', "third container name should be contC")
        self.assertTrue(contC.is_multi_instance_container(), "contC is a multi instance container")

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
        self.assertEqual(len(subCont.get_references()), 3, "3 references present in subCont")

        ref1 = subCont.get_references()[0]
        self.assertEqual(ref1.get_name(), 'ref1', "reference name should be ref1")
        self.assertEqual(ref1.get_destination(), '/ModuleDef/demo_other/contA', "destinationRef for ref1 is /ModuleDef/demo_other/contA")
        
        ref2 = subCont.get_references()[1]
        self.assertEqual(ref2.get_name(), 'ref2', "reference name should be ref2")
        self.assertTrue(ref2.is_multi_instance_reference(), "ref2 can have multiple values")
        self.assertEqual(ref2.get_destination(), '/ModuleDef/demo/contC', "destinationRef for ref1 is /ModuleDef/demo/contC")

        foreignRef = subCont.get_references()[2]
        self.assertEqual(foreignRef.get_name(), 'foreignRef', "reference name should be foreignRef")
        self.assertEqual(foreignRef.get_destination(), None, "destinationRef is not applicable for foreign reference")
        self.assertEqual(foreignRef.get_destination_type(), 'SW-COMPONENT-PROTOTYPE', "destinationType for foreignRef is SW-COMPONENT-PROTOTYPE")

    def test_get_path(self):
        """
        Test that AutosarFileProcessor builds the correct path
        for the autosar node
        """
        fileProcessor = AutosarFileProcessor(DEF_FILE_LOCATION, 'demo')
        module = fileProcessor.build_module()
        self.assertEqual(module.get_path(), '/demo', "path /demo expected")

        contA = module.get_containers()[0]
        self.assertEqual(contA.get_path(), '/demo/contA', "path /demo/contA expected")

        contB = module.get_containers()[1]
        self.assertEqual(contB.get_path(), '/demo/contB', "path /demo/contB expected")

        subCont = contB.get_sub_containers()[0]
        self.assertEqual(subCont.get_path(), '/demo/contB/subCont', "path /demo/contB/subCont")

        boolParam = contA.get_parameters()[0]
        self.assertEqual(boolParam.get_path(), '/demo/contA/boolParam', "path /demo/contA/boolParam expected")

if __name__ == '__main__':
    unittest.main()