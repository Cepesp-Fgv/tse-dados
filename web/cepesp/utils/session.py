from flask import session, request


def get_selected_columns_session_key():
    base = request.path.split('/')[-1]
    reg = str(request.args.get('agregacao_regional'))
    pol = str(request.args.get('agregacao_politica'))

    key = 'columns_' + base
    if reg:
        key += '_' + reg

    if pol:
        key += '_' + pol

    return key


def set_session_selected_columns(columns):
    key = get_selected_columns_session_key()
    session[key] = columns


def session_selected_columns(available_columns):
    key = get_selected_columns_session_key()

    if key in session:
        return [c for c in session[key] if c in available_columns]
    else:
        return []


def back(default='/'):
    return session.get('back', default)


def get_locale():
    return session.get('locale', 'pt')
