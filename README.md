[![Build Actions Status](https://github.com/girishchandranc/autosarconfigreader/workflows/app-testing/badge.svg)](https://github.com/girishchandranc/autosarconfigreader/actions)
# Autosar Config Reader

The asrGenerator package provides the option to read Autosar compliant ecu configuration files by:
- Generating python classes based on the autosar module definition file
    - Generate a python package and classes corresponding to the module/containers/parameters/references with exactly the same name as in the definition file.
    - Using the generated classes, users could simply access the complete configuration through a list of getter methods.
    - The package will be handy in writing code generators for the autosar modules where users would be benefitted from accessing the containers/parameter values as python classes instead of reading the autosar module configuration file

## Usage instructions
To generate the code for module, first install the package AutosarConfigReader and then call the module `asrGenerator` by providing the relevant arguments.
```python
pip install -i https://test.pypi.org/simple/ AutosarConfigReader
python3 -m asrGenerator -i <input_file> -m <module_name> -o <output_folder>
```
- <input_file>: Provide the path to the autosar definition file.
- <module_name>: Provide the module name for which the code needs to be generated.For eg: Rte
- <output_folder>: Provide the location where the code needs to be generated.

## Using the generated python classes
The generated package can be used for reading the autosar module configuration.
- Simply include the package inside one of your scripts and call the function read_and_build_module_configuration(file) with the input configuration file. 

> Example: Lets say we generated python package for Rte and now we want to read the Rte module configuration of the file passed as a commandline argument. The equivalent python code will look like:

```python
from Rte import Rte
import sys

rteNode = Rte.read_and_build_module_configuration(sys.argv[1])
if rteNode is not None:
    print('read sucessfull')
else:
    print('read failed')
```

- Additionaly there also exists a helper function `get_node(path)` which returns the python object for the given autosar path.

Lets consider a simple autosar definition file for an imgainary module named 'demo'. 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://autosar.org/schema/r4.0 AUTOSAR_00049.xsd">
  <AR-PACKAGES>
    <AR-PACKAGE UUID="ECUC:ModuleDef">
      <SHORT-NAME>ModuleDef</SHORT-NAME>
      <ELEMENTS>
        <ECUC-MODULE-DEF>
            <SHORT-NAME>demo</SHORT-NAME>
            <DESC>
                <L-2 L="EN">Configuration of the demo module.</L-2>
            </DESC>
            <LOWER-MULTIPLICITY>0</LOWER-MULTIPLICITY>
            <UPPER-MULTIPLICITY>1</UPPER-MULTIPLICITY>
            <POST-BUILD-VARIANT-SUPPORT>true</POST-BUILD-VARIANT-SUPPORT>
            <SUPPORTED-CONFIG-VARIANTS>
                <SUPPORTED-CONFIG-VARIANT>VARIANT-POST-BUILD</SUPPORTED-CONFIG-VARIANT>
                <SUPPORTED-CONFIG-VARIANT>VARIANT-PRE-COMPILE</SUPPORTED-CONFIG-VARIANT>
            </SUPPORTED-CONFIG-VARIANTS>
            <CONTAINERS>
                <ECUC-PARAM-CONF-CONTAINER-DEF>
                    <SHORT-NAME>contA</SHORT-NAME>
                    <LOWER-MULTIPLICITY>1</LOWER-MULTIPLICITY>
                    <UPPER-MULTIPLICITY>1</UPPER-MULTIPLICITY>
                    <PARAMETERS>
                        <ECUC-BOOLEAN-PARAM-DEF>
                            <SHORT-NAME>boolParam</SHORT-NAME>
                            <DEFAULT-VALUE>false</DEFAULT-VALUE>
                        </ECUC-BOOLEAN-PARAM-DEF>
                        <ECUC-ENUMERATION-PARAM-DEF>
                            <SHORT-NAME>enumParam</SHORT-NAME>
                            <DEFAULT-VALUE>GREEN</DEFAULT-VALUE>
                            <LITERALS>
                                <ECUC-ENUMERATION-LITERAL-DEF>
                                    <SHORT-NAME>RED</SHORT-NAME>
                                </ECUC-ENUMERATION-LITERAL-DEF>
                                <ECUC-ENUMERATION-LITERAL-DEF>
                                    <SHORT-NAME>YELLOW</SHORT-NAME>
                                </ECUC-ENUMERATION-LITERAL-DEF>
                                <ECUC-ENUMERATION-LITERAL-DEF>
                                    <SHORT-NAME>GREEN</SHORT-NAME>
                                </ECUC-ENUMERATION-LITERAL-DEF>
                            </LITERALS>
                        </ECUC-ENUMERATION-PARAM-DEF>
                    </PARAMETERS>
                </ECUC-PARAM-CONF-CONTAINER-DEF>
                <ECUC-PARAM-CONF-CONTAINER-DEF>
                    <SHORT-NAME>ContB</SHORT-NAME>
                    <LOWER-MULTIPLICITY>0</LOWER-MULTIPLICITY>
                    <UPPER-MULTIPLICITY-INFINITE>true</UPPER-MULTIPLICITY-INFINITE>
                    <SUB-CONTAINERS>
                        <ECUC-PARAM-CONF-CONTAINER-DEF>
                            <SHORT-NAME>ContBSubCont1</SHORT-NAME>
                            <LOWER-MULTIPLICITY>0</LOWER-MULTIPLICITY>
                            <UPPER-MULTIPLICITY-INFINITE>true</UPPER-MULTIPLICITY-INFINITE>
                            <PARAMETERS>
                                <ECUC-INTEGER-PARAM-DEF>
                                    <SHORT-NAME>intParam</SHORT-NAME>
                                    <LOWER-MULTIPLICITY>1</LOWER-MULTIPLICITY>
                                    <UPPER-MULTIPLICITY>1</UPPER-MULTIPLICITY>
                                    <MAX>65535</MAX>
                                    <MIN>0</MIN>
                                </ECUC-INTEGER-PARAM-DEF>
                            </PARAMETERS>
                            <REFERENCES>
                                <ECUC-REFERENCE-DEF>
                                    <SHORT-NAME>ref1</SHORT-NAME>
                                    <DESTINATION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/ModuleDef/demo/contA</DESTINATION-REF>
                                </ECUC-REFERENCE-DEF>
                            </REFERENCES>
                        </ECUC-PARAM-CONF-CONTAINER-DEF>
                    </SUB-CONTAINERS>
                </ECUC-PARAM-CONF-CONTAINER-DEF>
            </CONTAINERS>
        </ECUC-MODULE-DEF>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>
```
As mentioned earlier, when this file is provided to the asrGenerator, it generates the classes for the containers, parameters and references for the 'demo' module. For eg: The class 'demo' has getter methods to get the containers 'contA' and 'contB'. Similarly the class 'contA' has getter methods to get the parameters 'boolParam' and 'enumParam'.

Once the package for 'demo' is generated, lets build up the model for 'demo' by providing the a sample module configuration(as shown below).
```xml
<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://autosar.org/schema/r4.0 AUTOSAR_00049.xsd">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>ModuleConfig</SHORT-NAME>
      <ELEMENTS>
        <ECUC-MODULE-CONFIGURATION-VALUES>
          <SHORT-NAME>demo</SHORT-NAME>
          <DEFINITION-REF DEST="ECUC-MODULE-DEF">/ModuleDef/demo</DEFINITION-REF>
          <CONTAINERS>
            <ECUC-CONTAINER-VALUE>
              <SHORT-NAME>ContA_conf</SHORT-NAME>
              <DEFINITION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/ModuleDef/demo/contA</DEFINITION-REF>
              <PARAMETER-VALUES>
                <ECUC-NUMERICAL-PARAM-VALUE>
                  <DEFINITION-REF DEST="ECUC-BOOLEAN-PARAM-DEF">/ModuleDef/demo/contA/boolParam</DEFINITION-REF>
                  <VALUE>1</VALUE>
                </ECUC-NUMERICAL-PARAM-VALUE>
                <ECUC-TEXTUAL-PARAM-VALUE>
                  <DEFINITION-REF DEST="ECUC-ENUMERATION-PARAM-DEF">/ModuleDef/demo/contA/enumParam</DEFINITION-REF>
                  <VALUE>RED</VALUE>
                </ECUC-TEXTUAL-PARAM-VALUE>
              </PARAMETER-VALUES>
            </ECUC-CONTAINER-VALUE>
            <ECUC-CONTAINER-VALUE>
              <SHORT-NAME>ContB_conf</SHORT-NAME>
              <DEFINITION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/ModuleDef/demo/contB</DEFINITION-REF>
              <SUB-CONTAINERS>
                <ECUC-CONTAINER-VALUE>
                  <SHORT-NAME>subCont_conf</SHORT-NAME>
                  <DEFINITION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/ModuleDef/demo/contB/subCont</DEFINITION-REF>
                </ECUC-CONTAINER-VALUE>
              </SUB-CONTAINERS>
              <PARAMETER-VALUES>
                <ECUC-NUMERICAL-PARAM-VALUE>
                  <DEFINITION-REF DEST="ECUC-INTEGER-PARAM-DEF">/ModuleDef/demo/contB/subCont/intParam</DEFINITION-REF>
                  <VALUE>255</VALUE>
                </ECUC-NUMERICAL-PARAM-VALUE>
              </PARAMETER-VALUES>
              <REFERENCE-VALUES>
                <ECUC-REFERENCE-VALUE>
                    <DEFINITION-REF DEST="ECUC-REFERENCE-DEF">/ModuleDef/demo/contB/subCont/ref1</DEFINITION-REF>
                    <VALUE-REF DEST="ECUC-CONTAINER-VALUE">/ModuleConfig/demo/ContA_conf</VALUE-REF>
                </ECUC-REFERENCE-VALUE>
              </REFERENCE-VALUES>
            </ECUC-CONTAINER-VALUE>
          </CONTAINERS>
        </ECUC-MODULE-CONFIGURATION-VALUES>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>
```

Python code to build the model:
```python
from demo import demo
    demoNode = demo.read_and_build_module_configuration(sys.argv[1])
    if demoNode is not None:
        print('read sucessfull')
    else:
        print('read failed')
```
The variable 'demoNode' has object of the module configuration of 'demo' and we could get the containers 'contA' and 'contB' via the methods
```python
contANode = demoNode.get_contA()
contBNodes = demoNode.get_contBs()
```
> Please note that get_contBs() returns a list as the container 'contB' can have more than 1 instance in the module configuration. 

### Access Parameter values
Container classes has getter methods for accessing the parameter, which in turn returns the parameter objects. The parameter object has the getter methods for the following information:
- Value : The value configured in the configuration file
    - True/False for boolean parameter.
    - int value for integer parameter.
    - float value for float parameter.
    - string vale for enumeration/string/function parameter.
- DefaultValue : The default value available from the definition file.
- ParameterType : Enum value which returns the type of the parameter(BOOLEAN/INTEGER/FLOAT/STRING/FUNCTION/ENUMERATION).
- Min/Max value : Min and max value available from the definition file for integer and float parameters.

### Access Reference values
Container classes has getter methods for accessing the references, which in turn returns the reference objects. The reference object has the getter methods for the following information:
- Value : The value configured in the configuration file. Returns the value as String.
> The reason why we didn't returned the actual referenced node is due to the fact that the references could be pointing to a node in a different module or it could be a foreign reference. So, then, the user can use this path to identify the actual referenced node. Consider the following cases:
> - For reference to a container in the same module : user gets the value as path and then calls the `get_node` method by passing the path to retrieve the actual node.
> - For reference to a container in a different module : For eg: reference 'ref1' from 'demo' references a container 'contOther' of a module 'demoOther'. If you wish to retrieve the actual referenced node, then its recommended to generate the package for both the modules 'demo' and 'demoOther'. User gets the value as path from 'ref1' and then calls the `get_node` method of the 'demoOther' to retrieve the actual node.
> - For foreign references : User gets the value as path and he can do anything with it. Maybe, he could use this path to retrieve the actual object from the foreign file.
- ReferenceType : Enum value which returns the type of the reference(SIMPLE_REFERENCE/CHOICE_REFERENCE/FOREIGN_REFERENCE).
- DestintionRef : The destination ref available from the definition file. This is just available for simple and choice reference.
- DestinationType : The destination type available from the definition file. This is just available for foreign reference.

### Access nodes by path
It is possible to access a container/parameter/reference by the fully qualified path. 

```python
demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
contB = demo.get_node('/ModuleConfig/demo/ContB_conf_0')
self.assertTrue(contB is not None, "cannot be None")
```

There also exists another utility function to access container/parameter/reference by providing the definition path. For eg: this could be handy in situations where you need to know the description nodes for a definition node.

```python
demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
contB = demo.get_nodes_for_definition_path('/demo/contB')
self.assertTrue(contB is not None, "cannot be None")
self.assertEqual(len(contB), 2, "2 instance of contB are available")
self.assertEqual(contB[0].get_short_name(), 'ContB_conf_0', "short name is ContB_conf_0")
self.assertEqual(contB[1].get_short_name(), 'ContB_conf_1', "short name is ContB_conf_1")
```
> /demo/contB is the path to the definition container contB

### Modify parameter/reference values
It is possible to modify a parameter/reference values and save the changes. Changes are saved to the specified file passed to the `save()` method. If file name is not provided, the existing file is overwritten with the changes.

```python
module = demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
enumParam = demo.get_node('/ModuleConfig/demo/ContA_conf/enumParam')
enumParam.set_value('YELLOW')
intParam = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/intParam')
intParam.set_value(1234)
ref1 = demo.get_node('/ModuleConfig/demo/ContB_conf_0/subCont_conf/ref1')
ref1.set_value('/ModuleConfig/demo_other/ContA_conf_1234')
module.save(TEST_OUT_LOCATION)
```

### Access parent node
There exists a `get_parent()` API for each nodes to access its parent node.

```python
module = demo.read_and_build_module_configuration(DESC_FILE_LOCATION)
contB = demo.get_node('/ModuleConfig/demo/ContB_conf_0')
self.assertTrue(contB is not None, "cannot be None")
self.assertTrue(contB.get_parent() is not None, "parent cannot be None")
self.assertEqual(contB.get_parent().get_short_name(), 'demo' , "parents short name is demo")
self.assertEqual(contB.get_parent(), module , "the nodes should be same")
```

### Please refer the test "tests/test_generatedmodule.py" to know more about accessing different types of data from the generated module code.


