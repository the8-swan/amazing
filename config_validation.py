class ErrorConfig(Exception):
    pass


def config_validation(text: str):
    return text.split('\n')
