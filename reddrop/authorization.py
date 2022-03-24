import re
from functools import wraps

from flask import make_response, request, render_template_string, current_app

from reddrop.config import config

def compileRules():
    return [{'key': rule['key'], 'rule': re.compile(rule['rule'])} for rule in config['authorization_rules'].get()]

compiled_rules = compileRules()

def authorize(func):
    @wraps(func)
    def with_authorization(*args, **kwargs):
        request_parameters = dict(**kwargs)
        request_parameters.update(request.headers)
        request_parameters.update(request.args.to_dict())
        request_parameters.update(request.form.to_dict())
        
        isValidated = []

        for rule in compiled_rules:
            try:
                match = bool(rule['rule'].match(
                            request_parameters[rule['key']]
                        ))
            except KeyError:
                match = False
            
            isValidated.append(match)
        
        if len(isValidated) == 0 or all(isValidated):
            current_app.logger.debug('A request passed the set authorization rules', extra={
                'authorization_rules': config['authorization_rules'].get(),
                'parameters': request_parameters
            })
            return func(*args, **kwargs)

        else:
            current_app.logger.info('A request failed the set authorization rules', extra={
                'authorization_rules': config['authorization_rules'].get(),
                'parameters': request_parameters
            })
            return make_response(render_template_string(config['failure_response'].get()))

 
    return with_authorization