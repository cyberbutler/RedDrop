from waitress import serve

from reddrop.app import app
from reddrop.config import config
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
        
    if config['debug'].get():
        app.run(config['host'].get(), port=config['port'].get(), debug=config['debug'].get())
    else:
        app.logger.info("Starting Redbox Exfil Server")
        serve(app, host=config['host'].get(), port=config['port'].get())