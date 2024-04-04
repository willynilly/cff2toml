from typing import Any, Dict

from cff2toml.models.people.person import Person

CffAuthorData = Dict[str, Any]
PyprojectTomlAuthorData = Dict[str, Any]


class Author(Person):
    # https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md#how-to-deal-with-unknown-individual-authors
    def to_cff_data(self) -> CffAuthorData:
        data: CffAuthorData = {}
        if self.first_name:
            if self.middle_name:
                given_names = self.first_name + ' ' + self.middle_name
            else:
                given_names = self.first_name
            data['given-names'] = given_names
        if self.particle:
            data['name-particle'] = self.particle
        if self.last_name:
            data['family-names'] = self.last_name
        if self.suffix:
            data['name-suffix'] = self.suffix
        if 'given-names' not in data and 'family-names' not in data:
            data = {'name': 'anonymous'}
        return data

    def to_pyproject_toml_data(self) -> PyprojectTomlAuthorData:
        data: PyprojectTomlAuthorData = {}
        if len(self.name):
            if self.is_human_name():
                data['name'] = self.full_name
            else:
                data['name'] = self.name
        else:
            data['name'] = 'anonymous'
        if len(self.email):
            data['email'] = self.email
        return data
