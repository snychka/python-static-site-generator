from pathlib import Path


class Site:
    def __init__(self, source, dest, parsers=None):
        self.source = Path(source)
        self.dest = Path(dest)
        self.parsers = parsers or []

    def create_root(self):
        self.dest.mkdir(parents=True, exist_ok=True)

    def create_dir(self, path):
        directory = self.dest / path.relative_to(self.source)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

    def load_parser(self, extension):
        for parser in self.parsers:
            if parser.valid_extension(extension):
                return parser

    def run_parser(self, path):
        parser = self.load_parser(path.suffix)
        if parser is not None:
            parser.parse(path, self.dest)
        else:
            print('Error')

    def build(self):
        self.create_root()
        for path in self.source.rglob('*'):
            if path.is_dir():
                self.create_dir(path)
            elif path.is_file():
                self.run_parser(path)