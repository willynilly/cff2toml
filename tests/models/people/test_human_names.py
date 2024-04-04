
from cff2toml.models.people.human_names import is_human_name, parse_human_name


def test_is_human_name_for_empty_name():
    assert is_human_name('') == False


def test_parse_human_name():

    human_names_to_parts = {
        'Bob Smith Jr': ('Bob', '', '', 'Smith', 'Jr'),
        'Bob Smith Jr.': ('Bob', '', '', 'Smith', 'Jr.'),
        'Bob Dave Smith Jr.': ('Bob', 'Dave', '', 'Smith', 'Jr.'),
        'Sally Lou May': ('Sally', 'Lou', '', 'May', ''),
        'Sally Elizabeth Lou May': ('Sally', 'Elizabeth Lou', '', 'May', ''),
        'Sally Lou van May': ('Sally', 'Lou', 'van', 'May', ''),
        'Alicia de Francisco': ('Alicia', '', 'de', 'Francisco', ''),
        'Adam van het Francisco IV': ('Adam', '', 'van het', 'Francisco', 'IV'),
        'Tony': ('Tony', '', '', '', ''),
        'Tony Li': ('Tony', '', '', 'Li', ''),
        'Tony X': ('Tony', '', '', 'X', ''),
    }

    for human_name, (expected_first_name, expected_middle_name, expected_particle, expected_last_name, expected_suffix) in human_names_to_parts.items():
        first_name, middle_name, particle, last_name, suffix = parse_human_name(
            human_name=human_name)
        assert first_name == expected_first_name
        assert middle_name == expected_middle_name
        assert particle == expected_particle
        assert last_name == expected_last_name
        assert suffix == expected_suffix
