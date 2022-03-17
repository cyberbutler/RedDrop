from redbox.logger import logger
from redbox.config import config
from redbox.processors import processFromList

def processRequestParameter(field, value, processing_list=[]) -> dict:
    try:
        processedData = str(value).encode("utf-8")
    except AttributeError as e:
        # object has no attribute 'encode'
        processedData = value

    try:
        processedData, processing_list = processFromList(processedData, processing_list)

    except RecursionError:
        logger.error("The payload could not be processed automatically. It may be getting recognized repeatedly by a data processor. You should force the processing parameters.")

    try:
        processedData = processedData.decode("utf-8") if processedData else None

    except UnicodeDecodeError as e:
        if config['auto_process'].get():
            logger.error((
                'There was an issue when attempting to decode the processedData. ' 
                'It appears you have Auto Process enabled. This can cause issues in some cases where the `validate` functions of the Processors identify plaintext as something it is not. '
                'Try forcing the encoding pattern and attempt your request again. '
                f'Detected: Process Order: {processing_list}'
            ))
        else:
            logger.error(f'There was an issue when attempting to decode the processedData. Is the data encoded or encrypted properly?')

        processedData = None
    

    dataLogObject = {
        "field": field,
        "originalValue": value,
        "processedValue": processedData,
        "process": processing_list
    }


    return dataLogObject