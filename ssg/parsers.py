import os
import shutil

from pathlib import Path

from markdown import markdown
from docutils.core import publish_parts


class Parser:

    extensions = []

    def valid_extension(self, extension):
        return extension in self.extensions

    def parse(self, path, source, dest):
        raise NotImplementedError

    def read(self, path):
        with open(path, 'r') as file:
            return file.read()

    def write(self, path, dest, content, ext='.html'):
        full_path = dest / path.with_suffix(ext).name
        with open(full_path, 'w') as file:
            file.write(content)

    def copy(self, path, source, dest):
        shutil.copy2(path, dest / path.relative_to(source))


class MarkdownParser(Parser):

    extensions = ['.md', '.markdown']

    def parse(self, path, source, dest):
        content = markdown(self.read(path))
        self.write(path, dest, content)


class ReStructuredTextParser(Parser):

    extensions = ['.rst']

    def parse(self, path, source, dest):
        content = publish_parts(self.read(path), writer_name='html5')
        self.write(path, dest, content['html_body'])


class ResourceParser(Parser):

    extensions = ['.jpg', '.png', '.gif', '.css', '.html']

    def parse(self, path, source, dest):
        self.copy(path, source, dest)
