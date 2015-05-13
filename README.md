#Less models

By default in web2py the table definition is done in the models. Models are executed in each request, so if you have many tables defined, these will be loaded  even if you do no need it. In this small app you can see how the models have been defined in a class into the module folder and only load or define the tables you need for each request.

The example below will define the table “comments” and “post”. This is done because there is a dependency between them.
```
from model import DataBase
DataBase(db=self.db, auth=self.auth, request=self.request, tables=['t_comments'])
```

The example below, only will define the table “docs”
```
from model import DataBase
DataBase(db=self.db, auth=self.auth, request=self.request, tables=['t_docs'])
```

If you do not specify any table, by default the module will define all. This is good for the first request of the app or even if you want to populate the entire database.
```
DataBase(db=self.db, auth=self.auth, request=self.request) 
```

Example of the app where you test a few options:

![Alt text](./less_models.png?raw=true "Example of the app")

Example loading the "t_docs" table content. In the terminal you can see only "t_docs" is loaded. "t_comments" and "t_post" tables are ignored for this request.

![Alt text](./less_models1.png?raw=true "Json loading docs table")