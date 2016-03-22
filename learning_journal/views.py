from pyramid.view import (view_config, forbidden_view_config)
from pyramid.security import (remember, forget)
import pyramid.httpexceptions as ex
import markdown
from jinja2 import Markup
from .models import (DBSession, Entry, NewEntry, LoginPage)
from learning_journal.security import (check_pw, check_username)


@view_config(route_name='home', renderer='templates/list.jinja2', permission='view')
def list_view(request):
    entries = DBSession.query(Entry).order_by(Entry.created.desc()).all()
    return {'entries': entries}


@view_config(route_name='entry', renderer='templates/entry.jinja2', permission='view')
def detail_view(request):
    this_id = request.matchdict['entry']
    this_entry = DBSession.query(Entry).get(this_id)
    if this_entry is None:
        raise ex.HTTPNotFound()
    this_entry.text = Markup(markdown.markdown(this_entry.text))
    return {'entry': this_entry, 'logged_in': request.authenticated_userid}


@view_config(route_name='add_entry', renderer='templates/add.jinja2', permission='edit')
def add_new(request):
    form = NewEntry(request.POST)
    if request.POST and form.validate():
        entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(entry)
        DBSession.flush()
        return ex.HTTPFound(request.route_url('entry', entry=entry.id))
    return {'form': form}


@view_config(route_name="edit_entry", renderer="templates/edit.jinja2", permission='edit')
def edit_existing(request):
    post_id = request.matchdict['entry']
    this_entry = DBSession.query(Entry).filter(Entry.id == post_id).first()
    form = NewEntry(request.POST, this_entry)

    if request.POST and form.validate():
        form.populate_obj(this_entry)
        return ex.HTTPFound(request.route_url('entry', entry=post_id))
    return {'form': form}


@view_config(context=".models.DefaultRoot", route_name="login", renderer="templates/login.jinja2")
@forbidden_view_config(renderer="templates/login.jinja2")
def login(request):
    form = LoginPage(request.POST)
    login_url = request.resource_url(request.context, "login")
    message, username, password = "", "", ""
    referrer = request.url
    if referrer == login_url: referrer = '/'
    came_from = request.params.get('came_from', referrer)

    if request.POST:
        username = request.params.get('username', '')
        password = request.params.get('password', "")
        if check_username(username) and check_pw(password):
            headers = remember(request, username)
            return ex.HTTPFound(location=came_from, headers=headers)
        message = "That login failed!"

    return {
        "form": form,
        "message": message,
        "url": request.application_url + '/login',
        "came_from": came_from,
        "username": username,
        "password": password
    }


@view_config(context=".models.DefaultRoot", name="logout")
def logout(request):
    headers = forget(request)
    return ex.HTTPFound(location=request.resource_url(request.context), headers=headers)
