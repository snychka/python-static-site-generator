import re
import pytest

import redbaron


@pytest.mark.test_parser_base_class_module2
def test_parser_base_class_module2(parse):
    # from typing import List
    # from pathlib import Path

    # class Parser:
    #     extensions: List[str] = []

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    typing_import = "List" in parsers.get_from_import("typing")
    assert typing_import, "Have you imported `List` from `typing`?"

    path_import = "Path" in parsers.get_from_import("pathlib")
    assert path_import, "Have you imported `Path` from `pathlib`?"

    parser_class = parsers.get_by_name("class", "Parser")

    assert (
        parser_class.exists
    ), "Have you created a class called `Parser` in the `parsers.py` file?"

    extensions = parsers.get_by_value("assignment", "extensions", parser_class.code)
    extensions_exist = (
        extensions.exists
        and extensions.code.value.type == "list"
        and str(extensions.code.annotation) == "List[str]"
    )
    assert extensions_exist, (
        "Have you created a variable called `extensions` and assigned it an empty list?"
        " Have you given it a type annotation of `List[str]`?"
    )


@pytest.mark.test_parser_valid_extension_function_module2
def test_parser_valid_extension_function_module2(parse):
    # def valid_extension(self, extension):
    #     return extension in self.extensions

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    parser_class = parsers.get_by_name("class", "Parser")

    assert (
        parser_class.exists
    ), "Have you created a class called `Parser` in the `parsers.py` file?"

    valid_extension = parsers.get_by_name("def", "valid_extension", parser_class.code)

    assert (
        valid_extension.exists
    ), "Have you created a method called `valid_extension` in the `Parser` class?"

    self_arg = parsers.get_by_value("def_argument", "self", valid_extension.code)
    assert self_arg.exists, "Does the `valid_extension` method have a `self` argument?"

    extension_arg = parsers.get_by_value(
        "def_argument", "extension", valid_extension.code
    )
    assert (
        extension_arg.exists
    ), "Does the `valid_extension` method have a `extension` argument?"

    return_statement = valid_extension.code.return_
    return_exist = return_statement is not None
    assert return_exist, "Do you have a `return` statement?"

    in_statement = (
        return_statement.comparison.first.value == "extension"
        and return_statement.comparison.value.first == "in"
        and str(return_statement.comparison.second) == "self.extensions"
    )

    assert (
        in_statement
    ), "Do you have a `return` statement that returns if `extension` is `in` `self.extensions`?"


@pytest.mark.test_parser_parse_function_module2
def test_parser_parse_function_module2(parse):
    # def parse(self, path: Path, source: Path, dest: Path):
    #     raise NotImplementedError

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    parser_class = parsers.get_by_name("class", "Parser")
    assert (
        parser_class.exists
    ), "Have you created a class called `Parser` in the `parsers.py` file?"

    parse = parsers.get_by_name("def", "parse", parser_class.code)
    assert (
        parse.exists
    ), "Have you created a method called `parse` in the `Parser` class?"

    self_arg = parsers.get_by_value("def_argument", "self", parse.code)
    assert self_arg.exists, "Does the `parse` method have a `self` argument?"

    path_arg = parsers.get_by_value("def_argument", "path", parse.code)
    path_arg_exists = path_arg.exists and path_arg.code.annotation.value == "Path"
    assert path_arg_exists, "Does the `parse` method have a `path` argument?"

    source_arg = parsers.get_by_value("def_argument", "source", parse.code)
    source_arg_exists = source_arg.exists and source_arg.code.annotation.value == "Path"
    assert source_arg_exists, "Does the `parse` method have a `source` argument?"

    dest_arg = parsers.get_by_value("def_argument", "dest", parse.code)
    dest_arg_exists = dest_arg.exists and dest_arg.code.annotation.value == "Path"
    assert dest_arg_exists, "Does the `parse` method have a `dest` argument?"

    raise_exists = (
        parse.code.raise_ and parse.code.raise_.value.value == "NotImplementedError"
    )
    assert raise_exists, "Are you raising`NotImplementedError` in the `parse` method?"


@pytest.mark.test_parser_read_function_module2
def test_parser_read_function_module2(parse):
    # def read(self, path):
    #     with open(path, "r") as file:
    #         return file.read()

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    parser_class = parsers.get_by_name("class", "Parser")
    assert (
        parser_class.exists
    ), "Have you created a class called `Parser` in the `parsers.py` file?"

    read = parsers.get_by_name("def", "read", parser_class.code)
    assert read.exists, "Have you created a method called `read` in the `Parser` class?"

    self_arg = parsers.get_by_value("def_argument", "self", read.code)
    assert self_arg.exists, "Does the `read` method have a `self` argument?"

    path_arg = parsers.get_by_value("def_argument", "path", read.code)
    assert path_arg.exists, "Does the `read` method have a `path` argument?"

    with_exists = read.code.with_ is not None
    assert with_exists, "Do you have a `with` statement in the `read` method?"

    open_call = parsers.get_call("open", read.code.with_)
    assert open_call.exists, "Do you have a call to `open` in your `with` statement?"

    open_args = parsers.get_args(open_call.code)

    args_exist = "None:path" in open_args and 'None:"r"' in open_args
    assert args_exist, "Are you passing `open` the correct arguments?"

    with_as = read.code.with_context_item.as_.value == "file"
    assert with_as, "Does your `with ` have and `as file` statement?"

    return_read_call = (
        read.code.with_.return_.find(
            "atomtrailers",
            lambda node: node[0].value == "file"
            and node[1].value == "read"
            and node[2].type == "call",
        )
        is not None
    )

    assert return_read_call, "Are you returning a call to `read()` on `file`?"


@pytest.mark.test_parser_write_function_module2
def test_parser_write_function_module2(parse):
    # def write(self, path, dest, content, ext=".html"):
    #     full_path = dest / path.with_suffix(ext).name

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    parser_class = parsers.get_by_name("class", "Parser")
    assert (
        parser_class.exists
    ), "Have you created a class called `Parser` in the `parsers.py` file?"

    write = parsers.get_by_name("def", "write", parser_class.code)
    assert (
        write.exists
    ), "Have you created a method called `write` in the `Parser` class?"

    self_arg = parsers.get_by_value("def_argument", "self", write.code)
    assert self_arg.exists, "Does the `write` method have a `self` argument?"

    path_arg = parsers.get_by_value("def_argument", "path", write.code)
    assert path_arg.exists, "Does the `write` method have a `path` argument?"

    dest_arg = parsers.get_by_value("def_argument", "dest", write.code)
    assert dest_arg.exists, "Does the `write` method have a `dest` argument?"

    content_arg = parsers.get_by_value("def_argument", "content", write.code)
    assert content_arg.exists, "Does the `write` method have a `content` argument?"

    ext_arg = parsers.get_by_value("def_argument", "ext", write.code)
    ext_arg_exists = (
        ext_arg.exists and ext_arg.code.value.value.replace("'", '"') == '".html"'
    )
    assert (
        ext_arg_exists
    ), "Does the `write` method have a `ext` argument set to the correct default argument?"

    assignment = write.code.assignment
    full_path_exists = assignment.target.value == "full_path"
    assert (
        full_path_exists
    ), "Do you have a variable called `full_path` that is set correctly?"

    right_side = (
        assignment.binary_operator.find(
            "atomtrailers",
            lambda node: node[0].value == "path"
            and node[1].value == "with_suffix"
            and node[2].type == "call"
            and node[2].call_argument.name.value == "ext"
            and node[3].value == "name",
        )
        is not None
    )

    correct_path = (
        assignment.binary_operator.value == "/"
        and assignment.binary_operator.first.value == "dest"
        and right_side
    )
    assert (
        correct_path
    ), "Do you have a variable called `full_path` that is set to `dest / path.with_suffix(ext).name`?"


@pytest.mark.test_parser_write_function_open_module2
def test_parser_write_function_open_module2(parse):
    # with open(full_path, "w") as file:
    #     file.write(content)

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    parser_class = parsers.get_by_name("class", "Parser")
    assert (
        parser_class.exists
    ), "Have you created a class called `Parser` in the `parsers.py` file?"

    write = parsers.get_by_name("def", "write", parser_class.code)
    assert (
        write.exists
    ), "Have you created a method called `write` in the `Parser` class?"

    with_exists = write.code.with_ is not None
    assert with_exists, "Do you have a `with` statement in the `write` method?"

    open_call = parsers.get_call("open", write.code.with_)
    assert open_call.exists, "Do you have a call to `open` in your `with` statement?"

    open_args = parsers.get_args(open_call.code)

    args_exist = "None:full_path" in open_args and 'None:"w"' in open_args
    assert args_exist, "Are you passing `open` the correct arguments?"

    with_as = write.code.with_context_item.as_.value == "file"
    assert with_as, "Does your `with ` have and `as file` statement?"

    write_call = (
        write.code.with_.find(
            "atomtrailers",
            lambda node: node[0].value == "file"
            and node[1].value == "write"
            and node[2].type == "call"
            and node[2].name.value == "content",
        )
        is not None
    )

    assert write_call, "Are you calling `write()` on `file` and passing in `content`?"


@pytest.mark.test_parser_copy_function_module2
def test_parser_copy_function_module2(parse):
    # import shutil
    # def copy(self, path, source, dest):
    #     shutil.copy2(path, dest / path.relative_to(source))

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    parser_class = parsers.get_by_name("class", "Parser")
    assert (
        parser_class.exists
    ), "Have you created a class called `Parser` in the `parsers.py` file?"

    shutil_import = "shutil" in parsers.get_imports()
    assert shutil_import, "Have you imported `shutil`?"

    copy = parsers.get_by_name("def", "copy", parser_class.code)
    assert copy.exists, "Have you created a method called `copy` in the `Parser` class?"

    self_arg = parsers.get_by_value("def_argument", "self", copy.code)
    assert self_arg.exists, "Does the `copy` method have a `self` argument?"

    path_arg = parsers.get_by_value("def_argument", "path", copy.code)
    assert path_arg.exists, "Does the `copy` method have a `path` argument?"

    source_arg = parsers.get_by_value("def_argument", "source", copy.code)
    assert source_arg.exists, "Does the `copy` method have a `source` argument?"

    dest_arg = parsers.get_by_value("def_argument", "dest", copy.code)
    assert dest_arg.exists, "Does the `copy` method have a `dest` argument?"

    copy2_call = copy.code.find(
        "atomtrailers",
        lambda node: node[0].value == "shutil"
        and node[1].value == "copy2"
        and node[2].type == "call",
    )
    copy2_call_exist = copy2_call is not None
    assert copy2_call_exist, "Are you calling `shutil.copy2()` in the `copy` method?"

    first_arg = copy2_call.call_argument.name.value == "path"
    assert (
        first_arg
    ), "Are you passing `path` as the first argument to `shutil.copy2()`?"

    right_side = (
        copy2_call.binary_operator.find(
            "atomtrailers",
            lambda node: node[0].value == "path"
            and node[1].value == "relative_to"
            and node[2].type == "call"
            and node[2].call_argument.name.value == "source",
        )
        is not None
    )

    correct_path = (
        copy2_call.binary_operator.value == "/"
        and copy2_call.binary_operator.first.value == "dest"
        and right_side
    )

    assert (
        correct_path
    ), "Are you passing `dest / path.relative_to(source)` as the first argument to `shutil.copy2()`?"


@pytest.mark.test_parser_resource_class_module2
def test_parser_resource_class_module2(parse):
    # class ResourceParser(Parser):
    #     extensions = [".jpg", ".png", ".gif", ".css", ".html"]

    #     def parse(self, path, source, dest):
    #         self.copy(path, source, dest)

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    resource_parser_class = parsers.get_by_name("class", "ResourceParser")
    assert (
        resource_parser_class.exists
    ), "Have you created a class called `ResourceParser` in the `parsers.py` file?"

    resource_parser_location = isinstance(resource_parser_class.code.parent, redbaron.redbaron.RedBaron)
    assert (
        resource_parser_location
    ), "Is the `ResourceParser` class declared in the correct scope?"

    inheriting = resource_parser_class.code.inherit_from.name.value == "Parser"
    assert inheriting, "Is `ResourceParser` a sub-class of the `Parser` class?"

    extensions = parsers.get_by_value(
        "assignment", "extensions", resource_parser_class.code
    )
    assert (
        extensions.exists
    ), "Have you created a variable called `extensions` and assigned it a list of extensions?"

    ext_list = extensions.code.list_
    ext_list_exists = ext_list is not None and len(ext_list) == 5
    assert (
        ext_list_exists
    ), "Have you created a variable called `extensions` and assigned it a list of extensions?"

    ext_values = list(
        ext_list.find_all("string").map(lambda node: re.sub("\"|'", "", node.value))
    )
    ext_values.sort()

    ext_values_exist = ext_values == [".css", ".gif", ".html", ".jpg", ".png"]
    assert (
        ext_values_exist
    ), "Does the `extensions` variable have the correct extensions?"

    parse = parsers.get_by_name("def", "parse", resource_parser_class.code)
    assert (
        parse.exists
    ), "Have you created a method called `parse` in the `ResourceParser` class?"

    self_arg = parsers.get_by_value("def_argument", "self", parse.code)
    assert self_arg.exists, "Does the `parse` method have a `self` argument?"

    path_arg = parsers.get_by_value("def_argument", "path", parse.code)
    assert path_arg.exists, "Does the `parse` method have a `path` argument?"

    source_arg = parsers.get_by_value("def_argument", "source", parse.code)
    assert source_arg.exists, "Does the `parse` method have a `source` argument?"

    dest_arg = parsers.get_by_value("def_argument", "dest", parse.code)
    assert dest_arg.exists, "Does the `parse` method have a `dest` argument?"

    parse_call = parse.code.find(
        "atomtrailers",
        lambda node: node[0].value == "self"
        and node[1].value == "copy"
        and node[2].type == "call"
        and node[2].value[0].name.value == "path"
        and node[2].value[1].name.value == "source"
        and node[2].value[2].name.value == "dest",
    )


@pytest.mark.test_site_parsers_module2
def test_site_parsers_module2(parse):
    # , parsers=None
    # self.parsers = parsers or []

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    init_def = site.get_by_name("def", "__init__", site_class.code)
    assert init_def.exists, "Does the class `Site` have an `__init__` method?"

    parsers_arg = site.get_by_value("def_argument", "parsers", init_def.code)
    assert parsers_arg.exists, "Does the `__init__` method have a `parsers` argument?"

    default_value = parsers_arg.code.value.name.value == "None"
    assert default_value, "Is the `parsers` argument set to `None`?"

    self_parsers = site.get_by_value("assignment", "self.parsers", init_def.code)
    assert self_parsers.exists, "Are you assigning the correct value to `self.parsers`?"

    right = self_parsers.code.boolean_operator

    parsers_correct = (
        right.value == "or"
        and right.first.name.value == "parsers"
        and right.second.type == "list"
        and len(right.second.value) == 0
    )
    assert parsers_correct, "Are you setting `self.parsers` to `parsers` or `[]`?"


@pytest.mark.test_ssg_config_parser_module2
def test_ssg_config_parser_module2(parse):
    # import ssg.parsers
    # "parsers": [
    #     ssg.parsers.ResourceParser(),
    # ],
    ssg = parse("ssg")
    assert ssg.success, ssg.message

    parsers_import = "ssg.parsers" in ssg.get_imports()
    assert parsers_import, "Are you importing `ssg.parsers`?"

    main = ssg.get_by_name("def", "main")
    assert (
        main.exists
    ), "Have you created a function called `main` in the `ssg.py` file?"

    config = ssg.get_by_value("assignment", "config", main.code)
    config_dict = ssg.flatten(config.code.value)

    rp_kv = "parsers:ssg.parsers.ResourceParser()" in config_dict
    assert (
        rp_kv
    ), "Does the `config` dictionary have a `parsers` key with an array with a single value of `ssg.parsers.ResourceParser()`?"


@pytest.mark.test_site_load_parser_module2
def test_site_load_parser_module2(parse):
    # def load_parser(self, extension):
    #     for parser in self.parsers:
    #         if parser.valid_extension(extension):
    #             return parser

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    load_parser = site.get_by_name("def", "load_parser", site_class.code)
    assert load_parser.exists, "Does the class `Site` have an `load_parser` method?"

    self_arg = site.get_by_value("def_argument", "self", load_parser.code)
    assert self_arg.exists, "Does the `load_parser` method have a `self` argument?"

    extension_arg = site.get_by_value("def_argument", "extension", load_parser.code)
    assert (
        extension_arg.exists
    ), "Does the `load_parser` method have a `extension` argument?"

    for_loop = load_parser.code.for_

    iterator_correct = (
        for_loop.iterator.name.value == "parser"
        and str(for_loop.target) == "self.parsers"
    )
    assert (
        iterator_correct
    ), "Does the `load_parser` method have a `for` loop that loops through `self.parsers`?"

    valid_extension_call = for_loop.if_.find(
        "atomtrailers",
        lambda node: node[0].value == "parser"
        and node[1].value == "valid_extension"
        and node[2].type == "call"
        and node[2].value[0].name.value == "extension",
    )
    assert (
        valid_extension_call
    ), "In the `for` loop are you testing if `extension` is a valid extension?"

    return_exists = for_loop.if_.return_.name.value == "parser"
    assert return_exists, "Are you returning `parser` in the `if`?"


@pytest.mark.test_site_run_parser_module2
def test_site_run_parser_module2(parse):
    # def run_parser(self, path):
    #     parser = self.load_parser(path.suffix)

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    run_parser = site.get_by_name("def", "run_parser", site_class.code)
    assert run_parser.exists, "Does the class `Site` have an `run_parser` method?"

    self_arg = site.get_by_value("def_argument", "self", run_parser.code)
    assert self_arg.exists, "Does the `run_parser` method have a `self` argument?"

    path_arg = site.get_by_value("def_argument", "path", run_parser.code)
    assert path_arg.exists, "Does the `run_parser` method have a `path` argument?"

    parser = site.get_by_value("assignment", "parser", run_parser.code)
    assert parser.exists, "Are you assigning the correct value to `parser`?"

    load_parser_call = (
        parser.code.find(
            "atomtrailers",
            lambda node: node[0].value == "self"
            and node[1].value == "load_parser"
            and node[2].type == "call"
            and str(node[2].find("call_argument")) == "path.suffix",
        )
        is not None
    )

    assert (
        load_parser_call
    ), "Are you assigning a call to `self.load_parser()` to `parser`? Are you passing the path.suffix to `self.load_parser()`?"


@pytest.mark.test_site_run_parser_if_module2
def test_site_run_parser_if_module2(parse):
    # if parser is not None:
    #     parser.parse(path, self.source, self.dest)
    # else:
    #     print('Not Implemented')

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    run_parser = site.get_by_name("def", "run_parser", site_class.code)
    assert run_parser.exists, "Does the class `Site` have an `run_parser` method?"

    parser_if = run_parser.code.find("if")
    if_test = parser_if.find("comparison")

    test_correct = (
        if_test.first.name.value == "parser"
        and if_test.value.first == "is"
        and if_test.value.second == "not"
        and if_test.second.name.value == "None"
    )
    assert (
        test_correct
    ), "Do you have an `if` statement that tests whether `parser` is not `None`?"

    parse_call = parser_if.find(
        "atomtrailers",
        lambda node: node[0].value == "parser"
        and node[1].value == "parse"
        and node[2].type == "call",
    )
    assert parse_call, "Do you have a call to `parser.parse()` in the body of the `if`?"

    parse_args = list(
        parse_call.find_all("call_argument").map(lambda node: str(node.value))
    )

    args_correct = (
        len(parse_args) == 3
        and parse_args[0] == "path"
        and parse_args[1] == "self.source"
        and parse_args[2] == "self.dest"
    )
    assert (
        args_correct
    ), "Are you passing the correct number of arguments to `parser.parse()`?"

    else_print = run_parser.code.else_.print_ is not None

    error_call = site.get_call("error", run_parser.code)
    error_call_exists = error_call.exists and error_call.code.parent[0].value == "self"
    error_args = list(
        error_call.code.call_argument.find_all(
            ["name", "string", "binary_operator"]
        ).map(lambda node: str(node.value).replace("'", '"'))
    )
    error_message = error_call_exists and error_args == [
        '"No parser for the {} extension, file skipped!"',
        "format",
        "path",
        "suffix",
    ]

    assert (
        else_print or error_message
    ), "Have you added an `else` statement to the `if` that prints the correct message?"


@pytest.mark.test_site_build_elif_module2
def test_site_build_elif_module2(parse):
    # elif path.is_file():
    #     self.run_parser(path)

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

    elif_exists = for_loop.elif_ is not None
    assert (
        elif_exists
    ), "Have you added an `elif` to the `if` statement in the `build` method?"

    is_file_call = for_loop.elif_.test.find(
        "atomtrailers",
        lambda node: node[0].value == "path"
        and node[1].value == "is_file"
        and node[2].type == "call",
    )
    assert is_file_call, "Does the `elif` test if `path` is a file?"

    run_parser_call = (
        for_loop.elif_.find(
            "atomtrailers",
            lambda node: node[0].value == "self"
            and node[1].value == "run_parser"
            and node[2].type == "call"
            and node[2].value[0].name.value == "path",
        )
        is not None
    )
    assert run_parser_call, "Are you calling self.run_parser() in the `elif`?"
