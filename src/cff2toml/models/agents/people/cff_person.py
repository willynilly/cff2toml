from cff2toml.models.basic_model import BasicModel


class CffPerson(BasicModel):
    # CFF definitions.person
    # https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md#definitionsperson

    address: str = ''
    affiliation: str = ''
    alias: str = ''
    city: str = ''
    country: str = ''
    email: str = ''
    family_names: str = ''
    fax: str = ''
    given_names: str = ''
    name_particle: str = ''
    name_suffix: str = ''
    orcid: str = ''
    post_code: str = ''
    region: str = ''
    tel: str = ''
    website: str = ''
