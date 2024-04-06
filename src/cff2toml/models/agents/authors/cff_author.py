from cff2toml.models.agents.organizations.cff_entity import CffEntity
from cff2toml.models.agents.people.cff_person import CffPerson
from cff2toml.models.basic_model import BasicModel


class CffAuthor(BasicModel):
    person: CffPerson = CffPerson()
    entity: CffEntity = CffEntity()
    is_person: bool = True
