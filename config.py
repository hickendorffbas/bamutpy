import tomli  #TODO: use tomllib when on python verison 3.11


_CONFIG = None


def get_config():
    return _CONFIG


class Config():

    def __init__(self, verbose_logging, main_project_folder, test_module_folder, amount_of_mutations):
        self.verbose_logging = verbose_logging
        self.main_project_folder = main_project_folder
        self.test_module_folder = test_module_folder
        self.amount_of_mutations = amount_of_mutations

    @classmethod
    def load(cls):
        with open("config.toml", "r") as config_file:
            config_dict = tomli.loads(config_file.read())

        loaded_config = Config(config_dict["general"]["verbose_logging"],
                               config_dict["paths"]["main_project_folder"],
                               config_dict["paths"]["test_module_folder"],
                               config_dict["general"]["amount_of_mutations"])

        global _CONFIG
        _CONFIG = loaded_config

