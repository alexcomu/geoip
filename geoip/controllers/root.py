# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from geoip import model
from geoip.lib.base import BaseController
from geoip.controllers.error import ErrorController
import socket, struct

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the geoip application.
    """
    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "geoip"

    @expose('json')
    def _default(self, *args, **kw):
        try:
            ip = request.url.split('/')[-1]
            geo = model.GeoIP.getRange(self.ip2long(ip))
            return dict(status="200", geoip=geo)
        except Exception as e:
            print e
            return dict(status="500", error="We need a valid IP!")

    def ip2long(self, ip):
        """
        Convert an IP string to long
        """
        if ip.count('.') != 3:
            raise Exception
        packedIP = socket.inet_aton(ip)
        return struct.unpack("!L", packedIP)[0]

    @expose('geoip.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)
