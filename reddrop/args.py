import argparse

from reddrop.logger import c
from reddrop.processors import getProcessorNames


class CustomArgumentFormatter(argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter):
    pass

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
        '--host', '-H', 
        help="The host IP Address to bind to", 
        default="0.0.0.0"
    )
    args.add_argument(
        '--port', '-P', 
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
        '--auto-extract-tar', '-x',
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

    return args.parse_args()
