from setuptools import setup

requires = [
    'pyramid',
    'cornice',
    'sqlalchemy',
    'pyramid_tm',
    'pyramid_retry',
    'zope.sqlalchemy',
    'psycopg2',
    'pyramid_jwt'
]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest',
    'sqlacodegen'
]

setup(
    name='rendering_server',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = src:main'
        ],
        'console_scripts': [
            'rendering_server_init_db = src.init_db:main'
        ],

    },
)