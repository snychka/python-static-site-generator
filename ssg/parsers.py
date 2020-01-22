import os
import shutil

from pathlib import Path

from markdown import markdown


class Parser:
    extensions = []

    def valid_extension(self, extension):
        return extension in self.extensions

    def parse(self, path, dest):
        raise NotImplementedError

    def read(self, path):
        with open(path, 'r') as file:
            return file.read()

    def write(self, path, dest, content, ext='.html'):
        full_path = dest / path.with_suffix(ext).name
        with open(full_path, 'w') as file:
            file.write(content)

    def copy(self, path, dest):
        pass


class MarkdownParser(Parser):

    extensions = ['.md']

    def parse(self, path, dest):
        content = markdown(self.read(path))
        self.write(path, dest, content)


class ResourceParser(Parser):

    extensions = ['.jpg', '.png', '.gif', '.css', '.html']

    def parse(self, path, dest):
        self.copy(path, dest)