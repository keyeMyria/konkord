import re
from urllib.parse import quote, unquote
from django.http import QueryDict



FIELDS_MATCH = re.compile('[;]')

def query_to_dict(query, existing_dict=None, prepared=False):
    """Takes custom query string and returns QueryDict"""

    if existing_dict is None:
        existing_dict = {}

    SINGLE_KEYS = {'paginate_by', 'sort_by'}
    save_filters = (SINGLE_KEYS & set(existing_dict.keys())) or prepared

    if existing_dict:
        d = existing_dict.copy()
    else:
        d = QueryDict(mutable=True)

    pairs = FIELDS_MATCH.split(query)

    for name_value in pairs:
        nv = name_value.split(':', 1)
        if len(nv) == 2:
            if (save_filters and (nv[0] not in SINGLE_KEYS or nv[0] not in d))\
                    or (not save_filters and nv[0] in SINGLE_KEYS):
                values = unquote(nv[1])
                values = values.split('_')
                for v in values:
                    d.appendlist(nv[0], v)

    return d


def dict_to_query(d):
    """Takes QueryDict and returns custom filter URL"""

    output = []
    exclude_params = {'category_id'}

    lists = sorted(d.lists(), key=lambda i: i[0])

    for k, list_ in lists:
        if k not in exclude_params:
            val = '_'.join(quote(v) for v in list_ if v)
            if val:
                output.extend(['%s:%s' % (k, val)])
    return ';'.join(output)