from dataclasses import dataclass

import cff2toml.models.people.human_names as hn


@dataclass
class Person:
    _name: str
    first_name: str
    middle_name: str
    particle: str  # e.g., von, de los
    last_name: str
    suffix: str
    title: str  # e.g., Dr. or Mr. or Mrs.
    email: str

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.strip()
        first_name, middle_name, particle, last_name, suffix = hn.parse_human_name(
            self._name)
        self.first_name = first_name if first_name else ''
        self.middle_name = middle_name if middle_name else ''
        self.last_name = last_name if last_name else ''
        self.particle = particle if particle else ''
        self.suffix = suffix if suffix else ''

    @property
    def full_name(self):
        return ' '.join([self.title, self.first_name, self.middle_name, self.last_name, self.suffix])

    def is_human_name(self):
        return hn.is_human_name(self.name)
