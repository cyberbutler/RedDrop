# Automatic Payload Processing
Payloads are the contents of an HTTP request parsed by RedDrop. RedDrop features various Processors which can automatically detect payloads and parse, transform, decode, or decrypt the data within. These Processors can be found [here](https://github.com/cyberbutler/RedDrop/tree/master/reddrop/processors). 

## Create a Processor
Processors can be created by extending the [`BaseProcessor`](https://github.com/cyberbutler/RedDrop/tree/master/reddrop/processors/BaseProcessor.py) class and overriding the `processData` and `validate` methods. Whats most important is that the `processData` return a value as the `bytes` type, and `validate` a `bool` type. Processors should be placed into the `reddrop/processors/` directory and the server should be restarted before the Processor is registered. 

Processors should also set the following attributes:
`name` should be set in Processors. This allows the program to select and create classes based on the name attribute,
rather than instantiating the Class directly. For example, when using the `-p` CLI argument flag.

`parameters` is a dictionary of arguments which can be defined with set defaults to be passed to the `processData` function. 
This allows users to then specify configuration options to change the default values as they wish. See [AES256PBKDF2Processor.py](https://github.com/cyberbutler/RedDrop/tree/master/reddrop/processors/AES256PBKDF2Processor.py) for an example.

`priority` allows you to specify the sort priority. Higher numbers will be added to the processing list first, while lower numbers will be last. The default priority  is `5`
