from yaml import load

__config = None


def config():
    global __config

    if not __config:
        with open("config.yaml", "r") as f:
            __config = load(f)

    return __config

    


