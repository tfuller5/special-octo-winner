import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')

#logging.basicConfig(level=logging.WARNING)
#logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.CRITICAL)
#logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.ERROR)

def hypotenuse(a, b):
    """Compute the hypotenuse"""
    return (a**2 + b**2)**0.5

kwargs = {'a':3, 'b':4, 'c':hypotenuse(3, 4)}

logger.debug("a = {a}, b = {b}".format(**kwargs))
logger.info("Hypotenuse of {a}, {b} is {c}".format(**kwargs))
logger.warning("a={a} and b={b} are equal".format(**kwargs))
logger.error("a={a} and b={b} cannot be negative".format(**kwargs))
logger.critical("Hypotenuse of {a}, {b} is {c}".format(**kwargs))