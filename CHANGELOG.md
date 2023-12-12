# ChangeLog
All notable changes to this project will be documented in this file.

## [0.1.0]() - 2020-12-12
First release of the AutosarConfigReader. Please refer README for more information.

## [0.1.4]() - 2020-12-14
### Added
- New API to get all instances of an Autosar node by its definition path.
- Support for references with upper multiplicity > 1
- New API to get_parent() to get the parent of any nodes
- New API set_value() to set the value of parameter/reference nodes
- It is now possible to save() the file once the parameter/reference values are modified

## [0.1.5]() - 2020-12-15
### Changed
- Unique classes are generated if there exists containers with duplicate names
- Module name option is now case-insenstive. Tool accepts both `-m com` or `-m Com

## [0.1.6]() - 2021-01-08
### Added
- New API `new` to create a new module configuration file
- Its now possible to create new containers/parameters/reference.

## [0.1.7]() - 2023-12-12
### Added
- Added support for instance reference
