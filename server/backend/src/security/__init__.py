from pyramid.authorization import ACLAuthorizationPolicy

def includeme(config):
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include('pyramid_jwt')
    config.set_jwt_cookie_authentication_policy(callback = add_role_principals)


def add_role_principals(userid, request):
    return ['role:%s' % role for role in request.jwt_claims.get('roles', [])]