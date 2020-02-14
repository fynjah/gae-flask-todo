from google.cloud import ndb


class Todo(ndb.Model):
    title = ndb.StringProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
    checked = ndb.BooleanProperty(default=False)
    userid = ndb.StringProperty()

    @classmethod
    def query_by_user(self, userid):
        return self.query(Todo.userid == userid).order(-self.timestamp)