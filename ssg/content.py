import re
import yaml

from collections.abc import Mapping

class Frontmatter:

    __delimiter = r'^(?:-|\+){3}\s*$'
    __regex = re.compile(__delimiter, re.MULTILINE)

    @classmethod
    def load(cls, string):
        _, fm, content = cls.__regex.split(string, 2)
        metadata = yaml.load(fm, Loader=yaml.FullLoader)

        return Content(metadata, content)

class Content(Mapping):

    def __init__(self, metadata, content):
        self.data = metadata
        self.data['content'] = content

    @property
    def body(self):
        return self.data['content']

    @property
    def type(self):
        return self.data['type'] if 'type' in self.data else None

    @type.setter
    def type(self, type):
        self.data['type'] = type

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def __iter__(self):
        self.data.__iter__()

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return '{}'.format(self.data)
