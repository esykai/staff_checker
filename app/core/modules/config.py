import configparser

config = configparser.ConfigParser()
config.read('app/config/constants.ini', encoding='utf-8')


def get_config_text(what, name):
    return config.get(what, name)
