# -*- coding: utf-8 -*-

from gluon.validators import IS_IN_DB, IS_SLUG, IS_IN_SET, IS_NOT_IN_DB, IS_NOT_EMPTY, IS_INT_IN_RANGE
from gluon.dal import Field
from functools import wraps

class DataBase(object):
    def __init__(self, db=None, auth=None, request=None, tables=['all']):
        self.request = request
        self.db = db
        self.auth = auth
        self.__define_table(tables)

    def __define_table(self, tables):
	# by default all, Good for the firts request
        if tables[0] == 'all':
            tables = []
            for item in dir(self):
                if item.startswith('_t_'):
                    tables.append(item[1:])
        for table in tables:
            if table not in self.db.tables:
                run = getattr(self, '_'+table)
                run()

    def _depends_on(*args):
        def _define(f):
            def _decorator(self):
                for table in args:
                    if table not in self.db.tables:
                        run = getattr(self, '_'+table)
                        run()
                    #self.__define_table(table)
                f(self)
            return wraps(f)(_decorator)
        return _define


    def _t_post(self):
        self.db.define_table('t_post',
            Field('f_user_id', 'reference auth_user', default=self.auth.user_id, writable=False, readable=False),
            Field('f_description', 'text'),
            )

    @_depends_on('t_post')
    def _t_comment(self):
        self.db.define_table('t_comment',
            Field('f_user_id', 'reference auth_user', default=self.auth.user_id, writable=False, readable=False),
            Field('f_post_id', 'reference t_post'),
            Field('f_comment', 'text'),
            Field('f_created_on', 'datetime', default=self.request.now, writable=False),
            )

    def _t_docs(self):
        self.db.define_table('t_docs',
            Field('f_title', 'string'),
            Field('f_description', 'text'),
            )
   

