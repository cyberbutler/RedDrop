import confuse

config = confuse.Configuration('RedDrop', __name__)

# Defaults
# The Host to bind to
config['host'] = '0.0.0.0'

# The Port to bind to on the host
config['port'] = 80

# Enable Flask's Debugger
config['debug'] = False

# The modules, in processing order, to use for processing payloads
config['process_list'] = []

# Automatically extract uploaded TAR files. 
# This software uses a small function to check if any tar members have insecure filenames before extraction
config['auto_extract_tar'] = False

# The header that can be passed by clients to specify processing order
config['process_list_header'] = 'Process'

# The directory to store files
config['upload_dir'] = 'uploads'

# Automatically attempt to identify and process payloads, rather than through the `processing_list`
config['auto_process'] = True

# Log the encryption password with the request
# WARNING: This logs the password in cleartext!
config['log_encryption_password'] = False

# This is where you can override the parameters to Processor modules
config['processor_arguments'] = {}

# Pretty Printer Jinja Templates
config['log_format_template'] = {
    'initial_request': (
        '[{{ c("blue", time.strftime("%m/%d/%y %H:%M:%S")) }}] '
        '{{ c("yellow", src) }} {{ c("grey", method) }} {{ c("green", "/" + path) }}'
    ),
    'data_received': (
        '[{{ c("blue", ", ".join(process)) }}]-> {{ c("green", field) }}\n{{processedValue if processedValue else originalValue}}\n\n'
    ),
    'file_uploaded': (
        '[{{ c("bold", c("red", "FILE UPLOAD")) }}][{{ c("blue", ", ".join(process)) }}] {% if autoExtracted %}{{c("yellow", "Extracted Archive")}}{% endif %} => '
        '{{ c("green", fileDir + "/" + fileName) }}\n'
    )
}

# The response to send to clients on a sucessful request. This is a Jinja2 Template
config['success_response'] = (
    "Received"
)

# The response to send to clients on a failed request. This is a Jinja2 Template
config['failure_response'] = (
    "Failed"
)

# This is a list of rules which will authorize requests to pass data in
# The list should be populated with dicitonaries in the following format:
# ```
# {'key': 'path || <insert parameter>', 'rule': 'regular expression'}
# ```
config['authorization_rules'] = []

# Confused Configuration Template for validating user provided configuration options
ConfigTemplate = {
    'authorization_rules': confuse.Sequence({
        'key': str,
        'rule': str
    })
}

# Set config from environment variables
# Example: REDDROP_HOST=0.0.0.0
config.set_env()

if __name__ == "__main__":
    # Dump Default Configuration
    print(config.dump())
