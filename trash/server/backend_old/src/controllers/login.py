import bcrypt
from typing import Tuple, List, Dict, Any
from pyramid.request import Request

from ..storage import user as UserStorage
from ..models.user import User

def __hashPassword(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def register(request: Request, json_data: Dict[str, Any]) -> Tuple[int, List[str]]:
    password: bytes = __hashPassword(json_data['password'])
    user: User = User(login = json_data['login'], password = password, email=json_data['email'])
    UserStorage.add(request.dbsession, user)
