import pytest


@pytest.mark.test_content_imports_module3
def test_content_imports_module3(parse):
    # import re

    # from collections.abc import Mapping

    # from yaml import load, FullLoader

    content = parse("content")
    assert content.success, content.message

    re_import = "re" in content.get_imports()
    assert re_import, "Have you imported `re`?"

    collections_import = "Mapping" in content.get_from_import("collections.abc")
    assert collections_import, "Have you imported `Mapping` from `collections.abc`?"

    yaml_load = "load" in content.get_from_import("yaml")
    yaml_full = "FullLoader" in content.get_from_import("yaml")

    yaml_imports = yaml_load and yaml_full
    assert collections_import, "Have you imported `load` and `FullLoader` from `yaml`?"


@pytest.mark.test_content_class_module3
def test_content_class_module3(parse):
    # class Content(Mapping):
    #     __delimiter = r"^(?:-|\+){3}\s*$"
    #     __regex = re.compile(__delimiter, re.MULTILINE)

    content = parse("content")
    assert content.success, content.message

    content_class = content.get_by_name("class", "Content")

    assert (
        content_class.exists
    ), "Have you created a class called `Content` in the `content.py` file?"

    inheriting = content_class.code.inherit_from.name.value == "Mapping"
    assert inheriting, "Is `Content` a sub-class of the `Mapping` class?"

    delimiter = content.get_by_value("assignment", "__delimiter", content_class.code)
    assert (
        delimiter.exists
    ), "Have you created a variable called `__delimiter` and assigned it a regular expression pattern?"

    delimiter_correct = (
        delimiter.code.value.value.replace("'", '"') == 'r"^(?:-|\\+){3}\\s*$"'
    )
    assert (
        delimiter_correct
    ), "Do you have the correct regular expression assigned to `__delimiter`?"

    regex = content.get_by_value("assignment", "__regex", content_class.code)
    assert (
        regex.exists
    ), "Have you created a variable called `__regex` and assigned it correctly?"

    re_compile_call = regex.code.find(
        "atomtrailers",
        lambda node: node[0].value == "re"
        and node[1].value == "compile"
        and node[2].type == "call",
    )
    assert re_compile_call, "Are you setting `__regex` to a call to `re.compile()`?"

    compile_args = list(
        re_compile_call.find_all("call_argument").map(lambda node: str(node.value))
    )

    args_correct = (
        len(compile_args) == 2
        and compile_args[0] == "__delimiter"
        and compile_args[1] == "re.MULTILINE"
    )
    assert (
        args_correct
    ), "Are you passing the correct number of arguments to `re.compile()`?"


@pytest.mark.test_content_classmethod_load_module3
def test_content_classmethod_load_module3(parse):
    # @classmethod
    # def load(cls, string):
    #     _, fm, content = cls.__regex.split(string, 2)
    #     metadata = load(fm, Loader=FullLoader)

    #     return cls(metadata, content)
    content = parse("content")
    assert content.success, content.message

    content_class = content.get_by_name("class", "Content")

    assert (
        content_class.exists
    ), "Have you created a class called `Content` in the `content.py` file?"

    load = content.get_by_name("def", "load", content_class.code)
    assert (
        load.exists
    ), "Have you created a class method called `load` in the `Content` class?"

    cls_arg = content.get_by_value("def_argument", "cls", load.code)
    assert cls_arg.exists, "Does the `load` method have a `cls` argument?"

    path_arg = content.get_by_value("def_argument", "string", load.code)
    assert path_arg.exists, "Does the `load` method have a `string` argument?"

    decorator_exists = load.code.decorators.dotted_name.name.value == "classmethod"
    assert (
        decorator_exists
    ), "Does the `load` method have a decorator of `@classmethod`?"

    tuple_return = load.code.find_all(
        "assignment",
        lambda node: node.find(
            "tuple",
            lambda node: node[0].name.value == "_"
            and node[1].name.value == "fm"
            and node[2].name.value == "content",
        ),
    )
    tuple_return_exists = tuple_return is not None
    assert (
        tuple_return_exists
    ), "Are you assigning a tuple the results of a call `to cls.__regex.split()`?"

    split_call = (
        tuple_return.find(
            "atomtrailers",
            lambda node: node[0].value == "cls"
            and node[1].value == "__regex"
            and node[2].value == "split"
            and node[3].type == "call",
        )
        is not None
    )
    assert (
        split_call
    ), "Do you have a call to `cls.__regex.split()` in the `load` method?"
    split_args = content.get_args(content.get_call("split", tuple_return).code)

    args_correct = (
        len(split_args) == 2
        and split_args[0] == "None:string"
        and split_args[1] == "None:2"
    )
    assert (
        args_correct
    ), "Are you passing the correct arguments to `cls.__regex.split()`?"

    metadata = content.get_by_value("assignment", "metadata", load.code)
    assert (
        metadata.exists
    ), "Have you created a variable called `metadata` and assigned it correctly?"

    yaml_load = content.get_call("load", metadata.code)
    yaml_load_args = content.get_args(yaml_load.code)

    yaml_args_correct = (
        len(yaml_load_args) == 2
        and yaml_load_args[0] == "None:fm"
        and yaml_load_args[1] == "Loader:FullLoader"
    )
    assert yaml_args_correct, "Are you passing the correct arguments to `load()`?"

    return_cls_call = load.code.return_ is not None
    assert return_cls_call, "Are you returning a call to `cls()`?"

    cls_call = content.get_call("cls", load.code.return_)
    cls_args = content.get_args(cls_call.code)

    cls_args_correct = (
        len(cls_args) == 2
        and cls_args[0] == "None:metadata"
        and cls_args[1] == "None:content"
    )
    assert cls_args_correct, "Are you passing the correct arguments to `cls()`?"


@pytest.mark.test_content_init_module3
def test_content_init_module3(parse):
    # def __init__(self, metadata, content):
    #     self.data = metadata
    #     self.data["content"] = content
    content = parse("content")
    assert content.success, content.message

    content_class = content.get_by_name("class", "Content")

    assert (
        content_class.exists
    ), "Have you created a class called `Content` in the `content.py` file?"

    init_def = content.get_by_name("def", "__init__", content_class.code)
    assert init_def.exists, "Does the class `Site` have an `__init__` method?"

    self_arg = content.get_by_value("def_argument", "self", init_def.code)
    assert self_arg.exists, "Does the `__init__` method have a `self` argument?"

    metadata_arg = content.get_by_value("def_argument", "metadata", init_def.code)
    assert metadata_arg.exists, "Does the `__init__` method have a `metadata` argument?"

    content_arg = content.get_by_value("def_argument", "content", init_def.code)
    assert content_arg.exists, "Does the `__init__` method have a `content` argument?"

    self_data = content.get_by_value("assignment", "self.data", init_def.code)
    self_data_exists = self_data.exists and self_data.code.value.value == "metadata"
    assert (
        self_data_exists
    ), "Have you created a variable called `self.data` and assigned it correctly?"

    self_content = init_def.code.find(
        "assignment",
        lambda node: node.find(
            "atomtrailers",
            lambda node: len(node) == 3
            and node[0].name.value == "self"
            and node[1].name.value == "data"
            and node[2].string.value.replace("'", '"') == '"content"',
        ),
    )
    self_content_exists = self_content is not None
    assert (
        self_content_exists and self_content.value.value == "content"
    ), 'Have you created a variable called `self.data["content"]` and assigned it correctly?'


@pytest.mark.test_content_body_property_module3
def test_content_body_property_module3(parse):
    # @property
    # def body(self):
    #     return self.data["content"]
    content = parse("content")
    assert content.success, content.message

    content_class = content.get_by_name("class", "Content")

    assert (
        content_class.exists
    ), "Have you created a class called `Content` in the `content.py` file?"

    body = content.get_by_name("def", "body", content_class.code)
    assert (
        body.exists
    ), "Have you created a class method called `body` in the `Content` class?"

    self_arg = content.get_by_value("def_argument", "self", body.code)
    assert self_arg.exists, "Does the `body` method have a `self` argument?"

    decorator_exists = body.code.decorators.dotted_name.name.value == "property"
    assert (
        decorator_exists
    ), "Does the `body` method have a decorator of `@property`?"

    body_return = body.code.return_.find(
        "atomtrailers",
        lambda node: len(node) == 3
        and node[0].name.value == "self"
        and node[1].name.value == "data"
        and node[2].string.value.replace("'", '"') == '"content"',
    ) is not None

    assert body_return, 'Are you returning `self.data["content"]` from `body`?'


@pytest.mark.test_content_type_property_module3
def test_content_type_property_module3(parse):
    # @property
    # def type(self):
    #     return self.data["type"] if "type" in self.data else None
    content = parse("content")
    assert content.success, content.message

    content_class = content.get_by_name("class", "Content")

    assert (
        content_class.exists
    ), "Have you created a class called `Content` in the `content.py` file?"

    type = content.get_by_name("def", "type", content_class.code)
    assert (
        type.exists
    ), "Have you created a class method called `type` in the `Content` class?"

    self_arg = content.get_by_value("def_argument", "self", type.code)
    assert self_arg.exists, "Does the `type` method have a `self` argument?"

    decorator_exists = type.code.decorators.dotted_name.name.value == "property"
    assert (
        decorator_exists
    ), "Does the `type` method have a decorator of `@property`?"

    type_return = type.code.return_.find(
        "atomtrailers",
        lambda node: len(node) == 3
        and node[0].name.value == "self"
        and node[1].name.value == "data"
        and node[2].string.value.replace("'", '"') == '"type"',
    ) is not None

    assert type_return, 'Are you returning `self.data["type"]` from `type`?'

    # TODO: Add tests for the id statement

    assert False

"""
@pytest.mark.test_content_type_setter_module3
def test_type_content_setter_module3(parse):
    # @type.setter
    # def type(self, type):
    #     self.data["type"] = type
    content = parse("content")
    assert content.success, content.message

    assert False


@pytest.mark.test_content_getitem_module3
def test_content_getitem_module3(parse):
    # def __getitem__(self, key):
    #     return self.data[key]
    content = parse("content")
    assert content.success, content.message

    assert False


@pytest.mark.test_content_iter_module3
def test_content_iter_module3(parse):
    # def __iter__(self):
    #     self.data.__iter__(parse)
    content = parse("content")
    assert content.success, content.message

    assert False


@pytest.mark.test_content_len_module3
def test_content_len_module3(parse):
    # def __len__(self):
    #     return len(self.data)
    content = parse("content")
    assert content.success, content.message

    assert False


@pytest.mark.test_content_repr_module3
def test_content_repr_module3(parse):
    # def __repr__(self):
    #     data = {}
    #     return str(data)
    content = parse("content")
    assert content.success, content.message

    assert False


@pytest.mark.test_content_repr_for_loop_module3
def test_content_repr_for_loop_module3(parse):
    # for key, value in self.data.items(parse):
    #     if key != "content":
    #         data[key] = value
    content = parse("content")
    assert content.success, content.message

    assert False
"""
