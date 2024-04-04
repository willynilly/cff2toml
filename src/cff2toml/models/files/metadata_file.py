from typing import Any, Dict, Mapping, Union

import pydash

Metadata = Mapping[str, Any]

DEFAULT_DIR: str = '.'


class MetadataFile:

    _metadata: Metadata = {}
    file_path: str = ''

    def get_metadata(self, property_path: str) -> Any:
        return pydash.objects.get(
            obj=self._metadata, path=property_path)

    def set_metadata(self, property_path: str, value: Any) -> None:
        self._metadata = pydash.objects.set_(
            obj=self._metadata, path=property_path, value=value)

    def delete_metadata(self, property_path: str) -> None:
        if self._metadata is not None:
            data_as_dict: Dict = dict(self._metadata)
            pydash.objects.unset(obj=data_as_dict, path=property_path)
            self._metadata = data_as_dict

    def has_metadata(self, property_path: str) -> bool:
        if self._metadata is None:
            return False
        else:
            return pydash.objects.has(self._metadata, path=property_path)
