from typing import Any, Dict, Union

from cff2toml.models.agents.authors.cff_author import CffAuthor
from cff2toml.models.agents.authors.pyproject_toml_author import PyprojectTomlAuthor
from cff2toml.models.agents.people.human_name import HumanName

CffAuthorData = Dict[str, Any]
PyprojectTomlAuthorData = Dict[str, Any]

Author = Union[CffAuthor, PyprojectTomlAuthor]


class CffAndPyprojectTomlAuthorSynchronizer():

    # https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md#how-to-deal-with-unknown-individual-authors
    @staticmethod
    def to_valid_cff_author(author: Author) -> CffAuthor:
        if isinstance(author, CffAuthor):
            author = author.model_copy(deep=True)
            if author.is_person:
                if not author.person.given_names and not author.person.family_names:
                    author.is_person = False
                    author.entity.name = "anonymous"
                    author.entity.email = author.person.email
                    author.entity.orcid = author.person.orcid
                    author.entity.address = author.person.address
                    author.entity.city = author.person.city
                    author.entity.alias = author.person.alias
                    author.entity.country = author.person.country
                    author.entity.fax = author.person.fax
                    author.entity.post_code = author.person.post_code
                    author.entity.region = author.person.region
                    author.entity.tel = author.person.tel
                    author.entity.website = author.person.website
            return author
        elif isinstance(author, PyprojectTomlAuthor):
            name: HumanName = HumanName()
            name.full_name = author.name

            cff_author: CffAuthor = CffAuthor()
            if not name.first_name and not name.last_name:
                cff_author.is_person = False
                cff_author.entity.name = "anonymous"
                if author.email:
                    cff_author.entity.email = author.email
            else:
                cff_author.is_person = True
                if name.first_name:
                    if name.middle_name:
                        cff_author.person.given_names = name.first_name + ' ' + name.middle_name
                    else:
                        cff_author.person.given_names = name.first_name
                if name.particle:
                    cff_author.person.name_particle = name.particle
                if name.last_name:
                    cff_author.person.family_names = name.last_name
                if name.suffix:
                    cff_author.person.name_suffix = name.suffix
                if author.email:
                    cff_author.person.email = author.email

            return cff_author
        else:
            raise TypeError(
                "Cannot convert to CFF author. Should be an instance of CffAuthor or PyprojcetTomlAuthor.")

    @staticmethod
    def to_cff_author_data(author: Author) -> CffAuthorData:
        author = CffAndPyprojectTomlAuthorSynchronizer.to_valid_cff_author(
            author)
        if isinstance(author, CffAuthor):
            if author.is_person:
                return author.person.model_dump(mode="json", exclude_defaults=True, by_alias=True)
            else:
                return author.entity.model_dump(mode="json", exclude_defaults=True, by_alias=True)
        else:
            raise TypeError(
                "Cannot convert to CFF author data. Should be an instance of CffAuthor or PyprojcetTomlAuthor.")

    @staticmethod
    def to_valid_pyproject_toml_author(author: Author) -> PyprojectTomlAuthor:
        if isinstance(author, PyprojectTomlAuthor):
            return author
        elif isinstance(author, CffAuthor):
            pyproject_toml_author: PyprojectTomlAuthor = PyprojectTomlAuthor()
            if author.is_person:
                pyproject_toml_author.name = ' '.join(
                    [author.person.given_names, author.person.name_particle, author.person.family_names, author.person.name_suffix])
                pyproject_toml_author.email = author.person.email
            else:
                pyproject_toml_author.name = author.entity.name
            return pyproject_toml_author
        else:
            raise TypeError(
                "Cannot convert to PyprojectToml author. Should be an instance of CffAuthor or PyprojcetTomlAuthor.")

    @staticmethod
    def to_pyproject_toml_author_data(author: Author) -> PyprojectTomlAuthorData:
        if isinstance(author, CffAuthor):
            author = CffAndPyprojectTomlAuthorSynchronizer.to_valid_pyproject_toml_author(
                author)
        if isinstance(author, PyprojectTomlAuthor):
            return author.model_dump(mode="json", exclude_defaults=True, by_alias=True)
        else:
            raise TypeError(
                "Cannot convert to Pyproject TOML data. Should be an instance of CffAuthor or PyprojcetTomlAuthor.")
