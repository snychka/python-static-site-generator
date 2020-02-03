import pytest


@pytest.mark.test_path_import_module1
def test_path_import_module1(get_source_code):
    # from pathlib import Path
    pass


@pytest.mark.test_site_class_module1
def test_site_class_module1():
    # class Site:
    #     def __init__(self, source, dest):
    #         self.source = Path(source)
    #         self.dest = Path(dest)path_import
    pass


@pytest.mark.test_create_dir_function_module1
def test_create_dir_function_module1():
    # def create_dir(self, path):
    #     directory = self.dest / path.relative_to(self.source)
    pass


@pytest.mark.test_create_dir_mkdir_module1
def test_create_dir_mkdir_module1():
    # directory.mkdir(parents=True, exist_ok=True)
    pass


@pytest.mark.test_build_function_module1
def test_build_function_module1():
    # def build(self):
    #     self.dest.mkdir(parents=True, exist_ok=True)
    pass


@pytest.mark.test_path_rglob_module1
def test_path_rglob_module1():
    # for path in self.source.rglob("*"):
    #     if path.is_dir():
    #         self.create_dir(path)
    pass


@pytest.mark.test_imports_module1
def test_imports_module1():
    # import typer
    #
    # from ssg.site import Site
    pass


@pytest.mark.test_main_command_module1
def test_main_command_module1():
    # def main(source="content", dest="dist"):
    #     config = {
    #         "source": source,
    #         "dest": dest
    #     }
    pass


@pytest.mark.test_build_call_module1
def test_build_call_module1():
    # Site(**config).build()
    pass


@pytest.mark.test_typer_run_module1
def test_typer_run_module1():
    # typer.run(main)
    pass
