from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import os
from .models import (
    DBSession,
    Base,
    DefaultRoot,
)
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder
from cryptacular.bcrypt import BCRYPTPasswordManager

def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    database_url = os.environ.get('DATABASE_URL', None)
    if database_url is not None:
        settings['sqlalchemy.url'] = database_url
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    manager = BCRYPTPasswordManager()
    settings['auth.username'] = os.environ.get('auth_username', 'admin')
    settings['auth.password'] = os.environ.get('auth_password', manager.encode('secret'))
    auth_secret = os.environ.get('JOURNAL_AUTH_SECRET', 'itsaseekrit')
    authn_policy = AuthTktAuthenticationPolicy(
        # 'secret'
        secret=auth_secret,
        callback=groupfinder,
        hashalg='sha512'
    )
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(
        root_factory=DefaultRoot,
        settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
    )

    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('add_entry', '/write')
    config.add_route('login', '/login')
    config.add_route('entry', '/entry/{entry}')
    config.add_route('edit_entry', '/entry/{entry}/edit')
    config.scan()
    return config.make_wsgi_app()
