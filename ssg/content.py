import re
import yaml


class Frontmatter:

    _delimiter = r'^(?:-|\+){3}\s*$'
    _regex = re.compile(_delimiter, re.MULTILINE)

    @classmethod
    def load(cls, string):
        _, fm, content = cls._regex.split(string, 2)
        metadata = yaml.load(fm, Loader=yaml.FullLoader)

        type = metadata.get('type', '')
        title = metadata.get('title', '')
        slug = metadata.get('slug', '')
        date = metadata.get('date', '')
        author = metadata.get('author', '')
        
        if type == 'page':
            return Page(type, title, content, slug)
        elif type == 'post':
            return Post(type, title, content, date, author)
        else:
            return Content('plain', title, content)

class Content:

    count = 0

    def __init__(self, type, title, content):
        self._type = type
        self._title = title
        self._content = content
        Content.count += 1

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    def __repr__(self):
        return 'Title: {}\nType: {}\n'.format(self._title, self._type)


class Page(Content):

    count = 0

    def __init__(self, type, title, content, slug):
        super().__init__(type, title, content)
        self._slug = slug
        Page.count += 1

    @property
    def slug(self):
        return self._slug

    @slug.setter
    def slug(self, slug):
        self._slug = slug

    def __repr__(self):
         return '{}Slug: {}\n'.format(super().__repr__(), self._slug)

class Post(Content):

    count = 0

    def __init__(self, type, title, content, date, author):
        super().__init__(type, title, content)
        self._date = date
        self._author = author
        Post.count += 1

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author

    def __repr__(self):
        return '{}Date: {}\nAuthor: {}\n'.format(super().__repr__(), self._date, self._author)
