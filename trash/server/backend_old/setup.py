from setuptools import setup

requires = [
    'fastapi'
]

dev_requires = []

setup(
    name='rendering_server',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = src:main'
        ]
    },
)