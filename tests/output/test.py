#This file is generated for the module 'Rte' on Fri Dec 11 11:22:05 2020.

from Rte import Rte
import sys

rteNode = Rte.read_and_build_module_configuration(sys.argv[1])
if rteNode is not None:
    print('read sucessfull')
else:
    print('read failed')