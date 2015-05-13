# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

# Check security access
if not auth.user:
    redirect(URL(request.application, 'default', 'user', args=['login'],
                  vars=dict(_next=URL(args=request.args, vars=request.vars))))

from post import Post, add_json_head
from docs import Doc, add_json_head

def index():
    post = Post(db, auth)
    response.view = '%s/admin/manage.html' % myconf.take('general.theme')
    return dict(grid=post.grid())
  
def comment():
    post = Post(db, auth)
    print "defined tables:" + str(db.tables())
    return response.json({'collection': add_json_head(post.get_comment(), response)})
  
def docs():
    doc = Doc(db, auth)
    print "defined tables:" + str(db.tables())
    return response.json({'collection': add_json_head(doc.get_doc(), response)})

def populate_database():
  from model import DataBase
  DataBase(db=db, auth=auth, request=request, tables=['all'])
  from gluon.contrib.populate import populate
  skip = ['auth_group', 'auth_permission', 'auth_cas', 'auth_event']
  import time
  try:
      for table in db.tables():
	  if table not in skip:
	      print 'populating ' + table
	      populate(db.__getattr__(table), 50)
	      #population is done in a transaction, we need to commit to get the references
	      db.commit()
	      time.sleep(1)
  except Exception as e:
      print str(e)
  return "Done"
      

