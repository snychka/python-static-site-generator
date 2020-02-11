import pytest


@pytest.mark.test_parser_imports_module4
def test_parser_imports_module4(parse):
    # from docutils.core import publish_parts
    # from markdown import markdown

    # from ssg.content import Content
    pass


@pytest.mark.test_parser_markdown_class_module4
def test_parser_markdown_class_module4(parse):
    # class MarkdownParser(Parser):
    #     extensions = [".md", ".markdown"]
    pass


@pytest.mark.test_parser_markdown_parse_module4
def test_parser_markdown_parse_module4(parse):
    # def parse(self, path, source, dest):
    #     content = Content.load(self.read(path))
    pass


@pytest.mark.test_parser_markdown_parse_write_html_module4
def test_parser_markdown_parse_write_html_module4(parse):
    # html = markdown(content.body)
    # self.write(path, dest, html)
    pass


@pytest.mark.test_parser_restructuredtext_class_module4
def test_parser_restructuredtext_class_module4(parse):
    # class ReStructuredTextParser(Parser):
    #     extensions = [".rst"]
    pass


@pytest.mark.test_parser_restructuredtext_parse_module4
def test_parser_restructuredtext_parse_module4(parse):
    # def parse(self, path, source, dest):
    #     content = Content.load(self.read(path))
    pass


@pytest.mark.test_parser_restructuredtext_parse_write_html_module4
def test_parser_restructuredtext_parse_write_html_module4(parse):
    # html = publish_parts(content.body, writer_name="html5")
    # self.write(path, dest, html["html_body"])
    pass


@pytest.mark.test_site_staticmethod_module4
def test_site_staticmethod_module4(parse):
    # import sys

    # @staticmethod
    # def error(message, end="\n"):
    #     sys.stderr.write("\x1b[1;31m" + message.strip(parse) + "\x1b[0m" + end)
    pass


@pytest.mark.test_site_error_call_module4
def test_site_error_call_module4(parse):
    # self.error(
    #     "No parser for the `{}` extension, file skipped!".format(
    #         path.suffix
    #     )
    # )
    pass
