from .argumentparser import parseArguments, argParserStatus
from .autosarfileprocessor import AutosarFileProcessor, FileReaderStatus, ParameterTypes, ReferenceTypes
import logging, os, time
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

version = '0.1.0'
inputFile =''
outputFolder =''

def main():
    arguments = parseArguments()
    if arguments.get_parser_status() == argParserStatus.SUCCESS:
        fileProcessor = AutosarFileProcessor(arguments.get_input_file(), arguments.get_module())
        if fileProcessor.get_status() == FileReaderStatus.MODULE_FOUND:
            logging.info('Module {} found in the input file!'.format(arguments.get_module()))
            generate(fileProcessor.build_module(), arguments.get_output_folder())
            logging.info('Generation successful!')
        else:
            logging.error('Module {} not found in the input file!'.format(arguments.get_module()))

def generate(module, outputFolder):
    Path(outputFolder).mkdir(parents=True, exist_ok=True) #create output folder if doesn't exist
    moduleFolder = os.path.join(outputFolder, module.get_name())
    Path(moduleFolder).mkdir(parents=True, exist_ok=True) #create folder with module name if doesn't exist

    file_loader = FileSystemLoader(os.path.join(Path(__file__).parent.absolute(), 'templates'))
    env = Environment(loader=file_loader)

    #__init__.py generation
    template = env.get_template('moduleInitTemplate.txt')
    output = template.render(module = module, time = time.ctime(time.time()))
    
    initFile = open(os.path.join(moduleFolder, '__init__.py'), "w")
    initFile.write(output)
    initFile.close()

    #module.py generation
    template = env.get_template('moduleFileTemplate.txt')
    output = template.render(module = module, time = time.ctime(time.time()), ParameterTypes = ParameterTypes, ReferenceTypes = ReferenceTypes)
    
    moduleFile = open(os.path.join(moduleFolder, module.get_name() + '.py'), "w")
    moduleFile.write(output)
    moduleFile.close()

logging.basicConfig(format = '%(asctime)s: [%(levelname)s] %(message)s', datefmt = '%Y-%m-%d %H:%M:%S', level = logging.INFO)
main()