# -*- coding: utf-8 -*-
from collections import OrderedDict
from gluon.html import URL



def paginate(db, args, vars, max_items, query, arguments, fields):
    r = OrderedDict()
    limitby = [0, max_items+1]
    for key, value in vars.items():
            if key == '_offset':
                limitby[0] = int(value)  # MAY FAIL
            elif key == '_limit':
                limitby[1] = int(value)+1  # MAY FAIL

    arguments["limitby"] = limitby
    rows = db(query).select(*fields, **arguments)

    delta = limitby[1]-limitby[0]-1

    data = []
    for row in rows[:delta]:
        data.append(row)

    # Create the output
    r['items'] = {
            'data': data,
            }

    if len(rows) > delta:
        #vars = dict(request.get_vars)
        vars['_offset'] = limitby[1]-1
        vars['_limit'] = limitby[1]-1+delta
        r['next'] = {'rel': 'next',
                     'href': URL(args=args, vars=vars, scheme=True)}

    if limitby[0] > 0:
        #vars = dict(request.get_vars)
        vars['_offset'] = max(0,limitby[0]-delta)
        vars['_limit'] = limitby[0]
        r['previous'] = {'rel': 'previous',
                         'href': URL(args=args, vars=vars, scheme=True)}

    return r

