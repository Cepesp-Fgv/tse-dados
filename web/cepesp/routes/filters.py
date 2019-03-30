import os

from flask import url_for


def dated_url_for(endpoint, root_path, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)

    return url_for(endpoint, **values)


def asset_filter(fl, root_path):
    return dated_url_for('static', root_path, filename=fl)
