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

    assert False


"""
@pytest.mark.test_parser_valid_extension_function_module2
def test_parser_valid_extension_function_module2(parse):
    # def valid_extension(self, extension):
    #     return extension in self.extensions
    assert False


@pytest.mark.test_parser_parse_function_module2
def test_parser_parse_function_module2(parse):
    # def parse(self, path: Path, source: Path, dest: Path):
    #     raise NotImplementedError
    assert False


@pytest.mark.test_parser_read_function_module2
def test_parser_read_function_module2(parse):
    # def read(self, path):
    #     with open(path, "r") as file:
    #         return file.read()
    assert False


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
