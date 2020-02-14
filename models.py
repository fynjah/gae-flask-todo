from google.cloud import ndb


class Todo(ndb.Model):
    title = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    checked = ndb.BooleanProperty(default=False)