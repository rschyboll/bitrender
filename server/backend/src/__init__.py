from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_debugtoolbar')
    config.include('.models')
    config.include(".resources")
    config.include(".security")
    config.include(".services")
    return config.make_wsgi_app()