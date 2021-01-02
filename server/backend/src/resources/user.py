from cornice.resource import resource
from ..models.user import User


@resource(collection_path='user', path='user/{id}')
class UserResource(object):
    def __init__(self, request, context=None):
        self.request = request

    def get(self):
        query = self.request.dbsession.query(User)
        user = query.filter(User.id == self.request.matchdict['id'])
        return {}
