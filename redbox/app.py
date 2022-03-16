__author__ = "Allen Butler"
__maintainer__ = "cyberbutler"

import logging
import datetime

from flask import Flask, render_template_string, request

from redbox.logger import prettyPrintFormatString
from redbox.config import config
from redbox.processors import processors
from redbox.utils import getListFromConfigHeader
from redbox.request_processing import processRequestParameter
from redbox.file_processing import processFile

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

for Processor in processors:
    Processor().loadParameters()

@app.route('/', methods=['POST', 'GET', 'PUT'], defaults={"path": ""})
@app.route('/<path:path>', methods=['POST', 'GET', 'PUT'])
def processRequest(path):
    src_ip = request.headers.get('X-FORWARDED-FOR', request.remote_addr)

    # Get a list of decode names from the request header if available, otherwise default to the server configured version
    processing_list = getListFromConfigHeader(request, config['process_list_header'].get(), config['process_list'].get())

    requestLogObject = {
        "time": datetime.datetime.now(),
        "remote_addr": request.remote_addr,
        "src": src_ip,
        "method": request.method,
        "path": path,
        "files": [],
        "headers": dict(request.headers),
        "data": [],
        "password": config['encryption_password'].get() if config['log_encryption_password'].get() else None
    }
    
    prettyPrintFormatString(
        config['log_format_template']['initial_request'].get(), 
        requestLogObject
    )

    try:
        request_parameters = {}
        if request.json is not None:
            request_parameters.update(request.json)

        if len(request.data) and not request.is_json:
            request_parameters.update({"unparsed_data": request.data})

        request_parameters.update(request.args.to_dict())
        request_parameters.update(request.form.to_dict())

        # Parse Request Parameters
        for field,value in request_parameters.items():
            if len(value) == 0:
                app.logger.info(f"Parameter {field} has no value")
                continue

            dataLogObject = processRequestParameter(
                field, value, processing_list 
            )
            
            requestLogObject['data'].append(dataLogObject)

            prettyPrintFormatString(
                config['log_format_template']['data_received'].get(), 
                dataLogObject
            )
                

        # Parse Files
        for parameter, f in request.files.items():
            fileLogObject = processFile(
                parameter, f, src_ip, processing_list
            )

            requestLogObject['files'].append(fileLogObject)

            prettyPrintFormatString(
                config['log_format_template']['file_uploaded'].get(), 
                fileLogObject
            )

    except Exception as e:
        app.logger.error({"error": e}, extra=requestLogObject)
        return render_template_string(config['failure_response'].get())
    
    app.logger.info("A Request Has Been Processed", extra=requestLogObject)
    return render_template_string(config['success_response'].get())