import inspect
import logging

logger = logging.getLogger( 'app.' + __name__ )

logFormatter = logging.Formatter( '%(asctime)-5s - %(levelname)-5s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S' )

logHandler = logging.FileHandler( 'log/app.log', encoding='utf-8')
logHandler.setFormatter( logFormatter )
logger.addHandler( logHandler )

logger.setLevel( logging.INFO )


def log(func):
    def wrapper(*args,**kwargs):
        logger.info(f'function name: "{func.__name__}", arguments: {args, kwargs}')
        r = func(*args, **kwargs)
        logger.info(f'Function "{func.__name__}" called from a function "{inspect.stack()[1][3]}"')
        return r
    return wrapper