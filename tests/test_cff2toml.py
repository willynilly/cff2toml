import pytest
import os
from src.cff2toml.cff2toml import load_cff_object, load_toml_object, CFFObject, TOMLObject, TransformCFFObjectWithTOMLObjectFunction, TransformTOMLObjectWithCFFObjectFunction, update_cff_with_toml, update_toml_with_cff

import tempfile
import shutil
import os


class TempCopiedFile:

    def __init__(self, source_file_path: str):
        self.source_file_path = source_file_path

    def __enter__(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        shutil.copy2(src=self.source_file_path, dst=self.tmp.name)
        return self

    def __exit__(self, *args):
        os.remove(path=self.tmp.name)

    @property
    def file_path(self) -> str:
        if self.tmp.closed:
            return ''
        return self.tmp.name


@pytest.fixture
def dummy_directory_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dummy_files')


@pytest.fixture
def dummy_citation_cff_file_path(dummy_directory_file_path):
    return os.path.join(dummy_directory_file_path, 'dummy_CITATION.cff')


@pytest.fixture
def dummy_pyproject_toml_file_path(dummy_directory_file_path):
    return os.path.join(dummy_directory_file_path, 'dummy_pyproject.toml')


def test_load_cff_object(dummy_citation_cff_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        cff_object: CFFObject = load_cff_object(
            cff_file_path=tmp_dummy_citation_cff_file.file_path)
        assert cff_object['version'] == '0.0.2'
        assert cff_object['title'] == 'sometool'


def test_load_toml_object(dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        toml_object: TOMLObject = load_toml_object(
            toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
        assert toml_object['project']['version'] == '0.0.1'
        assert toml_object['project']['name'] == 'sometool'


def test_update_toml_with_cff(dummy_citation_cff_file_path, dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:

            toml_object: TOMLObject = load_toml_object(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
            assert toml_object['project']['version'] == '0.0.1'
            assert toml_object['project']['name'] == 'sometool'
            assert toml_object['project']['description'] == 'A module that does something.'
            assert toml_object['project']['license'] == 'Apache-2.0'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willnilly/cff2toml'

            def transformer(toml_object: TOMLObject, cff_object: CFFObject) -> TOMLObject:
                toml_object['project']['version'] = '5.0.1'
                toml_object['project']['name'] = 'cows'
                toml_object['project']['description'] = 'A module that does something else.'
                toml_object['project']['license'] = 'MIT'
                toml_object['project']['urls']['Source'] = 'https://github.com/willynilly/somewhereelse'
                return toml_object

            toml_object = update_toml_with_cff(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path,
                cff_file_path=tmp_dummy_citation_cff_file.file_path,
                transform_toml_object_func=transformer)

            assert toml_object['project']['version'] == '5.0.1'
            assert toml_object['project']['name'] == 'cows'
            assert toml_object['project']['description'] == 'A module that does something else.'
            assert toml_object['project']['license'] == 'MIT'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willynilly/somewhereelse'

            toml_object = load_toml_object(
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path)
            assert toml_object['project']['version'] == '5.0.1'
            assert toml_object['project']['name'] == 'cows'
            assert toml_object['project']['description'] == 'A module that does something else.'
            assert toml_object['project']['license'] == 'MIT'
            assert toml_object['project']['urls']['Source'] == 'https://github.com/willynilly/somewhereelse'


def test_update_cff_with_toml(dummy_citation_cff_file_path, dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_citation_cff_file_path) as tmp_dummy_citation_cff_file:
        with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:

            cff_object: CFFObject = load_cff_object(
                cff_file_path=tmp_dummy_citation_cff_file.file_path)
            assert cff_object['version'] == '0.0.2'
            assert cff_object['title'] == 'sometool'
            assert cff_object['license'] == 'Apache-2.0'
            assert cff_object['abstract'] == 'A module that does something.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewhere'

            def transformer(cff_object: CFFObject, toml_object: TOMLObject) -> CFFObject:
                cff_object['version'] = '4.0.0'
                cff_object['title'] = 'sheep'
                cff_object['license'] = 'MIT'
                cff_object['abstract'] = 'A module that does something else.'
                cff_object['repository-code'] = 'https://github.com/willynilly/somewhereelse'

                return cff_object

            cff_object = update_cff_with_toml(
                cff_file_path=tmp_dummy_citation_cff_file.file_path,
                toml_file_path=tmp_dummy_pyproject_toml_file.file_path,
                transform_cff_object_func=transformer)

            assert cff_object['version'] == '4.0.0'
            assert cff_object['title'] == 'sheep'
            assert cff_object['license'] == 'MIT'
            assert cff_object['abstract'] == 'A module that does something else.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewhereelse'

            cff_object = load_cff_object(
                cff_file_path=tmp_dummy_citation_cff_file.file_path)
            assert cff_object['version'] == '4.0.0'
            assert cff_object['title'] == 'sheep'
            assert cff_object['license'] == 'MIT'
            assert cff_object['abstract'] == 'A module that does something else.'
            assert cff_object['repository-code'] == 'https://github.com/willynilly/somewhereelse'
