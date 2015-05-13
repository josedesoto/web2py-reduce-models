# -*- coding: utf-8 -*-
from gluon.globals import current
from model import DataBase
from collections import OrderedDict
from utils import paginate
from gluon.html import URL
from gluon.sqlhtml import SQLFORM


VERSION = 1.0

def add_json_head(data, response):
    r = OrderedDict()
    r['version'] = VERSION
    r.update(data)
    response.headers['Content-Type'] = 'application/vnd.collection+json'
    return r

class Doc(object):

    def __init__(self, db, auth=None, define_tables=True):
        self.request = current.request
        self.cache = current.cache
        self.db = db
        self.auth = auth
        self.MAXITEMS = 2
        if define_tables:
            DataBase(db=self.db, auth=self.auth, request=self.request, tables=['t_docs'])
            

    def get_doc(self):
        """It will return a json with the psy favorites.
        Args:
            vars (dict): it can contain the field you want order the list: _orderby

        Returns: If successful, this method returns a response body with the following structure:

                    auth_user: {
                    first_name: "Charlesetta",
                    last_name: "Bambas",
                    f_photo: "None"
                    },
                    t_psychologist: {
                    f_ranking: 3,
                    id: 17
                    }
        """

        fields = [self.db.t_docs.id, self.db.t_docs.f_title, self.db.t_docs.f_description]
        orderby_filter=["f_title"]

        if self.request.vars['_orderby'] in orderby_filter:
            orderby = self.request.vars['_orderby']
        else:
            orderby = 'id'

        arguments = dict()
        arguments["orderby"] = self.db.t_docs.__getattr__(orderby)

        query = (self.db.t_docs.id > 0)

        return paginate(self.db, self.request.args, self.request.vars, self.MAXITEMS, query, arguments, fields)
