import os

class TomlFile:
    def __get__(self, instance, owner):
        return instance._config_file_path

    def __set__(self, instance, value):
        if not os.path.isfile(value):
            raise ValueError(f"Invalid config file path: {value}")
        if not value.lower().endswith('.toml'):
            raise ValueError(f"Invalid config file extension: {value}")
        instance._config_file_path = value
