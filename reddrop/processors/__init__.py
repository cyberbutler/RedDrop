"""
Processors are the payload manipulators used to decode, parse, decrypt, etc data passed in HTTP requests.
This module will auto import anything in the reddrop.processors.* path, so long as the following rules are met:

The processor filename must end with 'Processor.py'
The processor must implement the BaseProcessor class
The processor class name must be the same as its module name. 
"""

import importlib
import os
import inspect

from reddrop.config import config
from reddrop.logger import logger
from .BaseProcessor import BaseProcessor


processors = []

# Dynamically load Processors from reddrop/processors/*Processor.py
for dirpath, dirnames, filenames in os.walk(os.path.dirname(__file__)):
    for filename in filenames:
        if filename.endswith('Processor.py') \
        and filename != "__init__.py" \
        and filename != "BaseProcessor.py":

            modulename = filename.replace('.py','')
            module = importlib.import_module(f'reddrop.processors.{modulename}')
            processor = getattr(module, modulename)
            
            if inspect.isclass(processor) and issubclass(processor, BaseProcessor):
                processors.append(processor)
            else:
                raise ImportError(f"The Processor module '{modulename}' is invalid. It does not implement a BaseProcessor subclass'")

# Sort processors by their priority - This lets us force Base64 to be the last processor used to avoid cases where it tries to auto process a payload that isn't actually base64 (yet)
processors.sort(key=lambda p: p.priority * -1)

def getProcessorNames() -> list:
    """Returns a list of Processor names"""
    return [p.name for p in processors]

def getProcessorFromName(name: str) -> BaseProcessor:
    """
    Returns an uninitialized subclass of BaseProcessor given the `name` property
    """
    try:
        processor = next(
            (p for p in processors if p.name == name)
        )
    except StopIteration:
        raise ValueError(f'Invalid Coder Name: {name}')

    return processor

def processFromList(processedData, processing_list, detected=[], autoProcess=False):
    """
    Processes a payload via the processors defined in `processing_list`. 
    If a processing_list is empty, autoProcess will become True and this function will run recursively
    through all loaded processors until the `.validate()` method of each processor returns False.
    """
    if config['auto_process'].get() and len(processing_list) == 0:
        autoProcess = True
        processing_list = getProcessorNames()

    for pname in processing_list:
        try:
            Processor = getProcessorFromName(pname)()
            if autoProcess:
                if Processor.validate(processedData):
                    detected = detected + [pname]
                    processedData = Processor.processData(
                        processedData, 
                        **config['processor_arguments'][pname].get()
                    )

                    return processFromList(
                        processedData, 
                        processing_list, 
                        detected, 
                        autoProcess=autoProcess
                    )
            
            else:
                detected = detected + [pname]
                processedData = Processor.processData(
                    processedData, 
                    **config['processor_arguments'][pname].get()
                )

        except Exception as e:
            logger.error(f'Failed to decode data using Processor:{pname}: {e}', extra={"error": e})
            processedData = None

    return processedData, detected
