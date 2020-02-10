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

    site_class = site.get_by_name("class", "Site")

    assert site_class.exists, \
        "Have you created a class called `Site` in the `site.py` file?"

    init_def = site.get_by_name("def", "__init__", site_class.code)

    assert init_def.exists, \
        "Does the class `Site` have an `__init__` method?"

    self_arg = site.get_by_value("def_argument", "self", init_def.code)
    source_arg = site.get_by_value("def_argument", "source", init_def.code)
    dest_arg = site.get_by_value("def_argument", "dest", init_def.code)

    assert self_arg.exists, \
        "Does the `__init__` method have a `self` argument?"

    assert source_arg.exists, \
        "Does the `__init__` method have a `source` argument?"

    assert dest_arg.exists, \
        "Does the `__init__` method have a `dest` argument?"

    self_source = site.get_by_value("assignment", "self.source", init_def.code)
    self_dest = site.get_by_value("assignment", "self.dest", init_def.code)

    assert self_source.exists, \
        "Are you assigning the correct value to `self.source`?"

    assert self_dest.exists, \
        "Are you assigning the correct value to `self.dest`?"

    path_source_call = self_source.code.find_all("atomtrailers", lambda node: \
        node.find("name", lambda node: node.value == "Path" and \
        node.next_intuitive.find("name", value="source")))[0]

    path_source_call_exists = path_source_call is not None
    assert path_source_call_exists, \
        "Are you assigning `self.source` a call to `Path()` passing in `source`?"

    path_dest_call = self_dest.code.find_all("atomtrailers", lambda node: \
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

    site_class = site.get_by_name("class", "Site")

    assert site_class.exists, \
        "Have you created a class called `Site` in the `site.py` file?"

    create_dir = site.get_by_name("def", "create_dir", site_class.code)

    self_arg = site.get_by_value("def_argument", "self", create_dir.code)
    path_arg = site.get_by_value("def_argument", "path", create_dir.code)

    assert self_arg.exists, \
        "Does the `create_dir` method have a `self` argument?"

    assert path_arg.exists, \
        "Does the `create_dir` method have a `path` argument?"

    directory = site.get_by_value("assignment", "directory", create_dir.code)

    assert directory.exists, \
        "Are you assigning the correct value to `directory`?"

    directory_path = directory.code.find_all("binary_operator", value="/")
    directory_path_exists = len(directory_path) == 1

    assert directory_path_exists, \
        "Are you assigning the correct path to `directory`?"

    first = directory_path[0].first

    first_exist = str(first) == "self.dest"
    assert first_exist, \
        "Are you assigning the correct path to `directory`? The first part of the path should be `self.dest`."

    second = directory_path[0].second
    second_exist = second[0].value == "path" and second[1].value == "relative_to"

    assert second_exist, \
        "Are you assigning the correct path to `directory`? The second part path should be a call to `path.relative_to()`."

    call_argument_exists = len(second.find_all("call_argument")) == 1 and str(second.find_all("call_argument")[0]) == "self.source"

    assert call_argument_exists, \
        "Are you passing `self.source` to `path.relative_to()`?"



@pytest.mark.test_site_create_dir_mkdir_module1
def test_site_create_dir_mkdir_module1(parse):

    # directory.mkdir(parents=True, exist_ok=True)

    site = parse('site')
    assert site.success, site.message

    assert False


"""
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
