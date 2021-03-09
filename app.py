# Import dependnecies
from flask import ( 
    Flask, 
    render_template, 
    request, 
    redirect, 
    url_for, 
    )
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    )
import logging

# Appliction imports
from view_model import ViewModel
from mongo_db.item_store import ItemStore
from mongo_db.user_store import UserStore
from github_oauth import GithubOauthProvider
from user.user import User
from user.user_access import user_write_access, user_admin_access
from user.user_role import UserRole

def create_app(item_store = ItemStore(), user_store = UserStore()):
    app = Flask(__name__)
    logging.basicConfig(level=logging.INFO)

    oauth_provider = GithubOauthProvider()

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.secret_key = oauth_provider.get_client_secret()
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        # Authenticate with GitHub
        return redirect(oauth_provider.get_authenticate_uri())
    
    @login_manager.user_loader
    def load_user(user_id):
        user = user_store.get_user(user_id)
        return user

    @app.route('/login/callback')
    def login_callback():                                                            # pylint: disable=unused-variable
        # Get authorization code from github 
        code = request.args.get("code")

        # Use the authorization code to get user info
        userinfo = oauth_provider.get_user_info(
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code)

        user = User.from_json(userinfo)
        user_store.add_user_if_missing(user)

        # Begin user session
        login_user(user)

        return redirect("/")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route("/admin")
    @login_required
    @user_admin_access
    def admin():
        users =  user_store.get_users()
        return render_template('admin.html', users=users, login_disabled=is_login_disabled(),  current_user=current_user)

    @app.route('/user/<operation>/<id>', methods=['POST'])
    @login_required
    @user_write_access
    def update_user(operation, id):                                     # pylint: disable=unused-variable
        print(f"Updateing user id={id} to {operation}")
        if operation == "reader":
            user_store.update_user(id, UserRole.READER)
        elif operation == "writer":
            user_store.update_user(id, UserRole.WRITER)
        elif operation == "admin":
            user_store.update_user(id, UserRole.ADMIN)
        elif operation == "delete":
            user_store.remove_user(id)
        return redirect("/admin")

    @app.route('/')
    @login_required
    def index():                                                            # pylint: disable=unused-variable
        items =  item_store.get_items()
        return render_template('index.html', view_model=ViewModel(items), login_disabled=is_login_disabled(), current_user=current_user)

    @app.route('/update/<id>/<new_status>', methods=['POST'])
    @login_required
    @user_write_access
    def update(id, new_status):                                             # pylint: disable=unused-variable
        app.logger.info(f'Updateing item id={id} new_status={new_status}')  # pylint: disable=no-member
        item_store.update_item(id, new_status)
        return redirect("/")

    @app.route('/add', methods=['GET', 'POST'])
    @login_required
    @user_write_access
    def add():                                                              # pylint: disable=unused-variable
        if request.method == 'POST':
            if 'add' in request.form:
                app.logger.info(f'Processing add name={request.form.get("new_todo_title")}') # pylint: disable=no-member
                item_store.add_item(
                    request.form.get('new_todo_title'),
                    request.form.get('new_todo_description'),
                    request.form.get('new_todo_due'))
            return redirect("/")

        return render_template('add.html')

    @app.route('/editdetails/<id>', methods=['GET', 'POST'])
    @login_required
    @user_write_access
    def editdetails(id):                                                   # pylint: disable=unused-variable
        if request.method == 'POST':
            if 'edit' in request.form:
                app.logger.info(f'Editing item id={id}')                   # pylint: disable=no-member
                item_store.edit_item(id, 
                    request.form.get('todo_title'),
                    request.form.get('todo_description'),
                    request.form.get('todo_due'))
            return redirect("/")

        return render_template('editdetails.html', item=item_store.get_item(id))

    @app.route('/delete/<id>', methods=['GET', 'POST'])
    @login_required
    @user_write_access
    def delete(id):                                                         # pylint: disable=unused-variable
        print(f"in delete removing {id}")
        if request.method == 'POST':
            if 'delete' in request.form:
                app.logger.info(f'Deleting item id={id}')                   # pylint: disable=no-member
                item_store.remove_item(id)
            return redirect("/")

        return render_template('delete.html', item=item_store.get_item(id))

    def is_login_disabled():                                                         # pylint: disable=unused-variable
        if('LOGIN_DISABLED' in app.config):
            return app.config['LOGIN_DISABLED']
        return False

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
