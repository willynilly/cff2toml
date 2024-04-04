from typing import Union
import yaml
import os
from cff2toml.models.files.metadata_file import MetadataFile, DEFAULT_DIR

DEFAULT_CITATION_CFF_FILENAME: str = 'CITATION.cff'
DEFAULT_CITATION_CFF_FILE_PATH: str = os.path.join(
    DEFAULT_DIR, DEFAULT_CITATION_CFF_FILENAME)


class LoadCffFileException(Exception):
    pass


class SaveCffFileException(Exception):
    pass


class CffFile(MetadataFile):

    def __init__(self, file_path: str = DEFAULT_CITATION_CFF_FILE_PATH):
        self.file_path = file_path
        try:
            with open(self.file_path, 'r') as cff_file:
                self._metadata = yaml.safe_load(cff_file)
        except:
            raise LoadCffFileException(
                f"Cannot load this CFF file: {self.file_path}")

    def save(self, file_path: Union[str, None] = None) -> None:
        if file_path is None:
            file_path = self.file_path
        if self._metadata is not None:
            try:
                with open(file_path, 'w') as cff_file:
                    yaml.safe_dump(self._metadata, cff_file)
            except:
                raise SaveCffFileException(
                    f"Cannot save this CFF file: {file_path}")
        else:
            raise SaveCffFileException(
                f"Cannot save this CFF file: {file_path} because there is no data.")

    @property
    def metadata_version(self):
        return self.get_metadata("version")

    @property
    def metadata_title(self):
        return self.get_metadata("title")

    @property
    def metadata_license(self):
        return self.get_metadata("license")

    @property
    def metadata_abstract(self):
        return self.get_metadata("abstract")

    @property
    def metadata_authors(self):
        return self.get_metadata("authors")

    @property
    def metadata_repository_code(self):
        return self.get_metadata("repository-code")
