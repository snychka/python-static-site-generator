import re
import ast

import parso
import pytest

from pathlib import Path
from redbaron import RedBaron


def get_source_code(filename, ssg=True):

    if ssg:
        file_path = Path.cwd() / "ssg" / filename
    else:
        file_path = Path.cwd() / filename

    grammar = parso.load_grammar()
    module = grammar.parse(path=file_path.resolve())
    parse_error = len(grammar.iter_errors(module)) == 0

    try:
        error_message = grammar.iter_errors(module)[0].message
        error_start_pos = grammar.iter_errors(module)[0].start_pos[0]
    except IndexError:
        error_message = ""
        error_start_pos = ""
    message = "{} on or around line {} in `{}`.".format(
        error_message, error_start_pos, file_path.name
    )
    if parse_error:
        with open(file_path.resolve(), "r") as source_code:
            return parse_error, "", RedBaron(source_code.read())
    else:
        return parse_error, message, ""


@pytest.fixture
def content():
    return get_source_code('content.py')


@pytest.fixture
def parsers():
    return get_source_code('parsers.py')


@pytest.fixture
def site():
    return get_source_code('site.py')


@pytest.fixture
def ssg():
    return get_source_code('ssg.py', False)


@pytest.fixture
def get_imports():
    def _get_imports(code, value):
        imports = code.find_all(
            "from_import",
            lambda node: "".join(
                list(node.value.node_list.map(lambda node: str(node)))
            )
            == value,
        ).find_all("name_as_name")
        return list(imports.map(lambda node: node.value))

    return _get_imports


@pytest.fixture
def get_by_name():
    def _get_by_name(code, type, name):
        item = code.find_all(type, lambda node: node.name == name)

        return (True, item[0]) if len(item) > 0 else (False, [])

    return _get_by_name


# def rq(string):
#     return re.sub(r'(\'|")', "", str(string))


# def tqrw(string):
#     return str(string).replace("'", '"').replace(" ", "")


# def simplify(main):
#     def _simplify(node):
#         if not isinstance(node, ast.Ast):
#             if isinstance(node, (type(None), bool)):
#                 buf.append(repr(node))
#             else:
#                 buf.append(node)
#             return

#         for idx, field in enumerate(node.fields):
#             value = getattr(node, field)
#             if value == "load" or value == "store":
#                 return
#             if idx:
#                 buf.append(".")
#             if isinstance(value, list):
#                 for idx, item in enumerate(value):
#                     if idx:
#                         buf.append(".")
#                     _simplify(item)
#             else:
#                 _simplify(value)

#     buf = []
#     _simplify(main)
#     return "".join(buf)


# @pytest.fixture
# def get_conditional(code, values, type, nested=False):
#     def flat(node):
#         if node.type == "comparison":
#             return "{}:{}:{}".format(
#                 str(node.first).replace("'", '"'),
#                 str(node.value).replace(" ", ":"),
#                 str(node.second).replace("'", '"'),
#             )
#         elif node.type == "unitary_operator":
#             return "{}:{}".format(
#                 str(node.value), str(node.target).replace("'", '"')
#             )

#     nodes = code.value if nested else code
#     for value in values:
#         final_node = nodes.find_all(type).find(
#             ["comparison", "unitary_operator"], lambda node:
#             flat(node) == value
#         )
#         if final_node is not None:
#             return final_node
#     return None
