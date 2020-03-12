import re
import pytest


@pytest.mark.test_parser_imports_module4
def test_parser_imports_module4(parse):
    # from docutils.core import publish_parts
    # from markdown import markdown

    # from ssg.content import Content

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    docutils_import = "publish_parts" in parsers.get_from_import("docutils.core")
    assert docutils_import, "Are you importing `publish_parts` from `docutils.core`?"

    markdown_import = "markdown" in parsers.get_from_import("markdown")
    assert docutils_import, "Are you importing `markdown` from `markdown`?"

    ssg_import = "Content" in parsers.get_from_import("ssg.content")
    assert docutils_import, "Are you importing `Content` from `ssg.content`?"


@pytest.mark.test_parser_markdown_class_module4
def test_parser_markdown_class_module4(parse):
    # class MarkdownParser(Parser):
    #     extensions = [".md", ".markdown"]

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    markdown_parser_class = parsers.get_by_name("class", "MarkdownParser")
    assert (
        markdown_parser_class.exists
    ), "Have you created a class called `MarkdownParser` in the `parsers.py` file?"

    inheriting = markdown_parser_class.code.inherit_from.name.value == "Parser"
    assert inheriting, "Is `MarkdownParser` a sub-class of the `Parser` class?"

    extensions = parsers.get_by_value(
        "assignment", "extensions", markdown_parser_class.code
    )
    assert (
        extensions.exists
    ), "Have you created a variable called `extensions` and assigned it a list of extensions?"

    ext_list = extensions.code.list_
    ext_list_exists = ext_list is not None and len(ext_list) == 2
    assert (
        ext_list_exists
    ), "Have you created a variable called `extensions` and assigned it a list of extensions?"

    ext_values = list(
        ext_list.find_all("string").map(lambda node: re.sub("\"|'", "", node.value))
    )
    ext_values.sort()

    ext_values_exist = ext_values == [".markdown", ".md"]
    assert (
        ext_values_exist
    ), "Does the `extensions` variable have the correct extensions?"


@pytest.mark.test_parser_markdown_parse_module4
def test_parser_markdown_parse_module4(parse):
    # def parse(self, path, source, dest):
    #     content = Content.load(self.read(path))

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    markdown_parser_class = parsers.get_by_name("class", "MarkdownParser")
    assert (
        markdown_parser_class.exists
    ), "Have you created a class called `MarkdownParser` in the `parsers.py` file?"

    parse = parsers.get_by_name("def", "parse", markdown_parser_class.code)
    assert (
        parse.exists
    ), "Have you created a method called `parse` in the `MarkdownParser` class?"

    self_arg = parsers.get_by_value("def_argument", "self", parse.code)
    assert self_arg.exists, "Does the `parse` method have a `self` argument?"

    path_arg = parsers.get_by_value("def_argument", "path", parse.code)
    assert path_arg.exists, "Does the `parse` method have a `path` argument?"

    source_arg = parsers.get_by_value("def_argument", "source", parse.code)
    assert source_arg.exists, "Does the `parse` method have a `source` argument?"

    dest_arg = parsers.get_by_value("def_argument", "dest", parse.code)
    assert dest_arg.exists, "Does the `parse` method have a `dest` argument?"

    content = parsers.get_by_value("assignment", "content", parse.code)
    assert content.exists, "Are you assigning the correct value to `content`?"

    load_call = parsers.get_call("load", parse.code)

    load_call_exists = load_call.exists and load_call.code.parent[0].value == "Content"
    assert load_call_exists, "Are you calling `Content.load()`?"

    load_arg = load_call.code.call_argument.find(
        "atomtrailers",
        lambda node: node[0].value == "self"
        and node[1].value == "read"
        and node[2].type == "call"
        and node[2].value[0].name.value == "path",
    )
    assert load_arg, "Are you passing a call of `self.read(path)` to `Content.load()`?"


@pytest.mark.test_parser_markdown_parse_write_html_module4
def test_parser_markdown_parse_write_html_module4(parse):
    # html = markdown(content.body)
    # self.write(path, dest, html)

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    markdown_parser_class = parsers.get_by_name("class", "MarkdownParser")
    assert (
        markdown_parser_class.exists
    ), "Have you created a class called `MarkdownParser` in the `parsers.py` file?"

    parse = parsers.get_by_name("def", "parse", markdown_parser_class.code)
    assert (
        parse.exists
    ), "Have you created a method called `parse` in the `MarkdownParser` class?"

    html = parsers.get_by_value("assignment", "html", parse.code)
    assert html.exists, "Are you assigning the correct value to `html`?"

    markdown = parsers.get_call("markdown", parse.code)
    markdown_arg = (
        markdown.code.find(
            "atomtrailers",
            lambda node: node[0].value == "content" and node[1].value == "body",
        )
        is not None
    )
    markdown_call = markdown.exists and markdown_arg
    assert (
        markdown_call
    ), "Are you calling the `markdown` method and passing in `content.body`?"

    write_call = parse.code.find(
        "atomtrailers",
        lambda node: node[0].value == "self"
        and node[1].value == "write"
        and node[2].type == "call",
    )
    assert write_call, "Do you have a call to `self.write()`?"

    write_args = list(
        write_call.find_all("call_argument").map(lambda node: str(node.value))
    )

    args_correct = (
        len(write_args) == 3
        and write_args[0] == "path"
        and write_args[1] == "dest"
        and write_args[2] == "html"
    )
    assert (
        args_correct
    ), "Are you passing the correct number of arguments to `self.write()`?"


@pytest.mark.test_parser_restructuredtext_class_module4
def test_parser_restructuredtext_class_module4(parse):
    # class ReStructuredTextParser(Parser):
    #     extensions = [".rst"]

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    rst_parser_class = parsers.get_by_name("class", "ReStructuredTextParser")
    assert (
        rst_parser_class.exists
    ), "Have you created a class called `ReStructuredTextParser` in the `parsers.py` file?"

    inheriting = rst_parser_class.code.inherit_from.name.value == "Parser"
    assert inheriting, "Is `ReStructuredTextParser` a sub-class of the `Parser` class?"

    extensions = parsers.get_by_value("assignment", "extensions", rst_parser_class.code)
    assert (
        extensions.exists
    ), "Have you created a variable called `extensions` and assigned it a list of extensions?"

    ext_list = extensions.code.list_
    ext_list_exists = ext_list is not None and len(ext_list) == 1
    assert (
        ext_list_exists
    ), "Have you created a variable called `extensions` and assigned it a list of extensions?"

    ext_values = list(
        ext_list.find_all("string").map(lambda node: re.sub("\"|'", "", node.value))
    )
    ext_values.sort()

    ext_values_exist = ext_values == [".rst"]
    assert (
        ext_values_exist
    ), "Does the `extensions` variable have the correct extensions?"


@pytest.mark.test_parser_restructuredtext_parse_module4
def test_parser_restructuredtext_parse_module4(parse):
    # def parse(self, path, source, dest):
    #     content = Content.load(self.read(path))

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    rst_parser_class = parsers.get_by_name("class", "ReStructuredTextParser")
    assert (
        rst_parser_class.exists
    ), "Have you created a class called `ReStructuredTextParser` in the `parsers.py` file?"

    parse = parsers.get_by_name("def", "parse", rst_parser_class.code)
    assert (
        parse.exists
    ), "Have you created a method called `parse` in the `ReStructuredTextParser` class?"

    self_arg = parsers.get_by_value("def_argument", "self", parse.code)
    assert self_arg.exists, "Does the `parse` method have a `self` argument?"

    path_arg = parsers.get_by_value("def_argument", "path", parse.code)
    assert path_arg.exists, "Does the `parse` method have a `path` argument?"

    source_arg = parsers.get_by_value("def_argument", "source", parse.code)
    assert source_arg.exists, "Does the `parse` method have a `source` argument?"

    dest_arg = parsers.get_by_value("def_argument", "dest", parse.code)
    assert dest_arg.exists, "Does the `parse` method have a `dest` argument?"

    content = parsers.get_by_value("assignment", "content", parse.code)
    assert content.exists, "Are you assigning the correct value to `content`?"

    load_call = parsers.get_call("load", parse.code)

    load_call_exists = load_call.exists and load_call.code.parent[0].value == "Content"
    assert load_call_exists, "Are you calling `Content.load()`?"

    load_arg = load_call.code.call_argument.find(
        "atomtrailers",
        lambda node: node[0].value == "self"
        and node[1].value == "read"
        and node[2].type == "call"
        and node[2].value[0].name.value == "path",
    )
    assert load_arg, "Are you passing a call of `self.read(path)` to `Content.load()`?"


@pytest.mark.test_parser_restructuredtext_parse_write_html_module4
def test_parser_restructuredtext_parse_write_html_module4(parse):
    # html = publish_parts(content.body, writer_name="html5")
    # self.write(path, dest, html["html_body"])

    parsers = parse("parsers")
    assert parsers.success, parsers.message

    rst_parser_class = parsers.get_by_name("class", "ReStructuredTextParser")
    assert (
        rst_parser_class.exists
    ), "Have you created a class called `ReStructuredTextParser` in the `parsers.py` file?"

    parse = parsers.get_by_name("def", "parse", rst_parser_class.code)
    assert (
        parse.exists
    ), "Have you created a method called `parse` in the `ReStructuredTextParser` class?"

    html = parsers.get_by_value("assignment", "html", parse.code)
    assert html.exists, "Are you assigning the correct value to `html`?"

    publish_parts = parsers.get_call("publish_parts", html.code)
    publish_parts_args = parsers.get_args(publish_parts.code)

    args_correct = (
        len(publish_parts_args) == 2
        and publish_parts_args[0] == "None:content.body"
        and publish_parts_args[1] == 'writer_name:"html5"'
    )
    assert args_correct, "Are you passing the correct arguments to `publish_parts()`?"

    write_call = parsers.get_call("write", parse.code)
    write_call_exists = write_call.exists and write_call.code.parent[0].value == "self"
    assert write_call_exists, "Are you calling `self.write()`?"

    write_args = parsers.get_args(write_call.code)
    write_args_correct = (
        len(write_args) == 3
        and write_args[0] == "None:path"
        and write_args[1] == "None:dest"
        and write_args[2] == 'None:html["html_body"]'
    )
    assert (
        write_args_correct
    ), "Are you passing the correct arguments to `self.write()`?"


@pytest.mark.test_site_staticmethod_module4
def test_site_staticmethod_module4(parse):
    # import sys

    # @staticmethod
    # def error(message, end="\n"):
    #     sys.stderr.write("\x1b[1;31m" + message.strip() + "\x1b[0m" + end)

    site = parse("site")
    assert site.success, site.message

    sys_import = "sys" in site.get_imports()
    assert sys_import, "Are you importing `sys`?"

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    error = site.get_by_name("def", "error", site_class.code)
    assert (
        error.exists
    ), "Have you created a static method called `error` in the `Site` class?"

    decorator_exists = error.code.decorators.dotted_name.name.value == "staticmethod"
    assert (
        decorator_exists
    ), "Does the `error` method have a decorator of `@staticmethod`?"

    error.code.find(
        "atomtrailers",
        lambda node: len(node) == 4
        and node[0].name.value == "sys"
        and node[1].name.value == "stderr"
        and node[1].name.value == "write",
    )

    write_arg = list(
        error.code.call_argument.find_all(["name", "string", "binary_operator"]).map(
            lambda node: str(node.value).replace("'", '"')
        )
    )
    error_message = write_arg == [
        "+",
        '"\\x1b[1;31m"',
        "+",
        "message",
        "strip",
        "+",
        '"\\x1b[0m"',
        "end",
    ]
    assert error_message, "Are you passing in the correct error message?"


@pytest.mark.test_site_error_call_module4
def test_site_error_call_module4(parse):
    # self.error(
    #     "No parser for the `{}` extension, file skipped!".format(
    #         path.suffix
    #     )
    # )

    site = parse("site")
    assert site.success, site.message

    site_class = site.get_by_name("class", "Site")

    assert (
        site_class.exists
    ), "Have you created a class called `Site` in the `site.py` file?"

    run_parser = site.get_by_name("def", "run_parser", site_class.code)
    assert run_parser.exists, "Does the class `Site` have an `run_parser` method?"

    error_call = site.get_call("error", run_parser.code)
    error_call_exists = error_call.exists and error_call.code.parent[0].value == "self"
    assert error_call_exists, "Are you calling `self.error()`?"

    error_args = site.get_args(error_call.code)
    error_arg = list(
        error_call.code.call_argument.find_all(
            ["name", "string", "binary_operator"]
        ).map(lambda node: str(node.value).replace("'", '"'))
    )
    error_message = error_arg == [
        '"No parser for the {} extension, file skipped!"',
        "format",
        "path",
        "suffix",
    ]

    assert error_message, "Are you passing in the correct error message?"
