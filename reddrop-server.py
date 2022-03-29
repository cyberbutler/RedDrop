
from logging import DEBUG

import gunicorn.app.base
from confuse.exceptions import NotFoundError

import reddrop.authorization
from reddrop.app import app
from reddrop.config import ConfigTemplate, config
from reddrop.args import parse_arguments
from reddrop.logger import prettyPrintFormatString

class RedDropApplication(gunicorn.app.base.BaseApplication):
    """
    The Gunicorn Application Base for Red Drop:
    https://docs.gunicorn.org/en/stable/custom.html#custom-application
    """

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    import sys
    args = parse_arguments()

    if args.config:
        config.set_file(args.config)

    config.set_args(args, dots=True)
    
    if len(args.process_list) > 0:
        prettyPrintFormatString('{{ c("yellow", "[!] The following processing list has been set, turning off auto_process: ") }}{{process_list}}', {"process_list": args.process_list})
        config['auto_process'].set(False)

    if args.dump_config:
        print(config.dump())
        sys.exit()

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
        app.logger.info("Starting RedDrop Exfil Server")
        
        options = config['gunicorn'].get()
        options.update(config['gunicorn']['defaults'].get())
        options['bind'] = f'{config["host"].get()}:{config["port"].get()}'

        RedDropApplication(app, options).run()