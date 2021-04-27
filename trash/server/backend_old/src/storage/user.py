from sqlalchemy.orm import Session
from ..models.user import User

def add(dbsession: Session, user: User):
    dbsession.add(user)