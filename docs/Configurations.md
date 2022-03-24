# Configurations
RedDrop can be configured using a multitude of configurations through a specified YAML config file (`-c` CLI Arugment). The Default configuration, which you can view with the `--dump-config` CLI Argument, looks like this:

```yaml
authorization_rules: []
auto_extract_tar: no
auto_process: yes
debug: no
host: 0.0.0.0
port: 80
process_list: []
processor_arguments:
    openssl-aes256-pbkdf2:
        password: EncryptMe
        iterations: 10000
    b64: {}
    gzip: {}
    hex: {}
tags: []
failure_response: Failed
success_response: Received
log_format_template:
    initial_request: '[{{ c("blue", time.strftime("%m/%d/%y %H:%M:%S")) }}] {{ c("yellow", src) }} {{ c("grey", method) }} {{ c("green", "/" + path) }}'
    data_received: '[{{ c("blue", ", ".join(process)) }}]-> {{ c("green", field) }}

        {{processedValue if processedValue else originalValue}}


        '
    file_uploaded: '[{{ c("bold", c("red", "FILE UPLOAD")) }}][{{ c("blue", ", ".join(process)) }}] {% if autoExtracted %}{{c("yellow", "Extracted Archive")}}{% endif %} => {{ c("green", fileDir + "/" + fileName) }}

        '
log_encryption_password: no
upload_dir: uploads
process_list_header: Process
```

A description of each option is as follows:
| Option | Description |
| ------ | ----------- |
| `authorization_rules` | The [Authorization Rules](AuthorizationRules.md) to use. A list of dictionaries in the format: ```{'key': '<Request Key>', 'rule': '<Regular Expression>'}``` |
| `auto_extract_tar` | Automatically extract uploaded TAR files.<br> This software uses a small function to check if any tar members have insecure filenames before extraction |
| `auto_process` | Automatically attempt to identify and process payloads, rather than through the `process_list` |
| `debug` | Enable Flask's Debugger |
| `host` | The Host to bind to |
| `port` | The Port to bind to on the host |
| `process_list` | The modules, in processing order, to use for processing payloads |
| `processor_arguments` | This is where you can ovveride the parameters specified in Processor Modules, as Processors are populated, so are the parameters they specify in the `--dump-config` option. |
| `tags` | Specify tags to be applied to data captured during the runtime session. Be sure to remove tags between different sessions if you do not want them to be applied to new data. Sessions which have tags applied to them will save files in the configured `upload_dir` in a new directory named by joining tags with a `-` character | 
| `failure_response` | The response to send to clients on a failed request. This is a [Jinja Template](https://jinja.palletsprojects.com/en/3.0.x/) | 
| `success_response` | The response to send to clients on a successful request. This is a [Jinja Template](https://jinja.palletsprojects.com/en/3.0.x/) | 
| `log_format_template` | These are how messages are displayed in the console, each child item in the default configuration can be changed to display data in a way that suits you best. <br>`initial_request` is displayed first, see the options avaialble for display in [`app.py`](https://github.com/cyberbutler/RedDrop/tree/master/reddrop/app.py).<br>`data_received` is displayed when a request parameter is received and for each subsequent parameter in each request. See the return dict in [`request_processing.py`](https://github.com/cyberbutler/RedDrop/tree/master/reddrop/request_processing.py) for display fields. <br>`file_uploaded` is displayed when a file is uploaded. See the return dict in [`file_processing.py`](https://github.com/cyberbutler/RedDrop/tree/master/reddrop/file_processing.py) for display fields.
| `log_encryption_password` | Whether to log the specified encryption password to the log files in cleartext |
| `upload_dir` | The directory to store uploaded files to |
| `process_list_header` | The Header field which allows a client to specify the `process_list` using a comma separated value
