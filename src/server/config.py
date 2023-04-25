import configparser

class Config:
    _instance = None

    def __init__(self):
        self._config = configparser.ConfigParser()
    
    def read(self, filepath: str):
        '''
        Reads the data from config file.

        :param filepath: path to the config file
        '''
        self._config.read(filepath)

def get_config():
    '''
    Returns config singleton instance.

    :return: Config instance
    '''
    if type(Config._instance) != Config:
        Config._instance = Config()
    return Config._instance

def get_str(section: str, key: str, default: str):
    '''
    Return string value in given section and with given key.

    :param section: config section
    :param key: config key
    :param default: default value return when key is not found

    :return: config value
    '''
    if section in get_config()._config:
        if key in get_config()._config[section]:
            return get_config()._config[section][key]
    return default

def get_int(section: str, key: str, default: int):
    '''
    Return int value in given section and with given key.

    :param section: config section
    :param key: config key
    :param default: default value return when key is not found or parsing fails

    :return: config value
    '''
    if section in get_config()._config:
        if key in get_config()._config[section]:
            try:
                value_str = get_config()._config[section][key]
                return int(value_str)
            except:
                return default
    return default