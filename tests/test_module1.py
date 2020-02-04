import pytest
from redbaron import RedBaron

@pytest.mark.test_site_path_import_module1
def test_site_path_import_module1(site, get_imports):
    # from pathlib import Path

    assert site["success"], \
        site["message"]

    path_import = "Path" in get_imports(site["code"], "pathlib")

    assert path_import, \
        ""

    assert False

@pytest.mark.test_site_class_module1
def test_site_class_module1():
    # class Site:
    #     def __init__(self, source, dest):
    #         self.source = Path(source)
    #         self.dest = Path(dest)

    pass


@pytest.mark.test_site_create_dir_function_module1
def test_create_dir_function_module1():
    # def create_dir(self, path):
    #     directory = self.dest / path.relative_to(self.source)

    pass


@pytest.mark.test_site_create_dir_mkdir_module1
def test_create_dir_mkdir_module1():
    # directory.mkdir(parents=True, exist_ok=True)

    pass


@pytest.mark.test_site_build_function_module1
def test_build_function_module1():
    # def build(self):
    #     self.dest.mkdir(parents=True, exist_ok=True)

    pass


@pytest.mark.test_site_path_rglob_module1
def test_path_rglob_module1():
    # for path in self.source.rglob("*"):
    #     if path.is_dir():
    #         self.create_dir(path)

    pass


@pytest.mark.test_ssg_imports_module1
def test_imports_module1():
    # import typer
    #
    # from ssg.site import Site

    pass


@pytest.mark.test_ssg_main_command_module1
def test_main_command_module1():
    # def main(source="content", dest="dist"):
    #     config = {
    #         "source": source,
    #         "dest": dest
    #     }

    pass


@pytest.mark.test_ssg_build_call_module1
def test_build_call_module1():
    # Site(**config).build()

    pass


@pytest.mark.test_ssg_typer_run_module1
def test_typer_run_module1():
    # typer.run(main)

    pass
