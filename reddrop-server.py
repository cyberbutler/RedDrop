
from logging import DEBUG

from waitress import serve
from confuse.exceptions import NotFoundError

import reddrop.authorization
from reddrop.app import app
from reddrop.config import ConfigTemplate, config
from reddrop.args import parse_arguments
from reddrop.logger import prettyPrintFormatString

if __name__ == "__main__":
    import sys
    args = parse_arguments()

    config.set_args(args, dots=True)
    
    if len(args.process_list) > 0:
        prettyPrintFormatString('{{ c("yellow", "[!] The following processing list has been set, turning off auto_process: ") }}{{process_list}}', {"process_list": args.process_list})
        config['auto_process'].set(False)

    if args.dump_config:
        print(config.dump())
        sys.exit()

    if args.config:
        config.set_file(args.config)

    try:
        config.get(ConfigTemplate)
    except NotFoundError as e:
        app.logger.error(f'The configuration file provided is invalid, please fix: {e}')
        sys.exit()

    if args.authorization_rules:
        # We must recompile the authorization rules here as they have already been compiled at load time
        reddrop.authorization.compiled_rules = reddrop.authorization.compileRules()
    
    if config['debug'].get():
        app.logger.setLevel(DEBUG
        )
        app.run(config['host'].get(), port=config['port'].get(), debug=config['debug'].get())

    else:
        app.logger.info("Starting Redbox Exfil Server")
        serve(app, host=config['host'].get(), port=config['port'].get())