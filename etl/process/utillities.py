import pandas as pd


def resolve_conflicts(df, prefer='_x', drop='_y') -> pd.DataFrame:
    columns = df.columns.values.tolist()
    conflicts = [c for c in columns if c.endswith(prefer)]
    drops = [c for c in columns if c.endswith(drop)]
    renames = dict()
    for c in conflicts:
        renames[c] = c.replace(prefer, '')

    return df.rename(columns=renames).drop(drops, axis=1)
