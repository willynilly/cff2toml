from typing import OrderedDict

import pytest
from cff2toml.models.files.toml_file import TomlFile
from tests.temp_copied_file import TempCopiedFile


@pytest.fixture
def expected_top_level_pyproject_toml_file_metadata_ordered_keys():
    return ['build-system', 'project']


@pytest.fixture
def expected_second_level_pyproject_toml_file_metadata_ordered_keys():
    return {
        'build-system': ['requires', 'build-backend'],
        'project':
            ['name',
             'version',
             'description',
             'readme',
             'requires-python',
             'license',
             'keywords',
             'authors',
             'classifiers',
             'dependencies',
             'urls',
             'optional-dependencies']}


def test_load_toml_file_loads_metadata_values(dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        toml_file = TomlFile(file_path=tmp_dummy_pyproject_toml_file.file_path)
        assert toml_file.get_metadata('project.version') == '0.0.1'
        assert toml_file.get_metadata('project.name') == 'someuncooltool'
        assert toml_file.get_metadata(
            'project.description') == 'A module that does something uncool.'
        assert toml_file.get_metadata('project.license') == 'Apache-1.0'
        assert toml_file.get_metadata(
            'project.urls.Source') == 'https://github.com/willynilly/somewhereuncool'


def test_load_toml_file_preserves_metadata_order(dummy_pyproject_toml_file_path, expected_top_level_pyproject_toml_file_metadata_ordered_keys, expected_second_level_pyproject_toml_file_metadata_ordered_keys):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        toml_file = TomlFile(file_path=tmp_dummy_pyproject_toml_file.file_path)

        ordered_metadata: OrderedDict = OrderedDict(
            toml_file.metadata.to_dict())

        top_level_ordered_keys: list[str] = list(
            ordered_metadata.keys())
        assert top_level_ordered_keys == expected_top_level_pyproject_toml_file_metadata_ordered_keys

        assert list(ordered_metadata['build-system'].keys(
        )) == expected_second_level_pyproject_toml_file_metadata_ordered_keys['build-system']

        assert list(ordered_metadata['project'].keys(
        )) == expected_second_level_pyproject_toml_file_metadata_ordered_keys['project']


def test_save_toml_file(dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        toml_file: TomlFile = TomlFile(
            file_path=tmp_dummy_pyproject_toml_file.file_path)
        assert toml_file.get_metadata('project.version') == '0.0.1'
        assert toml_file.get_metadata('project.name') == 'someuncooltool'
        assert toml_file.get_metadata(
            'project.description') == 'A module that does something uncool.'
        assert toml_file.get_metadata('project.license') == 'Apache-1.0'
        assert toml_file.get_metadata(
            'project.urls.Source') == 'https://github.com/willynilly/somewhereuncool'
        assert toml_file.has_metadata('project.license') == True
        assert toml_file.has_metadata('wolves.live.in.the.forest') == False
        assert toml_file.has_metadata(
            'wolves.average_weight') == False

        toml_file.delete_metadata('project.license')
        toml_file.set_metadata('project.version', '100.0.1')
        toml_file.set_metadata('project.urls.Source', 'https://somewhere')
        toml_file.set_metadata('wolves.live.in.the.forest', 'yes')
        toml_file.set_metadata(
            'wolves.average_weight', 4.5)

        toml_file.save()

        after_save_toml_file: TomlFile = TomlFile(
            file_path=tmp_dummy_pyproject_toml_file.file_path)
        assert after_save_toml_file.has_metadata('project.license') == False
        assert after_save_toml_file.get_metadata(
            'project.version') == '100.0.1'
        assert after_save_toml_file.get_metadata(
            'project.name') == 'someuncooltool'
        assert after_save_toml_file.get_metadata(
            'project.description') == 'A module that does something uncool.'
        assert after_save_toml_file.get_metadata(
            'project.urls.Source') == 'https://somewhere'
        assert after_save_toml_file.get_metadata(
            'wolves.live.in.the.forest') == 'yes'
        assert after_save_toml_file.get_metadata(
            'wolves.average_weight') == 4.5


def test_save_toml_file_preserves_metadata_order_after_set_existing_metadata(dummy_pyproject_toml_file_path, expected_top_level_pyproject_toml_file_metadata_ordered_keys, expected_second_level_pyproject_toml_file_metadata_ordered_keys):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        toml_file: TomlFile = TomlFile(
            file_path=tmp_dummy_pyproject_toml_file.file_path)

        before_ordered_metadata: OrderedDict = OrderedDict(
            toml_file.metadata.to_dict())

        before_top_level_ordered_keys: list[str] = list(
            before_ordered_metadata.keys())
        assert before_top_level_ordered_keys == expected_top_level_pyproject_toml_file_metadata_ordered_keys

        assert list(before_ordered_metadata['build-system'].keys(
        )) == expected_second_level_pyproject_toml_file_metadata_ordered_keys['build-system']

        assert list(before_ordered_metadata['project'].keys(
        )) == expected_second_level_pyproject_toml_file_metadata_ordered_keys['project']

        toml_file.set_metadata('project.license', 'MIT')

        toml_file.save()

        after_save_toml_file: TomlFile = TomlFile(
            file_path=tmp_dummy_pyproject_toml_file.file_path)

        after_ordered_metadata: OrderedDict = OrderedDict(
            after_save_toml_file.metadata.to_dict())

        after_top_level_ordered_keys: list[str] = list(
            after_ordered_metadata.keys())
        assert after_top_level_ordered_keys == expected_top_level_pyproject_toml_file_metadata_ordered_keys

        assert list(after_ordered_metadata['build-system'].keys(
        )) == expected_second_level_pyproject_toml_file_metadata_ordered_keys['build-system']

        assert list(after_ordered_metadata['project'].keys(
        )) == expected_second_level_pyproject_toml_file_metadata_ordered_keys['project']
