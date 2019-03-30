import re


class Builder:

    def __init__(self, **options):
        self.options = options
        self.rx = re.compile(r'[!?\\/\-\&\*\%\$\#\"\']+', flags=re.M | re.I)

    def trim(self, value):
        return re.sub('(\r|\n| )+', ' ', value).strip()

    def escape(self, value):
        return self.rx.sub('', value)

    def opt(self, key, default=None):
        return self.options[key] if key in self.options else \
            default

    def arg(self, key):
        if key not in self.options:
            raise KeyError(f'No argument {key} supplied')

        return self.options[key]
