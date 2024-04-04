import pytest
import os

from cff2toml.models.files.cff_file import CffFile
from cff2toml.models.files.pyproject_toml_file import PyprojectTomlFile
from tests.temp_copied_file import TempCopiedFile


@pytest.fixture
def dummy_directory_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dummy_files')


@pytest.fixture
def dummy_cff_file_path(dummy_directory_file_path):
    return os.path.join(dummy_directory_file_path, 'dummy_CITATION.cff')


@pytest.fixture
def dummy_pyproject_toml_file_path(dummy_directory_file_path):
    return os.path.join(dummy_directory_file_path, 'dummy_pyproject.toml')


@pytest.fixture
def dummy_cff_file(dummy_cff_file_path):
    with TempCopiedFile(source_file_path=dummy_cff_file_path) as tmp_dummy_cff_file:
        cff_file: CffFile = CffFile(
            file_path=tmp_dummy_cff_file.file_path)
        yield cff_file


@pytest.fixture
def dummy_pyproject_toml_file(dummy_pyproject_toml_file_path):
    with TempCopiedFile(source_file_path=dummy_pyproject_toml_file_path) as tmp_dummy_pyproject_toml_file:
        pyproject_toml_file: PyprojectTomlFile = PyprojectTomlFile(
            file_path=tmp_dummy_pyproject_toml_file.file_path)
        yield pyproject_toml_file
