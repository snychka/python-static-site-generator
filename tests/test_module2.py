import pytest


@pytest.mark.test_parser_base_class_module2
def test_parser_base_class_module2():
    # from typing import List


    # class Parser:
    #     extensions: List[str] = []
    pass


@pytest.mark.test_parser_valid_extension_function_module2
def test_parser_valid_extension_function_module2():
    # def valid_extension(self, extension):
    #     return extension in self.extensions
    pass


@pytest.mark.test_parser_parse_function_module2
def test_parser_parse_function_module2():
    # def parse(self, path: Path, source: Path, dest: Path):
    #     raise NotImplementedError
    pass


@pytest.mark.test_parser_read_function_module2
def test_parser_read_function_module2():
    # def read(self, path):
    #     with open(path, "r") as file:
    #         return file.read()
    pass


@pytest.mark.test_parser_write_function_module2
def test_parser_write_function_module2():
    # def write(self, path, dest, content, ext=".html"):
    #     full_path = dest / path.with_suffix(ext).name
    pass


@pytest.mark.test_parser_write_function_open_module2
def test_parser_write_function_open_module2():
    # with open(full_path, "w") as file:
    #     file.write(content)
    pass


@pytest.mark.test_parser_copy_function_module2
def test_parser_copy_function_module2():
    # import shutil
    # def copy(self, path, source, dest):
    #     shutil.copy2(path, dest / path.relative_to(source))
    pass


@pytest.mark.test_parser_resource_class_module2
def test_parser_resource_class_module2():
    # class ResourceParser(Parser):
    #     extensions = [".jpg", ".png", ".gif", ".css", ".html"]

    #     def parse(self, path, source, dest):
    #         self.copy(path, source, dest)
    pass


@pytest.mark.test_site_parsers_module2
def test_site_parsers_module2():
    # , parsers=None
    # self.parsers = parsers or []
    pass


@pytest.mark.test_ssg_config_parser_module2
def test_ssg_config_parser_module2():
    # import ssg.parsers
    # "parsers": [
    #     ssg.parsers.ResourceParser(),
    # ],
    pass


@pytest.mark.test_site_load_parser_module2
def test_site_load_parser_module2():
    # def load_parser(self, extension):
    #     for parser in self.parsers:
    #         if parser.valid_extension(extension):
    #             return parser
    pass


@pytest.mark.test_site_run_parser_module2
def test_site_run_parser_module2():
    # def run_parser(self, path):
    #     parser = self.load_parser(path.suffix)
    pass


@pytest.mark.test_site_run_parser_if_module2
def test_site_run_parser_if_module2():
    # if parser is not None:
    #     parser.parse(path, self.source, self.dest)
    # else:
    #     print('Error')
    pass


@pytest.mark.test_site_build_elif_module2
def test_site_build_elif_module2():
    # elif path.is_file():
    #     self.run_parser(path)
    pass
