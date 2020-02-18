from google.cloud import ndb


class Todo(ndb.Model):
    '''
    Datastore Todo model.
    Stores userid as string, 'cause user ids from google are too big :)
    '''
    title = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    checked = ndb.BooleanProperty(default=False)
    userid = ndb.StringProperty()