## Import pathlib
[//]: # (@pytest.mark.test_site_path_import_module1)
```
from pathlib import Path
```
By default, the Werkzeug library logs each request to the console when debug mode is on. Let's disable this default log. Open the `cms/handlers.py` file, below the existing imports, import the `getLogger` method from `logging`. Below the imports, call the `getLogger()` function and pass in the log we need, `'werkzeug'`. Assign the result to a variable named `request_log`. Then, set the `disabled` property of `request_log` to `True`. _Note: Unless otherwise noted, the rest of the tasks in this module happen in the file `cms/handlers.py`._


## Create a Class
[//]:#(@pytest.mark.test_site_class_module1)
```
class Site:
    def __init__(self, source, dest):
        self.source = Path(source)
        self.dest = Path(dest)
```


## Find Root Directory
[//]:#(@pytest.mark.test_site_create_dir_function_module1)
```
def create_dir(self, path):
    directory = self.dest / path.relative_to(self.source)
```


## Make a Directory
[//]:#(@pytest.mark.test_site_create_dir_mkdir_module1)
```
directory.mkdir(parents=True, exist_ok=True)
```


## Make the Destination Directory
[//]:#(@pytest.mark.test_site_build_function_module1)
```
def build(self):
    self.dest.mkdir(parents=True, exist_ok=True)
```


## Recreate all Paths
[//]:#(@pytest.mark.test_site_path_rglob_module1)
```
for path in self.source.rglob("*"):
    if path.is_dir():
        self.create_dir(path)
```


## Import Typer
[//]:#(@pytest.mark.test_ssg_imports_module1)
```
import typer
from ssg.site import Site
```


## Configuration Options
[//]:#(@pytest.mark.test_ssg_main_command_module1)
```
def main(source="content", dest="dist"):
    config = {
        "source": source,
        "dest": dest
    }
```


## Build the Site
[//]:#(@pytest.mark.test_ssg_build_call_module1)
```
Site(**config).build()
```


## Run Typer
[//]:#(@pytest.mark.test_ssg_typer_run_module1)
```
typer.run(main)
```


## Parser Class
[//]:#(@pytest.mark.test_parser_base_class_module2)
```
from typing import List

class Parser:
    extensions: List[str] = []
```


## Validate Extensions
[//]:#(@pytest.mark.test_parser_valid_extension_function_module2)
```
def valid_extension(self, extension):
    return extension in self.extensions
```


## Base parse method
[//]:#(@pytest.mark.test_parser_parse_function_module2)
```
def parse(self, path: Path, source: Path, dest: Path):
    raise NotImplementedError
```


## Parser read method
[//]:#(@pytest.mark.test_parser_read_function_module2)
```
def read(self, path):
    with open(path, "r") as file:
        return file.read()
```


## Parser write method
[//]:#(@pytest.mark.test_parser_write_function_module2)
```
def write(self, path, dest, content, ext=".html"):
    full_path = dest / path.with_suffix(ext).name
```


## Open file for writing
[//]:#(@pytest.mark.test_parser_write_function_open_module2)
```
with open(full_path, "w") as file:
    file.write(content)
```


## Parser copy method
[//]:#(@pytest.mark.test_parser_copy_function_module2)
```
import shutil
def copy(self, path, source, dest):
    shutil.copy2(path, dest / path.relative_to(source))
```


## ResourceParser subclass
[//]:#(@pytest.mark.test_parser_resource_class_module2)
```
class ResourceParser(Parser):
    extensions = [".jpg", ".png", ".gif", ".css", ".html"]

    def parse(self, path, source, dest):
        self.copy(path, source, dest)
```


## Available Parsers
[//]:#(@pytest.mark.test_site_parsers_module2)
```
, parsers=None
self.parsers = parsers or []
```


## Parser Configuration
[//]:#(@pytest.mark.test_ssg_config_parser_module2)
```
import ssg.parsers
"parsers": [
    ssg.parsers.ResourceParser(),
],
```


## Site class load parser method
[//]:#(@pytest.mark.test_site_load_parser_module2)
```
def load_parser(self, extension):
    for parser in self.parsers:
        if parser.valid_extension(extension):
            return parser
```


## Site class run parser method
[//]:#(@pytest.mark.test_site_run_parser_module2)
```
def run_parser(self, path):
    parser = self.load_parser(path.suffix)
```


## Call the parse method
[//]:#(@pytest.mark.test_site_run_parser_if_module2)
```
if parser is not None:
    parser.parse(path, self.source, self.dest)
else:
    print('Not Implemented')
```


## Run the parser
[//]:#(@pytest.mark.test_site_build_elif_module2)
```
elif path.is_file():
    self.run_parser(path)
```


## Imports
[//]:#(@pytest.mark.test_content_imports_module3)
```
import re

from collections.abc import Mapping

from yaml import load, FullLoader
```


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