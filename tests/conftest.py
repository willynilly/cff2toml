import pytest
import os

from cff2toml.models.agents.authors.cff_author import CffAuthor
from cff2toml.models.agents.authors.pyproject_toml_author import PyprojectTomlAuthor
from cff2toml.models.files.cff_file import CffFile
from cff2toml.models.files.pyproject_toml_file import PyprojectTomlFile
from cff2toml.models.files.synchronizers.cff_and_pyproject_toml_file_synchronizer import CffAndPyprojectTomlFileSynchronizer
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


@pytest.fixture
def dummy_cff_and_pyproject_toml_file_synchronizer(dummy_cff_file, dummy_pyproject_toml_file):
    synchronizer = CffAndPyprojectTomlFileSynchronizer(
        cff_file=dummy_cff_file, pyproject_toml_file=dummy_pyproject_toml_file)
    return synchronizer


@pytest.fixture
def dummy_cff_author_person():
    author = CffAuthor()
    author.is_person = True
    author.person.given_names = 'Billy Bob'
    author.person.family_names = 'Longshot'
    author.person.name_particle = 'de'
    author.person.name_suffix = 'VIII'
    author.person.email = 'longshot@somewherecool.nl'
    author.person.orcid = 'someorcidid'
    author.person.affiliation = 'Cool University'
    return author


@pytest.fixture
def dummy_cff_author_organization():
    author = CffAuthor()
    author.is_person = False
    author.entity.name = 'Cool Company'
    author.entity.email = 'coolcompany@somewherecool.nl'
    author.entity.orcid = 'coolcompanyorcid'
    return author


@pytest.fixture
def dummy_pyproject_author_person():
    author = PyprojectTomlAuthor()
    author.name = 'Penelope Cheddar van Gouda X'
    author.email = 'cheesefan@somewherecool.nl'
    return author


@pytest.fixture
def dummy_pyproject_author_organization():
    author = PyprojectTomlAuthor()
    author.name = 'Some Company'
    author.email = 'somecompany@somewherecool.nl'
    return author
