from typing import OrderedDict, Union
from cff2toml.models.files.metadata_file import MetadataFile
import tomlkit


class LoadTomlFileException(Exception):
    pass


class SaveTomlFileException(Exception):
    pass


class TomlFile(MetadataFile):

    def __init__(self, file_path: str):
        super().__init__(file_path=file_path)
        self.file_path = file_path
        try:
            with open(self.file_path, 'r') as toml_file:
                self._metadata.from_dict(
                    OrderedDict(tomlkit.load(toml_file).value))
        except:
            raise LoadTomlFileException(
                f"Cannot load this TOML file: {self.file_path}")

    def save(self, file_path: Union[str, None] = None) -> None:
        if file_path is None:
            file_path = self.file_path
        if self._metadata is not None:
            try:
                with open(file_path, 'w') as toml_file:
                    tomlkit.dump(OrderedDict(self._metadata.to_dict()),
                                 toml_file)
            except:
                raise SaveTomlFileException(
                    f"Cannot save this TOML file: {file_path}")
        else:
            raise SaveTomlFileException(
                f"Cannot save this TOML file: {file_path} because there is no data.")
