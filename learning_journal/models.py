from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Unicode,
)

import datetime
from wtforms import Form, StringField, TextAreaField, PasswordField
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker)
from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.security import (Allow, Everyone, ALL_PERMISSIONS)
import os
import markdown

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class DefaultRoot(object):
    """Default Root."""

    __name__ = None
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Everyone, 'read'),
        (Allow, 'group:users', 'edit'),
        (Allow, 'group:admin', ALL_PERMISSIONS)]

    def __init__(self, request):
        """Init Default Root Class."""
        self.request = request


class Entry(Base):
    """Create New Entry in Entries Table."""

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(120))
    text = Column(Unicode)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def markdown_text(self):
        md = markdown.Markdown(safe_mode='replace', html_replacement_text='--RAW HTML NOT ALLOWED --')
        return md.convert(self.text)

    def __json__(self, request):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'created': self.created,
            'markdown': self.markdown
        }


class NewEntry(Form):
    """Create Form for New Entry."""

    title = StringField('Title')
    text = TextAreaField('Text')


class LoginPage(Form):
    """Create Form for Login Page."""

    username = StringField('username')
    password = PasswordField('password')
