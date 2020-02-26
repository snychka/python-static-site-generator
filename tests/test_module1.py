import re
import pytest


@pytest.mark.test_site_path_import_module1
def test_site_path_import_module1(parse):
    # from pathlib import Path

    site = parse("site")
    assert site.success, site.message

    path_import = "Path" in site.get_from_import("pathlib")
    assert path_import, "Have you imported `Path` from `pathlib`?"


@pytest.mark.test_site_class_module1
def test_site_class_module1(parse):

    # class Site:
    #     def __init__(self, source, dest):
    #         self.source = Path(source)
    #         self.dest = Path(dest)

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    init_def = site.get_by_name("def", "__init__", site_class.code)
    assert init_def.exists, "Does the class `Site` have an `__init__` method?"

    self_arg = site.get_by_value("def_argument", "self", init_def.code)
    assert self_arg.exists, "Does the `__init__` method have a `self` argument?"

    source_arg = site.get_by_value("def_argument", "source", init_def.code)
    assert source_arg.exists, "Does the `__init__` method have a `source` argument?"

    dest_arg = site.get_by_value("def_argument", "dest", init_def.code)
    assert dest_arg.exists, "Does the `__init__` method have a `dest` argument?"

    self_source = site.get_by_value("assignment", "self.source", init_def.code)
    assert self_source.exists, "Are you assigning the correct value to `self.source`?"

    self_dest = site.get_by_value("assignment", "self.dest", init_def.code)
    assert self_dest.exists, "Are you assigning the correct value to `self.dest`?"

    path_source_call = self_source.code.find_all(
        "atomtrailers",
        lambda node: node.find(
            "name",
            lambda node: node.value == "Path"
            and node.next_intuitive.find("name", value="source"),
        ),
    )[0]
    path_source_call_exists = path_source_call is not None
    assert (
        path_source_call_exists
    ), "Are you assigning `self.source` a call to `Path()` passing in `source`?"

    path_dest_call = self_dest.code.find_all(
        "atomtrailers",
        lambda node: node.find(
            "name",
            lambda node: node.value == "Path"
            and node.next_intuitive.find("name", value="dest"),
        ),
    )[0]
    path_dest_call_exists = path_dest_call is not None
    assert (
        path_dest_call_exists
    ), "Are you assigning `self.dest` a call to `Path()` passing in `dest`?"


@pytest.mark.test_site_create_dir_function_module1
def test_site_create_dir_function_module1(parse):

    # def create_dir(self, path):
    #     directory = self.dest / path.relative_to(self.source)

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    create_dir = site.get_by_name("def", "create_dir", site_class.code)

    assert (
        create_dir.exists
    ), "Have you created a method called `create_dir` in the `Site` class?"

    self_arg = site.get_by_value("def_argument", "self", create_dir.code)
    assert self_arg.exists, "Does the `create_dir` method have a `self` argument?"

    path_arg = site.get_by_value("def_argument", "path", create_dir.code)
    assert path_arg.exists, "Does the `create_dir` method have a `path` argument?"

    directory = site.get_by_value("assignment", "directory", create_dir.code)
    assert directory.exists, "Are you assigning the correct value to `directory`?"

    directory_path = directory.code.find_all("binary_operator", value="/")
    directory_path_exists = len(directory_path) == 1
    assert directory_path_exists, "Are you assigning the correct path to `directory`?"

    first_exist = str(directory_path[0].first) == "self.dest"
    assert (
        first_exist
    ), "Are you assigning the correct path to `directory`? The first part of the path should be `self.dest`."

    second_exist = (
        directory_path[0].second[0].value == "path"
        and directory_path[0].second[1].value == "relative_to"
    )
    assert (
        second_exist
    ), "Are you assigning the correct path to `directory`? The second part path should be a call to `path.relative_to()`."

    call_argument_exists = (
        len(second.find_all("call_argument")) == 1
        and str(second.find_all("call_argument")[0]) == "self.source"
    )
    assert (
        call_argument_exists
    ), "Are you passing `self.source` to `path.relative_to()`?"


@pytest.mark.test_site_create_dir_mkdir_module1
def test_site_create_dir_mkdir_module1(parse):

    # directory.mkdir(parents=True, exist_ok=True)

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")
    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    create_dir = site.get_by_name("def", "create_dir", site_class.code)
    assert (
        create_dir.exists
    ), "Have you created a method called `create_dir` in the `Site` class?"

    mkdir_call = create_dir.code.find(
        "atomtrailers",
        lambda node: node.value[0].value == "directory"
        and node.value[1].value == "mkdir"
        and node.value[2].type == "call",
    )
    mkdir_call_exist = mkdir_call is not None
    assert mkdir_call_exist, "Are you calling `mkdir()` on `directory`?"

    mkdir_call_args = site.get_args(mkdir_call)

    parents = "parents:True" in mkdir_call_args
    assert parents, "Are you passing `parents` set to `True` to `mkdir()`?"

    exist_ok = "exist_ok:True" in mkdir_call_args
    assert exist_ok, "Are you passing `exist_ok` set to `True` to `mkdir()`?"


@pytest.mark.test_site_build_function_module1
def test_site_build_function_module1(parse):

    # def build(self):
    #     self.dest.mkdir(parents=True, exist_ok=True)

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    build = site.get_by_name("def", "build", site_class.code)
    assert build.exists, "Have you created a method called `build` in the `Site` class?"

    self_arg = site.get_by_value("def_argument", "self", build.code)
    assert self_arg.exists, "Does the `build` method have a `self` argument?"

    mkdir_call = build.code.find(
        "atomtrailers",
        lambda node: node[0].value == "self"
        and node[1].value == "dest"
        and node[2].value == "mkdir"
        and node[3].type == "call",
    )
    mkdir_call_exist = mkdir_call is not None
    assert mkdir_call_exist, "Are you calling `mkdir()` on `self.dest`?"

    mkdir_call_args = site.get_args(mkdir_call)

    parents = "parents:True" in mkdir_call_args
    assert parents, "Are you passing `parents` set to `True` to `mkdir()`?"

    exist_ok = "exist_ok:True" in mkdir_call_args
    assert exist_ok, "Are you passing `exist_ok` set to `True` to `mkdir()`?"


@pytest.mark.test_site_path_rglob_module1
def test_site_path_rglob_module1(parse):

    # for path in self.source.rglob("*"):
    #     if path.is_dir():
    #         self.create_dir(path)

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    build = site.get_by_name("def", "build", site_class.code)
    assert build.exists, "Have you created a method called `build` in the `Site` class?"

    for_loop = build.code.for_
    for_loop_exists = for_loop is not None
    assert for_loop_exists, "Have you created a for loop in the `build` method?"

    for_loop_target_exists = (
        str(for_loop.target).replace("'", '"') == 'self.source.rglob("*")'
    )
    assert (
        for_loop_target_exists
    ), "Have you created a for loop in the `build` method? That loops through `self.source` with the `rglob` method?"

    for_loop_iterator_exists = for_loop.iterator.value == "path"
    assert (
        for_loop_iterator_exists
    ), "Have you created a `for` loop in the `build` method? Are you calling the current loop item `path`?"

    if_is_dir = for_loop.if_.find(
        "atomtrailers",
        lambda node: node[0].value == "path"
        and node[1].value == "is_dir"
        and node[2].type == "call",
    )
    if_is_dir_exist = if_is_dir is not None
    assert (
        if_is_dir_exist
    ), "Have you created an `if` statement that checks if `path` is a directory?"

    if_line = len(for_loop.if_.value) == 1
    assert if_line, "Do you have at least one statement in your `if` statement?"

    self_create_dir_exists = (
        for_loop.if_.value[0].find(
            "atomtrailers",
            lambda node: node.value[0].value == "self"
            and node[1].value == "create_dir"
            and node[2].type == "call"
            and node[2].value[0].value.value == "path",
        )
        is not None
    )
    assert (
        self_create_dir_exists
    ), "Are you calling the `create_dir()` method and passing the correct parameters?"


@pytest.mark.test_ssg_imports_module1
def test_ssg_imports_module1(parse):

    # import typer

    # from ssg.site import Site

    ssg = parse("ssg")
    assert ssg.success, ssg.message

    typer_import = "typer" in ssg.get_imports()
    assert typer_import, "Are you importing `typer`?"

    site_import = "Site" in ssg.get_from_import("ssg.site")
    assert site_import, "Are you importing `Site` from `ssg.site`?"


@pytest.mark.test_ssg_main_command_module1
def test_ssg_main_command_module1(parse):

    # def main(source="content", dest="dist"):
    #     config = {
    #         "source": source,
    #         "dest": dest
    #     }

    ssg = parse("ssg")
    assert ssg.success, ssg.message

    main = ssg.get_by_name("def", "main")
    assert (
        main.exists
    ), "Have you created a function called `main` in the `ssg.py` file?"

    source_arg = ssg.get_by_value("def_argument", "source", main.code)
    assert source_arg.exists, "Does the `main` function have a `source` argument?"

    source_default = source_arg.code.value.value.replace("'", '"') == '"content"'
    assert (
        source_default
    ), 'Does the `source` argument have a default value of `"content"`?'

    dest_arg = ssg.get_by_value("def_argument", "dest", main.code)
    assert dest_arg.exists, "Does the `main` function have a `dest` argument?"

    dest_default = dest_arg.code.value.value.replace("'", '"') == '"dist"'
    assert dest_default, 'Does the `source` argument have a default value of `"dist"`?'

    config = ssg.get_by_value("assignment", "config", main.code)
    config_dict = ssg.flatten(config.code.value)
    config_exists = config.exists and config.code.value.type == "dict"
    assert (
        config_exists
    ), "Are you assigning a dictionary to a variable named `config` in the `main` function?"

    source_kv = "source:source" in config_dict
    dest_kv = "dest:dest" in config_dict
    assert (
        source_kv
    ), 'Does the `config` dictionary have a `"source": source` key value pair?'

    assert dest_kv, 'Does the `config` dictionary have a `"dest": dest` key value pair?'


@pytest.mark.test_ssg_build_call_module1
def test_ssg_build_call_module1(parse):

    # Site(**config).build()

    ssg = parse("ssg")
    assert ssg.success, ssg.message

    main = ssg.get_by_name("def", "main")
    assert (
        main.exists
    ), "Have you created a function called `main` in the `ssg.py` file?"

    build_call = main.code.find(
        "atomtrailers",
        lambda node: node.value[0].value == "Site"
        and node[1].type == "call"
        and node[1].value[0].type == "dict_argument"
        and node[1].value[0].value.value == "config"
        and node[2].value == "build"
        and node[3].type == "call",
    )
    build_call_exists = build_call is not None
    assert (
        main.exists
    ), "Are you calling the `build()` method on `Site()`? And are you passing `**config` to the `Site` instance?"


@pytest.mark.test_ssg_typer_run_module1
def test_ssg_typer_run_module1(parse):

    # typer.run(main)

    ssg = parse("ssg")
    assert ssg.success, ssg.message

    run_call = ssg.code.find(
        "atomtrailers",
        lambda node: node[0].value == "typer"
        and node[1].value == "run"
        and node[2].type == "call"
        and node[2].value[0].value.value == "main",
    )
    run_call_exist = run_call is not None
    assert run_call_exist, "Are you calling `run()` on `typer` and passing in `main`?"
