from _csv import QUOTE_ALL
from io import BytesIO
import pandas as pd
from flask import send_file


class ResponseConverter:

    _mime = {
        'json': 'application/json',
        'csv': 'text/csv'
    }

    def __init__(self, name=None):
        self._name = name

    def to_stream(self, stream, s_format='csv'):
        name = self._name + '.' + s_format
        return send_file(stream, mimetype=self._mime[s_format], attachment_filename=name, as_attachment=True)

    def to_json(self, result: pd.DataFrame, start_offset: int = 0):
        total = start_offset + (len(result) * 2)
        data = result.to_json(orient='records')
        response = "{\"draw\": 0, \"recordsTotal\": %d, \"recordsFiltered\": %d, \"error\": null, \"data\": %s}" % (
            total,
            total,
            data
        )

        return self.to_stream(BytesIO(response.encode('utf-8')), 'json')

    def to_csv(self, result: pd.DataFrame, separator) -> str:
        stream = BytesIO()
        result.to_csv(stream, header=True, index=False, encoding='utf8', sep=separator, quoting=QUOTE_ALL)

        return self.to_stream(stream, 'csv')
