import re
import yaml


class Frontmatter:

    _delimiter = r'^(?:-|\+){3}\s*$'
    _regex = re.compile(_delimiter, re.MULTILINE)

    @classmethod
    def load(cls, string):
        _, fm, content = cls._regex.split(string)
        return yaml.load(fm, Loader=yaml.FullLoader), content

class Content:
    pass


class Page(Content):
    pass


class Post(Content):
    pass
