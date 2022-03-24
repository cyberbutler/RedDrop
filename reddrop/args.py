import argparse

from reddrop.logger import c
from reddrop.processors import getProcessorNames


class CustomArgumentFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

class ParseKeyValue(argparse._AppendAction):
    """
    This Argparse Action extends the "append" action. It will split a provided argument on the first `=` character and return
    a dictionary like so: 
    ```
        key=value 
    # Becomes:
        {'key': 'value'}
    ```
    """
    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values, option_string) -> None:
        splitValues = values.split('=')
        key = splitValues[0]
        rule = '='.join(splitValues[1:])
        values = {'key': key, 'rule': rule}

        super(ParseKeyValue, self).__call__(parser, namespace, values, option_string)

def ascii_banner():
    return """
                      +:                     
                    .*##-                    
                   :##**#+                   
                  +#*****##:                 
                :##********#+                
               =#***********#+               
              =#******#******#*              
            .+#******#-*#*****##-            
           -#******#*.  =#******#*           
          +#******#+     :##*****##:         
        .*#*****##-        +#******#=        
       :#******#+.          -#******#+       
      -#******#-             :##*****#*.     
     +#******#:               .*#*****##:    
   :##*****#*.                  =#******#+   
    *#****#-                     .*#****#-   
   +#***##.                        =#***##:  
  +#****##.                        +#*****#: 
 +#****##.                          =#*****#.
:#*****#.                            ******#=
*#******         Red    Drop         -#******
#******+                             :#*****#
#*******                             -#*****#
*#*****#.                            +*******
-#*****#*                           -#*****#=
 *#*****#*.                        =#******#.
  *#******#=.                    -*#******#- 
   +#*******#*-               :+##******##:  
    -##*******##*+=-:...::-=+##********#*.   
      -*#**********#######***********#+:     
        -*#***********************##+.       
          .=+##***************##*=:          
              :-=+**######**+=:              

    """.replace('*', c('red', '*'))

def parse_arguments():
    args = argparse.ArgumentParser(
        description=f"{ascii_banner()} A Webserver for File and Data Exfiltration.\n\tAuthor: @{c('red', 'cyberbutler')}/@{c('blue', 'thecyberbutler')}",
        epilog="Far more configuration options exist which must be specified in Environment Variables, use `--dump-config` to see all of the options",
        formatter_class=CustomArgumentFormatter
    )
    args.add_argument(
        '-H', '--host', 
        help="The host IP Address to bind to", 
        default="0.0.0.0"
    )
    args.add_argument(
        '-P','--port',
        help="The port to bind to", 
        default=80, 
        type=int
    )
    args.add_argument(
        '-c', '--config',
        help="YAML config file path"
    )
    args.add_argument(
        '--dump-config', 
        default=False, 
        action='store_true', 
        help="Dump the configuration settings as YAML"
    )
    args.add_argument(
        '--debug', 
        default=False, 
        action='store_true', 
        help="Enable Flask's Debug Mode"
    )
    args.add_argument(
        '-p', '--processor', 
        help='Specify a processor to use. This flag can be used more than once to define multiple %(dest)s functions. Use this flag in the order in which you wish to process received data',
        dest='process_list',
        action='append', 
        choices=getProcessorNames(), 
        default=[]
    )
    args.add_argument(
        '-A', '--auto-process',
        help='Automatically run processors based on detected data. This option is enabled by default, but should be disabled (--no-auto-process) when you receive output you don\'t expect. Such as in the case of Base64 decoding being run on output that is not Base64 encoded. Instead, force the process with the `-p` flag.',
        default=True,
        action=argparse.BooleanOptionalAction
    )
    args.add_argument(
        '-x','--auto-extract-tar',
        help='Auto extract TAR archives received by the server.',
        action='store_true',
        default=False
    )
    args.add_argument(
        '--encryption-password', 
        help='The password used to decrypt/encrypt.',
        dest='processor_arguments.openssl-aes256-pbkdf2.password',
        default="EncryptMe"
    )
    args.add_argument(
        '-r', '--authorization_rules',
        help="Specify an Authorization Rule to deny requests which do not match the provided Key and Regex value pair. Specified as <Key>=<Regex>.",
        action=ParseKeyValue
    )
    args.add_argument(
        '-t', '--tag',
        help='Tag data received during this session in the logs as well as the directory files are uploaded to. Example: -t log4j -t acme.org',
        action='append',
        dest='tags'
    )

    return args.parse_args()
