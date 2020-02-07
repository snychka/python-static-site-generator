import pytest


@pytest.mark.test_site_path_import_module1
def test_site_path_import_module1(parse):
    # from pathlib import Path

    site = parse('site')
    assert site.success, site.message

    path_import = "Path" in site.get_imports("pathlib")
    assert path_import, \
        "Have you imported `Path` from `pathlib`?"


@pytest.mark.test_site_class_module1
def test_site_class_module1(parse):

    # class Site:
    #     def __init__(self, source, dest):
    #         self.source = Path(source)
    #         self.dest = Path(dest)

    site = parse('site')
    assert site.success, site.message

    site_class_exists, site_class = site.get_by_name("class", "Site")

    assert site_class_exists, \
        "Have you created a class called `Site` in the `site.py` file?"

    init_def_exists, init_def = site.get_by_name("def", "__init__", site_class)

    assert init_def_exists, \
        "Does the class `Site` have an `__init__` method?"

    self_arg, _ = site.get_by_value("def_argument", "self", init_def)
    source_arg, _ = site.get_by_value("def_argument", "source", init_def)
    dest_arg, _ = site.get_by_value("def_argument", "dest", init_def)

    assert self_arg, \
        "Does the `__init__` method have a `self` argument?"

    assert source_arg, \
        "Does the `__init__` method have a `source` argument?"

    assert dest_arg, \
        "Does the `__init__` method have a `dest` argument?"

    self_source_exists, self_source = site.get_by_value("assignment", "self.source", init_def)
    self_dest_exists, self_dest = site.get_by_value("assignment", "self.dest", init_def)

    assert self_source_exists, \
        "Are you assigning `self.source`?"

    assert self_dest_exists, \
        "Are you assigning `self.dest`?"

    path_source_call = self_source.find_all("atomtrailers", lambda node: \
        node.find("name", lambda node: node.value == "Path" and \
        node.next_intuitive.find("name", value="source")))[0]

    path_source_call_exists = path_source_call is not None
    assert path_source_call_exists, \
        "Are you assigning `self.source` a call to `Path()` passing in `source`?"

    path_dest_call = self_dest.find_all("atomtrailers", lambda node: \
        node.find("name", lambda node: node.value == "Path" and \
        node.next_intuitive.find("name", value="dest")))[0]

    path_dest_call_exists = path_dest_call is not None
    assert path_dest_call_exists, \
        "Are you assigning `self.dest` a call to `Path()` passing in `dest`?"


@pytest.mark.test_site_create_dir_function_module1
def test_site_create_dir_function_module1(parse):

    # def create_dir(self, path):
    #     directory = self.dest / path.relative_to(self.source)

    site = parse('site')
    assert site.success, site.message

    assert False


"""
@pytest.mark.test_site_create_dir_mkdir_module1
def test_site_create_dir_mkdir_module1(parse):

    # directory.mkdir(parents=True, exist_ok=True)

    site = parse('site')
    assert site.success, site.message

    assert False


@pytest.mark.test_site_build_function_module1
def test_site_build_function_module1(parse):

    # def build(self):
    #     self.dest.mkdir(parents=True, exist_ok=True)

    site = parse('site')
    assert site.success, site.message

    assert False


@pytest.mark.test_site_path_rglob_module1
def test_site_path_rglob_module1(parse):

    # for path in self.source.rglob("*"):
    #     if path.is_dir():
    #         self.create_dir(path)

    site = parse('site')
    assert site.success, site.message

    assert False


@pytest.mark.test_ssg_imports_module1
def test_ssg_imports_module1(parse):

    # import typer

    # from ssg.site import Site

    ssg = parse('ssg')
    assert ssg.success, ssg.message

    assert False


@pytest.mark.test_ssg_main_command_module1
def test_ssg_main_command_module1(parse):

    # def main(source="content", dest="dist"):
    #     config = {
    #         "source": source,
    #         "dest": dest
    #     }

    ssg = parse('ssg')
    assert ssg.success, ssg.message

    assert False


@pytest.mark.test_ssg_build_call_module1
def test_ssg_build_call_module1(parse):

    # Site(**config).build()

    ssg = parse('ssg')
    assert ssg.success, ssg.message

    assert False


@pytest.mark.test_ssg_typer_run_module1
def test_ssg_typer_run_module1(parse):

    # typer.run(main)

    ssg = parse('ssg')
    assert ssg.success, ssg.message

    assert False
"""
