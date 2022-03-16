from redbox.config import config
class BaseProcessor:
    """
    The base class for Processors. Processors are classes which are used for processing passed payloads.
    Subclasses should implement and override the `processData` and `validate` functions accordingly.

    The `name` should be set in subclasses as well. This allows the program to select and create classes based on the name attribute,
    rather than instantiating the Class directly. 

    `parameters` is a dictionary of arguments which can be defined with set defaults to be passed to the `processData` function. 
    This allows users to then specify configuration options to change the default values as they wish. See AES256PBKDF2Processor.py for an example.

    `priority` allows you to specify the sort priority. Higher numbers will be added to the processing list first, while lower numbers will be last.
    """
    name = ""
    parameters = {}
    priority = 5
    
    def loadParameters(self) -> None:
        """
        Sets the default parameters in the Confuse ConfigSource for the Coder.
        """
        config[f'processor_arguments'].set({self.name: self.parameters})
    
    def processData(self, *args, **kwargs) -> bytes:
        raise NotImplementedError()

    def validate(self, *args, **kwargs) -> bool:
        raise NotImplementedError()
