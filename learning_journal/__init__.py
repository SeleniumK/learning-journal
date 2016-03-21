from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import os

from wtforms import Form, BooleanField, StringField, validators

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    database_url = os.environ.get('DATABASE_URL', None)
    if database_url is not None:
        settings['sqlalchemy.url'] = database_url
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('entry', '/entry/{entry}')
    config.add_route('add_entry', '/entry/write')
    config.add_route('edit_entry', '/entry/{entry}/edit')
    config.scan()
    return config.make_wsgi_app()
