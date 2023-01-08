from bamutpy.config import get_config

def log(message):
    if get_config().verbose_logging:
        print(message)

