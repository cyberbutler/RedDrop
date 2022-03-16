from redbox.config import config 

def getListFromConfigHeader(request, header:str, default_options:list) -> list:
    """
    Return a list of values based on a provided comma-separated Request Header.
    If the provided header is not found in the request, return the `default_options`
    """
    return [
        d.strip() for d in request.headers.get(header).split(',') if len(d.strip())
    ] if request.headers.get(header) else default_options