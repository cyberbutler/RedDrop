import os
import sys
import logging
import datetime
from logging.handlers import TimedRotatingFileHandler

from reddrop.config import config

from jinja2 import Environment, BaseLoader
from pythonjsonlogger import jsonlogger

supported_keys = [
    'asctime',
    'created',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'message',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'thread',
    'threadName'
]

def c(color, message):
    colors = {
        'header': '\033[95m',
        'darkgrey': '\033[38;5;237m',
        'grey': '\033[90m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'darkred': '\033[38;5;1m',
        'red': '\033[91m',
        'ENDC': '\033[0m',
        'bold': '\033[1m',
        'underline': '\033[4m'
    }

    return colors[color] + str(message) + colors['ENDC']

def prettyPrintFormatString(fmt:str, vars:dict) -> str:
    template=Environment(loader=BaseLoader()).from_string(fmt)
    output = template.render(c=c, **vars)
    print(output.replace('\r\n', '\n'), file=sys.stderr)

class RedDropLogFormatter(logging.Formatter):
    """
    Greys out default logs. This is to draw a greater contrast to the output of prettyPrintFormatString
    """
    def format(self, record):
        if not config['debug'].get():
            fmt = c('darkgrey', self._fmt)
        else:
            fmt = self._fmt

        if record.levelname == "ERROR":
            record.levelname = c("darkred", record.levelname)
        

        formatter = logging.Formatter(fmt)
        return formatter.format(record)

def log_format(x): 
    return ['%({0:s})s'.format(i) for i in x]

logger = logging.getLogger()
    
# STDOUT Formatter
stdoutFormat = '%(levelname)s - %(name)s - %(funcName)s - L:%(lineno)s %(message)s'
stdoutHandler= logging.StreamHandler()
stdoutHandler.setFormatter(RedDropLogFormatter(stdoutFormat))

# JSON Formatter
custom_format = ' '.join(log_format(supported_keys))
jsonFormatter = jsonlogger.JsonFormatter(custom_format)

if not os.path.exists('logs'):
    os.makedirs('logs')

rotatitingFileHandler = TimedRotatingFileHandler(
    'logs/' + datetime.datetime.strftime(datetime.datetime.now(), "%m-%d-%Y") + ".log.json",
    when='d'
)
rotatitingFileHandler.setFormatter(jsonFormatter)

# Add Handlers
logger.addHandler(rotatitingFileHandler)
logger.addHandler(stdoutHandler)