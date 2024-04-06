from cff2toml.models.files.cff_file import CffFile
from cff2toml.models.files.pyproject_toml_file import PyprojectTomlFile
from cff2toml.models.files.synchronizers.cff_and_pyproject_toml_file_synchronizer import CffAndPyprojectTomlFileSynchronizer
from tests.temp_copied_file import TempCopiedFile


def test_update_cff_with_pyproject_toml_only_deletes_metadata_for_mapped_properties_missing_in_pyproject_toml(dummy_cff_and_pyproject_toml_file_synchronizer):
    cff_file = dummy_cff_and_pyproject_toml_file_synchronizer.cff_file
    pyproject_toml_file = dummy_cff_and_pyproject_toml_file_synchronizer.pyproject_toml_file

    assert cff_file.has_metadata('license') == True
    assert pyproject_toml_file.has_metadata('project.license') == True
    pyproject_toml_file.delete_metadata('project.license')
    assert pyproject_toml_file.has_metadata('project.license') == False

    assert cff_file.has_metadata('version') == True
    assert cff_file.has_metadata('project.version') == False
    assert pyproject_toml_file.has_metadata('version') == False
    assert pyproject_toml_file.has_metadata('project.version') == True
    assert cff_file.metadata_version == '0.0.2'
    assert pyproject_toml_file.metadata_project_version == '0.0.1'

    dummy_cff_and_pyproject_toml_file_synchronizer.update_cff_with_pyproject_toml(
        delete_missing_metadata=True)

    # should remove license from cff since we first remove corresponding
    # mapped project project.license from pyproject_toml
    assert cff_file.has_metadata('license') == False
    assert pyproject_toml_file.has_metadata('project.license') == False

    assert cff_file.has_metadata('version') == True
    assert cff_file.has_metadata('project.version') == False
    assert pyproject_toml_file.has_metadata('version') == False
    assert pyproject_toml_file.has_metadata('project.version') == True
    assert cff_file.metadata_version == '0.0.1'
    assert pyproject_toml_file.metadata_project_version == '0.0.1'


def test_update_pyproject_toml_with_cff_only_deletes_metadata_for_mapped_properties_missing_in_cff(dummy_cff_and_pyproject_toml_file_synchronizer):
    cff_file = dummy_cff_and_pyproject_toml_file_synchronizer.cff_file
    pyproject_toml_file = dummy_cff_and_pyproject_toml_file_synchronizer.pyproject_toml_file

    assert pyproject_toml_file.has_metadata('project.license') == True
    assert cff_file.has_metadata('license') == True
    cff_file.delete_metadata('license')
    assert cff_file.has_metadata('license') == False

    assert pyproject_toml_file.has_metadata('project.version') == True
    assert pyproject_toml_file.has_metadata('version') == False
    assert cff_file.has_metadata('project.version') == False
    assert cff_file.has_metadata('version') == True
    assert pyproject_toml_file.metadata_project_version == '0.0.1'
    assert cff_file.metadata_version == '0.0.2'

    dummy_cff_and_pyproject_toml_file_synchronizer.update_pyproject_toml_with_cff(
        delete_missing_metadata=True)

    # should remove project.license from project_toml since we first remove corresponding
    # mapped project license from cff
    assert pyproject_toml_file.has_metadata('project.license') == False
    assert cff_file.has_metadata('license') == False

    assert pyproject_toml_file.has_metadata('project.version') == True
    assert pyproject_toml_file.has_metadata('version') == False
    assert cff_file.has_metadata('project.version') == False
    assert cff_file.has_metadata('version') == True
    assert pyproject_toml_file.metadata_project_version == '0.0.2'
    assert cff_file.metadata_version == '0.0.2'


def test_save(dummy_cff_and_pyproject_toml_file_synchronizer):
    cff_file = dummy_cff_and_pyproject_toml_file_synchronizer.cff_file
    pyproject_toml_file = dummy_cff_and_pyproject_toml_file_synchronizer.pyproject_toml_file

    assert cff_file.metadata_version == '0.0.2'
    assert pyproject_toml_file.metadata_project_version == '0.0.1'

    dummy_cff_and_pyproject_toml_file_synchronizer.set_version('70.0.0')

    # should change internal representation
    assert cff_file.metadata_version == '70.0.0'
    assert pyproject_toml_file.metadata_project_version == '70.0.0'

    check_cff_file: CffFile = CffFile(file_path=cff_file.file_path)
    check_pyproject_toml_file: PyprojectTomlFile = PyprojectTomlFile(
        file_path=pyproject_toml_file.file_path)

    # should not save
    assert check_cff_file.metadata_version == '0.0.2'
    assert check_pyproject_toml_file.metadata_project_version == '0.0.1'

    dummy_cff_and_pyproject_toml_file_synchronizer.save()

    # should save

    assert cff_file.metadata_version == '70.0.0'
    assert pyproject_toml_file.metadata_project_version == '70.0.0'


def test_set_version(dummy_cff_and_pyproject_toml_file_synchronizer):
    cff_file = dummy_cff_and_pyproject_toml_file_synchronizer.cff_file
    pyproject_toml_file = dummy_cff_and_pyproject_toml_file_synchronizer.pyproject_toml_file

    assert cff_file.metadata_version == '0.0.2'
    assert pyproject_toml_file.metadata_project_version == '0.0.1'

    dummy_cff_and_pyproject_toml_file_synchronizer.set_version('70.0.0')

    # should change internal representation
    assert cff_file.metadata_version == '70.0.0'
    assert pyproject_toml_file.metadata_project_version == '70.0.0'

    check_cff_file: CffFile = CffFile(file_path=cff_file.file_path)
    check_pyproject_toml_file: PyprojectTomlFile = PyprojectTomlFile(
        file_path=pyproject_toml_file.file_path)

    # should not save
    assert check_cff_file.metadata_version == '0.0.2'
    assert check_pyproject_toml_file.metadata_project_version == '0.0.1'


def test_set_description(dummy_cff_and_pyproject_toml_file_synchronizer):
    cff_file = dummy_cff_and_pyproject_toml_file_synchronizer.cff_file
    pyproject_toml_file = dummy_cff_and_pyproject_toml_file_synchronizer.pyproject_toml_file

    assert cff_file.metadata_abstract == 'A module that does something cool.'
    assert pyproject_toml_file.metadata_project_description == 'A module that does something uncool.'

    dummy_cff_and_pyproject_toml_file_synchronizer.set_description(
        'A module that does something cooler.')

    # should change internal representation
    assert cff_file.metadata_abstract == 'A module that does something cooler.'
    assert pyproject_toml_file.metadata_project_description == 'A module that does something cooler.'

    check_cff_file: CffFile = CffFile(file_path=cff_file.file_path)
    check_pyproject_toml_file: PyprojectTomlFile = PyprojectTomlFile(
        file_path=pyproject_toml_file.file_path)

    # should not save
    assert check_cff_file.metadata_abstract == 'A module that does something cool.'
    assert check_pyproject_toml_file.metadata_project_description == 'A module that does something uncool.'


def test_set_code_repository_url(dummy_cff_and_pyproject_toml_file_synchronizer):
    cff_file = dummy_cff_and_pyproject_toml_file_synchronizer.cff_file
    pyproject_toml_file = dummy_cff_and_pyproject_toml_file_synchronizer.pyproject_toml_file

    assert cff_file.metadata_repository_code == 'https://github.com/willynilly/somewherecool'
    assert pyproject_toml_file.metadata_project_urls_source == 'https://github.com/willynilly/somewhereuncool'

    dummy_cff_and_pyproject_toml_file_synchronizer.set_code_repository_url(
        'https://github.com/willynilly/somewherecooler')

    # should change internal representation
    assert cff_file.metadata_repository_code == 'https://github.com/willynilly/somewherecooler'
    assert pyproject_toml_file.metadata_project_urls_source == 'https://github.com/willynilly/somewherecooler'

    check_cff_file: CffFile = CffFile(file_path=cff_file.file_path)
    check_pyproject_toml_file: PyprojectTomlFile = PyprojectTomlFile(
        file_path=pyproject_toml_file.file_path)

    # should not save
    assert check_cff_file.metadata_repository_code == 'https://github.com/willynilly/somewherecool'
    assert check_pyproject_toml_file.metadata_project_urls_source == 'https://github.com/willynilly/somewhereuncool'


def test_set_license(dummy_cff_and_pyproject_toml_file_synchronizer):
    cff_file = dummy_cff_and_pyproject_toml_file_synchronizer.cff_file
    pyproject_toml_file = dummy_cff_and_pyproject_toml_file_synchronizer.pyproject_toml_file

    assert cff_file.metadata_license == 'Apache-2.0'
    assert pyproject_toml_file.metadata_project_license == 'Apache-1.0'

    dummy_cff_and_pyproject_toml_file_synchronizer.set_license('MIT')

    # should change internal representation
    assert cff_file.metadata_license == 'MIT'
    assert pyproject_toml_file.metadata_project_license == 'MIT'

    check_cff_file: CffFile = CffFile(file_path=cff_file.file_path)
    check_pyproject_toml_file: PyprojectTomlFile = PyprojectTomlFile(
        file_path=pyproject_toml_file.file_path)

    # should not save
    assert check_cff_file.metadata_license == 'Apache-2.0'
    assert check_pyproject_toml_file.metadata_project_license == 'Apache-1.0'


def test_set_title(dummy_cff_and_pyproject_toml_file_synchronizer):
    cff_file = dummy_cff_and_pyproject_toml_file_synchronizer.cff_file
    pyproject_toml_file = dummy_cff_and_pyproject_toml_file_synchronizer.pyproject_toml_file

    assert cff_file.metadata_title == 'somecooltool'
    assert pyproject_toml_file.metadata_project_name == 'someuncooltool'

    dummy_cff_and_pyproject_toml_file_synchronizer.set_title('somecoolertool')

    # should change internal representation
    assert cff_file.metadata_title == 'somecoolertool'
    assert pyproject_toml_file.metadata_project_name == 'somecoolertool'

    check_cff_file: CffFile = CffFile(file_path=cff_file.file_path)
    check_pyproject_toml_file: PyprojectTomlFile = PyprojectTomlFile(
        file_path=pyproject_toml_file.file_path)

    # should not save
    assert check_cff_file.metadata_title == 'somecooltool'
    assert check_pyproject_toml_file.metadata_project_name == 'someuncooltool'


def test_set_authors():
    assert False
