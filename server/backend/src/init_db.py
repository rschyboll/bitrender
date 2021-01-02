import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .models.user import User

def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('config_uri', help="development.ini")
    return parser.parse_args(argv[1:])

def add_users(dbsession):
    admin = User(login='admin', password='test', email="robin.schyboll@gmail.com", register_date='01.01.2021')
    test = User(login='test', password='test', email="test.test@test.com", register_date='01.01.2021')
    dbsession.add(admin)
    dbsession.add(test)

def main(argv=sys.argv):
    args = parse_args(argv)
    env = bootstrap(args.config_uri)
    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            add_users(dbsession)
    except OperationalError:
        print("""Your database server may not be running.  Check that the
              database server referred to by the "sqlalchemy.url" setting in
              your "development.ini" file is running.""")