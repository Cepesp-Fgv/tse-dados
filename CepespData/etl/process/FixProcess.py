import os
from _csv import QUOTE_ALL

import inflection as inflection
import pandas as pd


class FixProcess:

    def __init__(self, fixes, output):
        self.fixes = fixes
        self.output = output
        self.items = []

    def fix_name(self, i):
        return inflection.underscore(self.fixes[i].__class__.__name__)

    def get_item_file(self, item, i):
        if 1 <= i < len(self.fixes):
            path = os.path.join(self.output, self.fix_name(i), item['name'])
            if not os.path.exists(path):
                return self.get_item_file(item, i - 1)
            else:
                return path
        else:
            return item['path']

    def get_item_df(self, item, i):
        path = self.get_item_file(item, i)
        return pd.read_csv(path, sep=';', dtype=str)

    def save_fix_df(self, item, df, i):
        path = os.path.join(self.output, self.fix_name(i), item['name'])
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        df.to_csv(path, compression='gzip', sep=';', encoding='utf-8', index=False, quoting=QUOTE_ALL)

    def apply_fix(self, item, i):
        if not self.fix_done(item, i) and self.fixes[i].check(item):
            print("STEP %s on %s" % (self.fix_name(i), item['name']))

            df = self.get_item_df(item, i - 1)
            df = self.fixes[i].apply(df)
            self.save_fix_df(item, df, i)

    def output_files(self):
        files = []
        for item in self.items:
            files.append(self.get_item_file(item, len(self.fixes) - 1))
        return files

    def handle(self, item):
        self.items.append(item)
        for i in range(len(self.fixes)):
            self.apply_fix(item, i)

    def fix_done(self, item, i):
        path = os.path.join(self.output, self.fix_name(i), item['name'])
        return os.path.exists(path)
