## Import pathlib
[//]: # (@pytest.mark.test_site_path_import_module1)
```
from pathlib import Path
```
In this module we'll build up a `Site` Class that will set configuration values and create the root structure of our static site. We'll also create a command line tool using the `Typer` library. Since we are going to be working with paths let's import `pathlib`, which is part of the standard library.

Open the `site.py` located in the `ssg` directory. At the top import `Path` from `pathlib`.

## Create a Class
[//]:#(@pytest.mark.test_site_class_module1)
```
class Site:
    def __init__(self, source, dest):
        self.source = Path(source)
        self.dest = Path(dest)
```
Below the import you just wrote, create a class called `Site`. Next, create a `Site` class constructor that accepts three arguments `self`, `source`, and `dest`.
In the constructor wrap both `source`, and `dest` with a call to `Path()`. Assign the results of these calls to class attributes with the same names using `self`.


## Find Root Directory
[//]:#(@pytest.mark.test_site_create_dir_function_module1)
```
def create_dir(self, path):
    directory = self.dest / path.relative_to(self.source)
```
Still in the `Site` class create a method called `create_dir` that accepts two arguments `self`, and `path`.
In the body of the `create_dir` method assign a variable called `directory` a `pathlib` path that has two parts. 
It should start with `self.dest` and end with a `path` `relative_to` `self.source`.


## Make a Directory
[//]:#(@pytest.mark.test_site_create_dir_mkdir_module1)
```
directory.mkdir(parents=True, exist_ok=True)
```
On a new line in the `create_dir` method, call the `mkdir` method on `directory`. For our scenario we want `directory` to be replaced if it exists.
Pass the following keyword arguments to `mkdir`:

  - `parents` set to `True`
  - `exist_ok` set to `True`


## Make the Destination Directory
[//]:#(@pytest.mark.test_site_build_function_module1)
```
def build(self):
    self.dest.mkdir(parents=True, exist_ok=True)
```
Create a new method called `build` in the `Site` class. Call the `mkdir` method on `self.dest`.
As with other `mkdir` calls, pass the following keyword arguments to `mkdir`:

  - `parents` set to `True`
  - `exist_ok` set to `True`


## Recreate all Paths
[//]:#(@pytest.mark.test_site_path_rglob_module1)
```
for path in self.source.rglob("*"):
    if path.is_dir():
        self.create_dir(path)
```
Still in the `build` method, create a `for` loop that iterates through the paths of `self.source.rglob(*)`.
Call the current iteration `path`. In the body of the `for` loop test `if` the current `path` is a directory.
If it is a directory call the `create_dir` method of the class and pass in the current `path`.


## Import Typer
[//]:#(@pytest.mark.test_ssg_imports_module1)
```
import typer
from ssg.site import Site
```
Lets setup the command line interface (CLI), open the `ssg.py` file in the root directory of the project.
At the top import `typer`. Also, import the `Site` class from `ssg.site`.


## Configuration Options
[//]:#(@pytest.mark.test_ssg_main_command_module1)
```
def main(source="content", dest="dist"):
    config = {
        "source": source,
        "dest": dest
    }
```
The Typer library requires a function to run that captures command line arguments.
We'll call this function `main`. It should accept two keyword arguments, `source` with a default value of `"content"` and `dest` with a default value of `"dist"`.
In the body of the `main` function create a dictionary called `config`. Add two key value pairs to `config`, `"source"` set to `source`, and `"dest"` set to `dest`.


## Build the Site
[//]:#(@pytest.mark.test_ssg_build_call_module1)
```
Site(**config).build()
```
Still in the `main` function, create an instance of the `Site` class. The `Site` class requires that you provide two attributes `source` and `dest` when creating an instance. These are currently store in the `config` dictionary as key value pairs. Unpack these dictionary values with `**` and pass it to the `Site` instance. Finally, chain a call to the `build()` method on this instance.


## Run Typer
[//]:#(@pytest.mark.test_ssg_typer_run_module1)
```
typer.run(main)
```
At the bottom of the file, `typer.run()` the `main` function.


## Parser Class
[//]:#(@pytest.mark.test_parser_base_class_module2)
```
from typing import List

class Parser:
    extensions: List[str] = []
```
In this module we will create a `Parser` base class that will have several functions that will help when converting Markdown and ReStructuredText to HTML.
To start, open the `ssg/parsers.py` file. We will add a few type annotations and one requires an import. Import `List` from `typing`. Also, import `Path` from `pathlib`.
Next, create a class called `Parser`. Create a variable called `extensions` and assign it an empty list. Annotate `extensions` with the type `List[str]`.


## Validate Extensions
[//]:#(@pytest.mark.test_parser_valid_extension_function_module2)
```
def valid_extension(self, extension):
    return extension in self.extensions
```
We will need to know whether certain files have a parser. This will be done by looking at the extension.
Create a new method in the `Parser` class called `valid_extension`. This method should accept an `extension`
and return whether or not that `extension` is `in` the class variable `self.extensions`.
**Hint: This method is part of the `Parser` methods so it should accept self as an argument.**


## Base parse method
[//]:#(@pytest.mark.test_parser_parse_function_module2)
```
def parse(self, path: Path, source: Path, dest: Path):
    raise NotImplementedError
```
Since the `Parser` class is a base class we will create a method that will be overwritten in a Sub-class.
Call this method `parse`, it should accept a `path`, `source`, and `dest`. Annotate each of these with the `Path` type.
In the body `raise` the `NotImplementedError`.

## Parser read method
[//]:#(@pytest.mark.test_parser_read_function_module2)
```
def read(self, path):
    with open(path, "r") as file:
        return file.read()
```
The `Parser` class with need to be able to read the contents of a file. Create a method called `read` that accepts a `path`.
Use a `with` statement and a call to `open()` to open `path` for reading `as` `file`.
In the body of the `with` statement `return` a what is `read()` from `file`.

## Parser write method
[//]:#(@pytest.mark.test_parser_write_function_module2)
```
def write(self, path, dest, content, ext=".html"):
    full_path = dest / path.with_suffix(ext).name
```
Still in the `Parser` class create a method called `write` that accepts the following arguments `path`, `dest`, and `content`.
Also, add a keyword argument called `ext` with a default value of `".html"`.
In the body of the method assign a variable called `full_path` a `pathlib` path that has two parts. 
It should start with `dest` and end with the `name` of the `path` `with_suffix()` of `ext`.


## Open file for writing
[//]:#(@pytest.mark.test_parser_write_function_open_module2)
```
with open(full_path, "w") as file:
    file.write(content)
```
Still in the `write` method use `with` and `open()` to open `path` for writing `as` `file`.
In the body of the `with` statement `write` `content` to `file`.


## Parser copy method
[//]:#(@pytest.mark.test_parser_copy_function_module2)
```
import shutil
def copy(self, path, source, dest):
    shutil.copy2(path, dest / path.relative_to(source))
```
Move back to the top of the page and import `shutil`. We'll this use this library to copy resources to the correct location.
Below the exiting methods in the `Parser` class create a new method called `copy`. This method should accept the following arguments `path`, `source`, and `dest`.
Use `copy2` from `shutil` to copy the file at `path` to the root of `dest` with a second `path` `relative_to` `source`.


## ResourceParser subclass
[//]:#(@pytest.mark.test_parser_resource_class_module2)
```
class ResourceParser(Parser):
    extensions = [".jpg", ".png", ".gif", ".css", ".html"]

    def parse(self, path, source, dest):
        self.copy(path, source, dest)
```
Create a class called `ResourceParser` that is a sub-class of `Parser`. Next, create a `Site` class constructor that accepts three arguments `self`, `source`, and `dest`.
In the constructor wrap both `source`, and `dest` with a call to `Path()`. Assign the results of these calls to class attributes with the same names using `self`.
Create a variable called `extensions` and assign it a list with 5 extensions, `".jpg"`, `".png"`, `".gif"`, `".css"`, and `".html"`.

Implement the `parse` method in the `ResourceParser` class. It should have the same signature as in the base class.
In the body, call the `copy` method that is part of the class because we inherited from `Parser`.
Pass in the `path`, `source` and `dest`.


## Available Parsers
[//]:#(@pytest.mark.test_site_parsers_module2)
```
, parsers=None
self.parsers = parsers or []
```
Open `ssg/site.py` and add a keyword argument to the constructor called `parsers` set to `None`.
In the body of the constructor, set a new class attribute called `parsers` to `parsers` `or` an empty list.

## Parser Configuration
[//]:#(@pytest.mark.test_ssg_config_parser_module2)
```
import ssg.parsers
"parsers": [
    ssg.parsers.ResourceParser(),
],
```
Open `ssg.py`, at the top import `ssg.parsers`. Add a new key value pair to the `config` dictionary in the `main` function.
The key should be `"parsers"` and the value should be a list with a single element of `ssg.parsers.ResourceParser()`.


## Site class load parser method
[//]:#(@pytest.mark.test_site_load_parser_module2)
```
def load_parser(self, extension):
    for parser in self.parsers:
        if parser.valid_extension(extension):
            return parser
```
Back in `ssg/site.py` add a new method to the `Site` class called `load_parser` below the existing methods. This method should accept an argument called `extension`.
The first statement in the method should be a `for` loop that cycles through `self.parsers`. Call the current loop value `parser`. 
The body should have an `if` statement that tests if `extension` is a `valid_extension`. **Hint: `parser` is an instance of the correct Parser class. So it will have a method of `valid_extension`.** Return `parser` in the `if` statement.


## Site class run parser method
[//]:#(@pytest.mark.test_site_run_parser_module2)
```
def run_parser(self, path):
    parser = self.load_parser(path.suffix)
```
Still in the `Site` class, add a new method called `run_parser`. This method should accept an argument called `path`.
In the method call `load_parser` passing in `path.suffix`, save the result to a variable called `parser`.


## Call the parse method
[//]:#(@pytest.mark.test_site_run_parser_if_module2)
```
if parser is not None:
    parser.parse(path, self.source, self.dest)
else:
    print('Not Implemented')
```
Still in the `run_parser` method test if `parser` is not `None`. If parser is not `None` then call the `parse` method of `parser`.
Pass in the `path` and the `Site` class attributes of `source` and `dest`. In an else print the message `Not Implemented`.


## Run the parser
[//]:#(@pytest.mark.test_site_build_elif_module2)
```
elif path.is_file():
    self.run_parser(path)
```
To connect everything together find the `if` statement in the `build` method. Add an `elif` that tests whether `path` is a file.
If `path` is a file then call `run_parser` passing in `path`. **Hint: run_parser is part of the `Site` class.**

## Imports
[//]:#(@pytest.mark.test_content_imports_module3)
```
import re

from collections.abc import Mapping

from yaml import load, FullLoader
```
In this module we will extract YAML frontmatter from files in our site. We this will be done by spliting the contents of the file. This will require the use of regular expressions. Import `re` from the standard library. We will also need `Mapping` from `collections.abc`. Finally, import `load` and `FullLoader` from `yaml`.

## Content class
[//]:#(@pytest.mark.test_content_class_module3)
```
class Content(Mapping):
    __delimiter = r"^(?:-|\+){3}\s*$"
    __regex = re.compile(__delimiter, re.MULTILINE)
```


## The load class method
[//]:#(@pytest.mark.test_content_classmethod_load_module3)
```
@classmethod
def load(cls, string):
    _, fm, content = cls.__regex.split(string, 2)
    metadata = load(fm, Loader=FullLoader)

    return cls(metadata, content)
```


## Content constructor
[//]:#(@pytest.mark.test_content_init_module3)
```
def __init__(self, metadata, content):
    self.data = metadata
    self.data["content"] = content
```


## Body property
[//]:#(@pytest.mark.test_content_body_property_module3)
```
@property
def body(self):
    return self.data["content"]
```


## Type property
[//]:#(@pytest.mark.test_content_type_property_module3)
```
@property
def type(self):
    return self.data["type"] if "type" in self.data else None
```


## Type setter
[//]:#(@pytest.mark.test_content_type_setter_module3)
```
@type.setter
def type(self, type):
    self.data["type"] = type
```


## Custom getitem method
[//]:#(@pytest.mark.test_content_getitem_module3)
```
def __getitem__(self, key):
    return self.data[key]
```


## Custom iterator method
[//]:#(@pytest.mark.test_content_getitem_module3)
```
def __iter__(self):
    self.data.__iter__()
```


## Custom length method
[//]:#(@pytest.mark.test_content_len_module3)
```
def __len__(self):
    return len(self.data)
```


## Content Representation
[//]:#(@pytest.mark.test_content_repr_module3)
```
def __repr__(self):
    data = {}
    return str(data)
```


## Removing content from the Representation
[//]:#(@pytest.mark.test_content_repr_for_loop_module3)
```
for key, value in self.data.items():
    if key != "content":
        data[key] = value
```


## Markdown and ReStructuredText Imports
[//]:#(@pytest.mark.test_parser_imports_module4)
```
from docutils.core import publish_parts
from markdown import markdown

from ssg.content import Content
```


## Markdown Parser
[//]:#(@pytest.mark.test_parser_markdown_class_module4)
```
class MarkdownParser(Parser):
    extensions = [".md", ".markdown"]
```


## Markdown parse method
[//]:#(@pytest.mark.test_parser_markdown_parse_module4)
```
def parse(self, path, source, dest):
    content = Content.load(self.read(path))
```


## Converting markdown to html
[//]:#(@pytest.mark.test_parser_markdown_parse_write_html_module4)
```
html = markdown(content.body)
self.write(path, dest, html)
```


## ReStructuredText Parser
[//]:#(@pytest.mark.test_parser_restructuredtext_class_module4)
```
class ReStructuredTextParser(Parser):
    extensions = [".rst"]
```


## ReStructuredText parse method
[//]:#(@pytest.mark.test_parser_restructuredtext_parse_module4)
```
def parse(self, path, source, dest):
    content = Content.load(self.read(path))
```


## Converting ReStructuredText to html
[//]:#(@pytest.mark.test_parser_restructuredtext_parse_write_html_module4)
```
html = publish_parts(content.body, writer_name="html5")
self.write(path, dest, html["html_body"])
```


## Error reporting static method
[//]:#(@pytest.mark.test_site_staticmethod_module4)
```
import sys

@staticmethod
def error(message, end="\n"):
    sys.stderr.write("\x1b[1;31m" + message.strip() + "\x1b[0m" + end)
```


## Calling the error static method
[//]:#(@pytest.mark.test_site_error_call_module4)
```
self.error(
    "No parser for the `{}` extension, file skipped!".format(
        path.suffix
    )
)
```
