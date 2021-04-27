from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_debugtoolbar')
    config.include('.services')
    config.include('.resources')
    config.include('.models')
    config.include('.errors')
    return config.make_wsgi_app()
