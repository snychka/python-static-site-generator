import pytest


@pytest.mark.test_site_path_import_module1
def test_site_path_import_module1(site, get_imports):
    # from pathlib import Path

    success, message, code = site
    assert success, message

    path_import = "Path" in get_imports(code, "pathlib")

    assert path_import, \
        "Have you imported `Path` from `pathlib`?"


@pytest.mark.test_site_class_module1
def test_site_class_module1(site, get_by_name):

    # class Site:
    #     def __init__(self, source, dest):
    #         self.source = Path(source)
    #         self.dest = Path(dest)

    success, message, code = site
    assert success, message

    site_class_exists, site_class = get_by_name(code, "class", "Site")

    assert site_class_exists, \
        "Have you created a class called `Site` in the `site.py` file?"

    init_def_exists, init_def = get_by_name(site_class, "def", "__init__")

    init_def.help()

    assert False


"""
@pytest.mark.test_site_create_dir_function_module1
def test_site_create_dir_function_module1(site):

    # def create_dir(self, path):
    #     directory = self.dest / path.relative_to(self.source)

    success, message, code = site
    assert success, message

    assert False


@pytest.mark.test_site_create_dir_mkdir_module1
def test_site_create_dir_mkdir_module1(site):

    # directory.mkdir(parents=True, exist_ok=True)

    success, message, code = site
    assert success, message

    assert False


@pytest.mark.test_site_build_function_module1
def test_site_build_function_module1(site):

    # def build(self):
    #     self.dest.mkdir(parents=True, exist_ok=True)

    success, message, code = site
    assert success, message

    assert False


@pytest.mark.test_site_path_rglob_module1
def test_site_path_rglob_module1(site):

    # for path in self.source.rglob("*"):
    #     if path.is_dir():
    #         self.create_dir(path)

    success, message, code = site
    assert success, message

    assert False


@pytest.mark.test_ssg_imports_module1
def test_ssg_imports_module1(ssg):

    # import typer

    # from ssg.site import Site

    success, message, code = ssg
    assert success, message

    assert False


@pytest.mark.test_ssg_main_command_module1
def test_ssg_main_command_module1(ssg):

    # def main(source="content", dest="dist"):
    #     config = {
    #         "source": source,
    #         "dest": dest
    #     }

    success, message, code = ssg
    assert success, message

    assert False


@pytest.mark.test_ssg_build_call_module1
def test_ssg_build_call_module1(ssg):

    # Site(**config).build()

    success, message, code = ssg
    assert success, message

    assert False


@pytest.mark.test_ssg_typer_run_module1
def test_ssg_typer_run_module1(ssg):

    # typer.run(main)

    success, message, code = ssg
    assert success, message

    assert False
"""
