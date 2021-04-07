from flask_login import current_user
from functools import wraps
from flask import abort, current_app

def user_write_access(func):
    '''
    If you decorate a function with this, it will ensure that the current user has
    write access before calling the actual function. If they do not
    a 403 error is raised. For example::

        @app.route('/stuff')
        @def user_write_access(func):
        def stuff():
            pass
    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)    
        elif current_user.is_readonly:
            abort(403, "User does not write have permision")
        return func(*args, **kwargs)
    return decorated_view

def user_admin_access(func):
    '''
    If you decorate a function with this, it will ensure that the current user has
    admin access before calling the actual function. If they do not
    a 403 error is raised. For example::

        @app.route('/stuff')
        @def user_admin_access(func):
        def stuff():
            pass
    '''
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)    
        if not current_user.is_admin:
            abort(403, "User does not admin have permision")
        return func(*args, **kwargs)
    return decorated_view
