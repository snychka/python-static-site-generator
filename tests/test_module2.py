import pytest


@pytest.mark.test_parser_base_class_module2
def test_parser_base_class_module2(parse):
    # from typing import List

    # class Parser:
    #     extensions: List[str] = []

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    typing_import = "List" in parsers.get_from_import("typing")
    assert typing_import, "Have you imported `List` from `typing`?"

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

    typing_import = "List" in parsers.get_from_import("typing")
    assert typing_import, "Have you imported `List` from `typing`?"

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
        return_statement.value.comparison.first.value == "extension"
        and return_statement.value.comparison.value.first == "in"
        and str(return_statement.value.comparison.second) == "self.extensions"
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

    typing_import = "List" in parsers.get_from_import("typing")
    assert typing_import, "Have you imported `List` from `typing`?"

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

    typing_import = "List" in parsers.get_from_import("typing")
    assert typing_import, "Have you imported `List` from `typing`?"

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
    
    args_exist = (
        "None:path" in open_args
        and 'None:"r"' in open_args
    )
    assert args_exist, "Are you passing `open` the correct arguments?"

    with_as = read.code.with_context_item.as_.value == "file"
    assert with_as, "Does your `with ` have and `as file` statement?"

    return_read_call = read.code.with_.return_.find(
        "atomtrailers",
        lambda node: node[0].value == "file"
        and node[1].value == "read"
        and node[2].type == "call",
    ) is not None

    assert return_read_call, "Are you return a call to `read()` on `file`?"


"""
@pytest.mark.test_parser_write_function_module2
def test_parser_write_function_module2(parse):
    # def write(self, path, dest, content, ext=".html"):
    #     full_path = dest / path.with_suffix(ext).name
    assert False


@pytest.mark.test_parser_write_function_open_module2
def test_parser_write_function_open_module2(parse):
    # with open(full_path, "w") as file:
    #     file.write(content)
    assert False


@pytest.mark.test_parser_copy_function_module2
def test_parser_copy_function_module2(parse):
    # import shutil
    # def copy(self, path, source, dest):
    #     shutil.copy2(path, dest / path.relative_to(source))
    assert False


@pytest.mark.test_parser_resource_class_module2
def test_parser_resource_class_module2(parse):
    # class ResourceParser(Parser):
    #     extensions = [".jpg", ".png", ".gif", ".css", ".html"]

    #     def parse(self, path, source, dest):
    #         self.copy(path, source, dest)
    assert False


@pytest.mark.test_site_parsers_module2
def test_site_parsers_module2(parse):
    # , parsers=None
    # self.parsers = parsers or []
    assert False


@pytest.mark.test_ssg_config_parser_module2
def test_ssg_config_parser_module2(parse):
    # import ssg.parsers
    # "parsers": [
    #     ssg.parsers.ResourceParser(),
    # ],
    assert False


@pytest.mark.test_site_load_parser_module2
def test_site_load_parser_module2(parse):
    # def load_parser(self, extension):
    #     for parser in self.parsers:
    #         if parser.valid_extension(extension):
    #             return parser
    assert False


@pytest.mark.test_site_run_parser_module2
def test_site_run_parser_module2(parse):
    # def run_parser(self, path):
    #     parser = self.load_parser(path.suffix)
    assert False


@pytest.mark.test_site_run_parser_if_module2
def test_site_run_parser_if_module2(parse):
    # if parser is not None:
    #     parser.parse(path, self.source, self.dest)
    # else:
    #     print('Error')
    assert False


@pytest.mark.test_site_build_elif_module2
def test_site_build_elif_module2(parse):
    # elif path.is_file():
    #     self.run_parser(path)
    assert False
"""
