import re
import ast

import parso
import pytest

from pathlib import Path
from redbaron import RedBaron
from redbaron.utils import indent


class SourceCode:

    def __init__(self, exists, code):
        self.exists = exists
        self.code = code


class Parser:
    def __init__(self, filename):
        self.code = ""
        self.message = ""

        error_message = ""
        error_start_pos = ""

        if filename == "ssg":
            file_path = Path.cwd() / "ssg.py"
        else:
            file_path = Path.cwd() / "ssg" / "{}.py".format(filename)

        grammar = parso.load_grammar()
        module = grammar.parse(path=file_path.resolve())
        self.success = len(grammar.iter_errors(module)) == 0

        if self.success:
            with open(file_path.resolve(), "r") as source_code:
               self.code = RedBaron(source_code.read())
        else:
            error_message = grammar.iter_errors(module)[0].message
            error_start_pos = grammar.iter_errors(module)[0].start_pos[0]
            self.message = "{} on or around line {} in `{}`.".format(
                error_message, error_start_pos, file_path.name
            )

    def get_by_name(self, type, name, code=None):
        if code is None:
            item = self.code.find_all(type, lambda node: node.name == name)
        else:
            item = code.find_all(type, lambda node: node.name == name)

        return SourceCode(True, item[0]) if len(item) > 0 else SourceCode(False, [])

    def get_by_value(self, type, value, code=None):
        if code is None:
            item = self.code.find_all(type, lambda node: str(node.target) == value)
        else:
            item = code.find_all(type, lambda node: str(node.target) == value)
        return SourceCode(True, item[0]) if len(item) > 0 else SourceCode(False, [])

    def get_imports(self, value):
        imports = self.code.find_all(
            "from_import",
            lambda node: "".join(
                list(node.value.node_list.map(lambda node: str(node)))
            )
            == value,
        ).find_all("name_as_name")
        return list(imports.map(lambda node: node.value))

    def get_conditional(self, values, type, nested=False):
        def flat(node):
            if node.type == "comparison":
                return "{}:{}:{}".format(
                    str(node.first).replace("'", '"'),
                    str(node.value).replace(" ", ":"),
                    str(node.second).replace("'", '"'),
                )
            elif node.type == "unitary_operator":
                return "{}:{}".format(
                    str(node.value), str(node.target).replace("'", '"')
                )

        nodes = self.code.value if nested else self.code
        for value in values:
            final_node = nodes.find_all(type).find(
                ["comparison", "unitary_operator"], lambda node:
                flat(node) == value
            )
            if final_node is not None:
                return final_node
        return None


@pytest.fixture
def parse():

    def _parse(filename):
        return Parser(filename)

    return _parse
