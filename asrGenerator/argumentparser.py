import logging, argparse,os
from pathlib import Path
from enum import Enum

argParserStatus = Enum('ArgParserStatus', 'SUCCESS FAILURE')

class Arguments:
    def __init__(self, input = None, module = None, output = None, status = argParserStatus.FAILURE):
        self.inputFile = input
        self.module = module
        self.outputFolder = output
        self.parseStatus = status
    
    def get_input_file(self):
        return self.inputFile

    def get_module(self):
        return self.module

    def get_output_folder(self):
        return self.outputFolder

    def get_parser_status(self):
        return self.parseStatus

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help = 'Absolute file path to the autosar module definition file')
    parser.add_argument('-m', '--module', help = 'The module for which the python classes should be generated')
    parser.add_argument('-o', '--output', help = 'Location where the python classes should be generated')
    args = parser.parse_args()
    
    inputFile = args.input
    if inputFile is None:
        logging.error('Module definition file is not provided.')
    else:
        inputFilePath = Path(inputFile)
        if inputFilePath.is_file():
            # file exists
            outputFolder = args.output
            if outputFolder == '.':
                outputFolder = os.getcwd()
            else:
                Path(outputFolder).mkdir(parents=True, exist_ok=True)
            return Arguments(input = inputFile, module = args.module, output = outputFolder, status = argParserStatus.SUCCESS)
        else:
            logging.error('Cannot find the module definition file :' + inputFile)
    
    return Arguments(status = argParserStatus.FAILURE)